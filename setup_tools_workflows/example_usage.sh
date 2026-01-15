#!/bin/bash

# Example usage of clone_repos.sh
# This file demonstrates common use cases

# Uncomment and modify the examples below to use them

# Example 1: Clone all repos from systemframe organization
# ./clone_repos.sh systemframe

# Example 2: Clone all repos from systemframe to a specific directory
# ./clone_repos.sh -d ~/projects/systemframe systemframe

# Example 3: Clone using HTTPS instead of SSH
# ./clone_repos.sh -m https systemframe

# Example 4: Clone with fewer parallel jobs (useful on slower connections)
# ./clone_repos.sh -p 2 systemframe

# Example 5: Clone only public repositories
# ./clone_repos.sh --public-only systemframe

# Example 6: Clone excluding forks
# ./clone_repos.sh --no-forks systemframe

# Example 7: Clone repos matching a pattern
# ./clone_repos.sh -f "ansible" systemframe

# Example 8: Full backup with all options
# ./clone_repos.sh --archived -d ~/backup/systemframe -l 2000 systemframe

echo "This is an example file. Please edit it to run the commands you need."
echo "Or run clone_repos.sh directly with your desired options."
echo ""
echo "Usage: ./clone_repos.sh [OPTIONS] <org-or-user>"
echo "Run './clone_repos.sh --help' for more information."
