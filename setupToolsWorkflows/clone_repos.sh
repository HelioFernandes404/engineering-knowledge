#!/bin/bash

# Script to clone all repositories from a GitHub organization or user
# Uses GitHub CLI (gh) for authentication and API access

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Default values
LIMIT=1000
PARALLEL_JOBS=8
TARGET_DIR="."
CLONE_METHOD="ssh"  # ssh or https

# Function to display usage
usage() {
    cat << EOF
Usage: $0 [OPTIONS] <org-or-user>

Clone all repositories from a GitHub organization or user.

OPTIONS:
    -l, --limit <number>        Maximum number of repos to fetch (default: 1000)
    -p, --parallel <number>     Number of parallel clone jobs (default: 8)
    -d, --directory <path>      Target directory for cloning (default: current directory)
    -m, --method <ssh|https>    Clone method: ssh or https (default: ssh)
    -f, --filter <pattern>      Filter repos by name (grep pattern)
    --public-only               Clone only public repositories
    --private-only              Clone only private repositories
    --archived                  Include archived repositories
    --no-forks                  Exclude forked repositories
    -h, --help                  Show this help message

EXAMPLES:
    # Clone all repos from an organization
    $0 systemframe

    # Clone with custom parallel jobs and limit
    $0 -p 4 -l 500 myorg

    # Clone to specific directory using HTTPS
    $0 -d ~/projects/myorg -m https myorg

    # Clone only public repos, excluding forks
    $0 --public-only --no-forks myusername

    # Filter repos by name pattern
    $0 -f "backend" myorg

EOF
    exit 1
}

# Function to print colored messages
print_info() {
    echo -e "${BLUE}ℹ${NC} $1"
}

print_success() {
    echo -e "${GREEN}✓${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

# Function to check if gh CLI is installed and authenticated
check_prerequisites() {
    if ! command -v gh &> /dev/null; then
        print_error "GitHub CLI (gh) is not installed."
        echo "Install it from: https://cli.github.com/"
        exit 1
    fi

    if ! gh auth status &> /dev/null; then
        print_error "GitHub CLI is not authenticated."
        echo "Run: gh auth login"
        exit 1
    fi

    print_success "GitHub CLI is installed and authenticated"
}

# Parse command line arguments
FILTER=""
VISIBILITY_FILTER=""
ARCHIVED_FLAG="--no-archived"
FORK_FILTER=""

while [[ $# -gt 0 ]]; do
    case $1 in
        -l|--limit)
            LIMIT="$2"
            shift 2
            ;;
        -p|--parallel)
            PARALLEL_JOBS="$2"
            shift 2
            ;;
        -d|--directory)
            TARGET_DIR="$2"
            shift 2
            ;;
        -m|--method)
            CLONE_METHOD="$2"
            shift 2
            ;;
        -f|--filter)
            FILTER="$2"
            shift 2
            ;;
        --public-only)
            VISIBILITY_FILTER="public"
            shift
            ;;
        --private-only)
            VISIBILITY_FILTER="private"
            shift
            ;;
        --archived)
            ARCHIVED_FLAG=""
            shift
            ;;
        --no-forks)
            FORK_FILTER="no-forks"
            shift
            ;;
        -h|--help)
            usage
            ;;
        -*)
            print_error "Unknown option: $1"
            usage
            ;;
        *)
            ORG_OR_USER="$1"
            shift
            ;;
    esac
done

# Check if org/user was provided
if [ -z "$ORG_OR_USER" ]; then
    print_error "Organization or user name is required"
    usage
fi

# Validate clone method
if [[ "$CLONE_METHOD" != "ssh" && "$CLONE_METHOD" != "https" ]]; then
    print_error "Clone method must be 'ssh' or 'https'"
    exit 1
fi

# Main execution
main() {
    print_info "Starting repository clone process..."
    echo ""

    check_prerequisites

    # Create target directory if it doesn't exist
    if [ ! -d "$TARGET_DIR" ]; then
        mkdir -p "$TARGET_DIR"
        print_success "Created directory: $TARGET_DIR"
    fi

    # Build gh repo list command
    GH_CMD="gh repo list $ORG_OR_USER --limit $LIMIT $ARCHIVED_FLAG"

    if [ -n "$VISIBILITY_FILTER" ]; then
        GH_CMD="$GH_CMD --visibility $VISIBILITY_FILTER"
    fi

    if [ "$FORK_FILTER" == "no-forks" ]; then
        GH_CMD="$GH_CMD --no-archived"
    fi

    # Determine which field to use based on clone method
    if [ "$CLONE_METHOD" == "ssh" ]; then
        CLONE_FIELD="sshUrl"
    else
        CLONE_FIELD="url"
    fi

    print_info "Fetching repository list from: $ORG_OR_USER"
    print_info "Clone method: $CLONE_METHOD"
    print_info "Parallel jobs: $PARALLEL_JOBS"
    echo ""

    # Get repository list
    REPO_LIST=$($GH_CMD --json nameWithOwner,isFork,$CLONE_FIELD,isArchived)

    # Apply filters
    FILTERED_REPOS=$(echo "$REPO_LIST" | jq -r "
        map(select(
            (if \$fork_filter == \"no-forks\" then .isFork == false else true end)
        )) |
        .[].$CLONE_FIELD
    " --arg fork_filter "$FORK_FILTER")

    # Apply name filter if specified
    if [ -n "$FILTER" ]; then
        FILTERED_REPOS=$(echo "$FILTERED_REPOS" | grep "$FILTER")
        print_info "Applied name filter: $FILTER"
    fi

    # Count repositories
    REPO_COUNT=$(echo "$FILTERED_REPOS" | grep -c '^' || true)

    if [ "$REPO_COUNT" -eq 0 ]; then
        print_warning "No repositories found matching the criteria"
        exit 0
    fi

    print_success "Found $REPO_COUNT repositories to clone"
    echo ""

    # Clone repositories
    cd "$TARGET_DIR"

    print_info "Cloning repositories to: $(pwd)"
    echo ""

    echo "$FILTERED_REPOS" | xargs -P"$PARALLEL_JOBS" -I {} bash -c "
        REPO_URL=\"{}\"
        REPO_NAME=\$(basename \"\$REPO_URL\" .git)

        if [ -d \"\$REPO_NAME\" ]; then
            echo -e \"⏭  Skipping \$REPO_NAME (already exists)\"
        else
            echo -e \"📥 Cloning \$REPO_NAME...\"
            if git clone \"\$REPO_URL\" >/dev/null 2>&1; then
                echo -e \"✓ Completed \$REPO_NAME\"
            else
                echo -e \"✗ Failed to clone \$REPO_NAME\" >&2
            fi
        fi
    "

    echo ""
    print_success "Clone process completed!"

    # Summary
    CLONED_COUNT=$(find . -maxdepth 1 -type d | grep -v '^\.$' | wc -l)
    print_info "Total directories in target: $CLONED_COUNT"
}

main
