# MyWorkflow CLI Commands Documentation

This document provides comprehensive documentation for all available commands in the MyWorkflow CLI tool.

## Table of Contents

- [Git Commands](#git-commands)
- [Docker Commands](#docker-commands)
- [ArgoCD Commands](#argocd-commands)
- [Help Commands](#help-commands)

## Git Commands

The git command provides shortcuts for common Git operations.

### Usage
```bash
myworkflow git [option] [arguments]
```

### Available Options

#### `--status`
Shows the current status of the Git repository.

```bash
myworkflow git --status
```

**Example Output:**
```
On branch main
Your branch is up to date with 'origin/main'.
nothing to commit, working tree clean
```

#### `--commit [message]`
Creates a Git commit. If no message is provided, it will prompt interactively for a commit message.

```bash
# Interactive commit (will prompt for message)
myworkflow git --commit

# Commit with message
myworkflow git --commit "Add new feature"
myworkflow git --commit "Fix: resolve issue with authentication"
```

**Behavior:**
- Automatically runs `git add .` before committing
- If no message provided, prompts user to enter commit message
- Cancels commit if empty message is provided

#### `--stash [action]`
Manages Git stash operations.

```bash
# Push current changes to stash
myworkflow git --stash push

# List all stashed changes
myworkflow git --stash list

# Pop most recent stash
myworkflow git --stash pop
```

**Actions:**
- `push` - Stash current changes
- `list` - Show all stashed changes
- `pop` - Apply and remove the most recent stash

#### `--config-aliases`
Shows all Git alias configurations.

```bash
myworkflow git --config-aliases
```

**Example Output:**
```
alias.co=checkout
alias.br=branch
alias.ci=commit
alias.st=status
```

#### `--help, -h`
Shows help information for git commands.

```bash
myworkflow git --help
myworkflow git -h
```

---

## Docker Commands

The docker command provides shortcuts for common Docker operations.

### Usage
```bash
myworkflow docker [command] [arguments]
```

### Available Commands

#### `build [options] <PATH>`
Builds a Docker image from a Dockerfile.

```bash
# Build from current directory
myworkflow docker build

# Build from specific path
myworkflow docker build /path/to/context

# Build with tag
myworkflow docker build -t myapp:latest .
```

#### `run <IMAGE> [options]`
Runs a Docker container from an image.

```bash
# Run container
myworkflow docker run nginx:latest

# Run with options
myworkflow docker run -p 80:80 -d nginx:latest
```

#### `ps`
Lists running Docker containers.

```bash
myworkflow docker ps
```

**Example Output:**
```
CONTAINER ID   IMAGE     COMMAND                  CREATED         STATUS         PORTS     NAMES
abc123def456   nginx     "/docker-entrypoint.…"   2 minutes ago   Up 2 minutes   80/tcp    amazing_docker
```

#### `images`
Lists available Docker images.

```bash
myworkflow docker images
```

**Example Output:**
```
REPOSITORY   TAG       IMAGE ID       CREATED        SIZE
nginx        latest    abc123def456   2 weeks ago    142MB
ubuntu       20.04     def456abc789   3 weeks ago    72.8MB
```

#### `logs <CONTAINER> [options]`
Views logs of a Docker container.

```bash
# View logs
myworkflow docker logs container_name

# View logs with options
myworkflow docker logs -f --tail 100 container_name
```

#### `exec <CONTAINER> <COMMAND>`
Executes a command in a running Docker container.

```bash
# Execute interactive bash
myworkflow docker exec container_name bash

# Execute command
myworkflow docker exec container_name ls -la
```

#### `rm <CONTAINER>`
Removes a stopped Docker container.

```bash
myworkflow docker rm container_name
```

#### `rmi <IMAGE>`
Removes a Docker image.

```bash
myworkflow docker rmi image_name:tag
```

#### `--help, -h`
Shows help information for docker commands.

```bash
myworkflow docker --help
myworkflow docker -h
```

---

## ArgoCD Commands

The argocd command provides shortcuts for ArgoCD operations.

### Usage
```bash
myworkflow argocd [command] [arguments]
```

### Available Commands

#### `login <SERVER> [options]`
Logs in to an ArgoCD server.

```bash
# Basic login
myworkflow argocd login argocd.example.com

# Login with options
myworkflow argocd login argocd.example.com --username admin --password
```

#### Application Commands

All application commands are prefixed with `app`:

##### `app list`
Lists all applications.

```bash
myworkflow argocd app list
```

##### `app get <APPNAME>`
Gets detailed information about a specific application.

```bash
myworkflow argocd app get my-application
```

##### `app sync <APPNAME> [options]`
Synchronizes an application with its Git repository.

```bash
# Basic sync
myworkflow argocd app sync my-application

# Sync with options
myworkflow argocd app sync my-application --prune --force
```

##### `app create <APPNAME> [options]`
Creates a new ArgoCD application.

```bash
myworkflow argocd app create my-app \
  --repo https://github.com/user/repo \
  --path k8s-manifests \
  --dest-server https://kubernetes.default.svc \
  --dest-namespace default
```

##### `app delete <APPNAME>`
Deletes an ArgoCD application.

```bash
myworkflow argocd app delete my-application
```

##### `app rollback <APPNAME> <REVISION>`
Rolls back an application to a specific revision.

```bash
myworkflow argocd app rollback my-application 123
```

##### `app history <APPNAME>`
Shows the deployment history of an application.

```bash
myworkflow argocd app history my-application
```

##### `app diff <APPNAME>`
Shows the difference between the current and desired state.

```bash
myworkflow argocd app diff my-application
```

#### Project Commands

##### `proj list`
Lists all ArgoCD projects.

```bash
myworkflow argocd proj list
```

#### `--help, -h`
Shows help information for ArgoCD commands.

```bash
myworkflow argocd --help
myworkflow argocd -h
```

---

## Help Commands

### Global Help
Shows the main help menu with all available commands.

```bash
myworkflow
myworkflow -h
```

**Output:**
```
MyWorkflow CLI - Development Command Shortcuts
Usage: myworkflow <command> [options]

Available commands:
  -h                Show help
  git               Git workflow shortcuts
  docker            Docker command shortcuts
  argocd            ArgoCD operations

Use 'myworkflow <command> --help' for command-specific help.
```

### Command-Specific Help
Each command supports its own help option:

```bash
myworkflow git --help
myworkflow docker --help
myworkflow argocd --help
```

---

## Error Handling

All commands include proper error handling:

- **Missing Arguments**: Commands will show appropriate error messages when required arguments are missing
- **Command Failures**: If the underlying command fails, the error output will be displayed
- **Invalid Options**: Unknown options will show an error and display help information

### Example Error Messages

```bash
# Missing required argument
$ myworkflow docker logs
Error: Container name/ID is required for docker logs

# Command execution failure
$ myworkflow git --status
Error: not a git repository (or any of the parent directories): .git

# Unknown option
$ myworkflow git --invalid
Unknown option: --invalid
Git Command Help
...
```

---

## Examples and Use Cases

### Development Workflow Example

```bash
# Check git status
myworkflow git --status

# Make changes to code...

# Commit changes
myworkflow git --commit "feat: implement new user authentication"

# Build Docker image
myworkflow docker build -t myapp:v1.0.0 .

# Run tests in container
myworkflow docker run -v $(pwd):/app myapp:v1.0.0 pytest

# Deploy with ArgoCD
myworkflow argocd app sync my-application
```

### Container Management Example

```bash
# List running containers
myworkflow docker ps

# Check container logs
myworkflow docker logs my-container

# Execute command in container
myworkflow docker exec my-container cat /etc/os-release

# Clean up
myworkflow docker rm my-container
myworkflow docker rmi my-image:tag
```

### ArgoCD Management Example

```bash
# Login to ArgoCD
myworkflow argocd login argocd.example.com

# List all applications
myworkflow argocd app list

# Check application status
myworkflow argocd app get my-app

# Sync if needed
myworkflow argocd app sync my-app

# View deployment history
myworkflow argocd app history my-app
```