# MyWorkflow CLI

A Python-based CLI tool that provides convenient shortcuts for common development commands including Git, Docker, and ArgoCD operations.

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone <repository-url>
cd MyWorkflowCLI

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# or
.venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Install the package locally
pip install -e .
```

### Basic Usage

```bash
# Show available commands
myworkflow

# Get help for a specific command
myworkflow git --help
myworkflow docker --help
myworkflow argocd --help
```

## 📋 Available Commands

### Git Commands

Streamlined Git workflow operations:

```bash
myworkflow git --status                    # Show git status
myworkflow git --commit "commit message"   # Add and commit changes
myworkflow git --stash push               # Stash current changes
myworkflow git --stash list               # List all stashes
myworkflow git --stash pop                # Apply latest stash
myworkflow git --config-aliases           # Show git aliases
```

### Docker Commands

Essential Docker operations made simple:

```bash
myworkflow docker build .                 # Build image from current directory
myworkflow docker run nginx:latest       # Run a container
myworkflow docker ps                      # List running containers
myworkflow docker images                 # List available images
myworkflow docker logs container_name    # View container logs
myworkflow docker exec container_name bash  # Execute command in container
myworkflow docker rm container_name      # Remove container
myworkflow docker rmi image_name         # Remove image
```

### ArgoCD Commands

ArgoCD application management:

```bash
myworkflow argocd login argocd.example.com     # Login to ArgoCD
myworkflow argocd app list                     # List applications
myworkflow argocd app get my-app               # Get app details
myworkflow argocd app sync my-app              # Sync application
myworkflow argocd app history my-app           # Show app history
myworkflow argocd proj list                    # List projects
```

## 🛠️ Development

### Setup Development Environment

```bash
# Install development dependencies
pip install -r requirements.txt

# Install pre-commit hooks (optional)
pre-commit install
```

### Code Quality

This project uses `ruff` for linting and formatting:

```bash
# Check code quality
ruff check src/

# Format code
ruff format src/

# Run pre-commit hooks
pre-commit run --all-files
```

### Project Structure

```
MyWorkflowCLI/
├── src/
│   ├── main.py              # CLI entry point
│   ├── commands/            # Command implementations
│   │   ├── git_command.py
│   │   ├── docker_command.py
│   │   ├── argocd_command.py
│   │   └── ...
│   └── utils/
│       └── command_factory.py  # Command factory pattern
├── docs/
│   └── commands.md          # Detailed command documentation
├── requirements.txt
└── pyproject.toml          # Project configuration
```

## 📖 Documentation

- **[Commands Documentation](docs/commands.md)** - Comprehensive guide to all available commands

## 🤝 Contributing

### Adding New Commands

1. Create a new command class in `src/commands/` implementing the `ICommand` interface
2. Add the command to the factory in `src/utils/command_factory.py`
3. Update the help text in `src/main.py`
4. Add documentation to `docs/commands.md`

Example command structure:

```python
from utils.command_factory import ICommand
import subprocess

class MyCommand(ICommand):
    def execute(self, args: list[str]) -> None:
        if len(args) < 3:
            self._show_help()
            return
        
        option = args[2].lower()
        
        if option in ["--help", "-h"]:
            self._show_help()
        # Add your command logic here
    
    def _show_help(self):
        print("My Command Help")
        # Add help text here
```

### Commit Convention

This project uses conventional commits:

```bash
# Make a conventional commit
cz commit

# Bump version
cz bump
```

## 🧪 Testing

```bash
# Test basic functionality
python src/main.py --help
python src/main.py git --status
python src/main.py docker ps
```

## 🔧 Configuration

The CLI is configured through:

- **Ruff**: Code formatting and linting (configured in `pyproject.toml`)
- **Commitizen**: Conventional commits and versioning
- **Pre-commit**: Code quality hooks

## 📝 Examples

### Daily Development Workflow

```bash
# Check current status
myworkflow git --status

# Stage and commit changes
myworkflow git --commit "feat: add new authentication feature"

# Build and test with Docker
myworkflow docker build -t myapp:latest .
myworkflow docker run --rm myapp:latest pytest

# Deploy via ArgoCD
myworkflow argocd app sync my-application
```

### Container Debugging

```bash
# Check running containers
myworkflow docker ps

# View logs
myworkflow docker logs my-container

# Access container shell
myworkflow docker exec my-container bash

# Clean up
myworkflow docker rm $(docker ps -a -q --filter status=exited)
```

## 🐛 Troubleshooting

### Common Issues

1. **Command not found**: Make sure you've installed the package with `pip install -e .`
2. **Permission errors**: Ensure your user has appropriate permissions for Docker/Git operations
3. **ArgoCD login fails**: Check your server URL and credentials

### Getting Help

- Use `myworkflow <command> --help` for command-specific help
- Check the [detailed documentation](docs/commands.md)
- Review error messages for specific guidance

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🚀 Roadmap

Future enhancements planned:

- [ ] Kubernetes (kubectl) commands
- [ ] Helm operations
- [ ] SSH connection management
- [ ] Linux system commands
- [ ] Docker Compose operations
- [ ] Configuration file support
- [ ] Command aliases and custom shortcuts