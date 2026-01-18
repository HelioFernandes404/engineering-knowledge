# Zsh Configuration Backup Tool

A simple script to backup and restore your `.zshrc` configuration file.

## Quick Start

### Using Make (Recommended)

```bash
make backup    # Create backup
make list      # Show backups
make apply     # Restore backup (interactive)
make help      # Show all commands
```

### Using Script Directly

```bash
./backup_zshrc.sh <command>
```

## Make Commands

| Command | Description |
|---------|-------------|
| `make backup` | Create a timestamped backup of current `.zshrc` |
| `make apply` | Interactively restore `.zshrc` from backup |
| `make restore` | Same as `make apply` |
| `make list` | Show available backup files |
| `make help` | Show help message |

## Script Commands

| Command | Alias | Description |
|---------|-------|-------------|
| `backup` | `b` | Create a timestamped backup of current `.zshrc` |
| `restore` | `r` | Restore `.zshrc` from backup file |
| `list` | `l` | Show available backup files |

### Examples

```bash
# Using Make
make backup
make apply

# Using script directly
./backup_zshrc.sh backup
./backup_zshrc.sh list
./backup_zshrc.sh restore zshrc_backup_20250822_155435
```

## Backup Locations

Backups are stored in two places for redundancy:
- `~/heliofernandes404/zshrc_config/` (this directory)
- `~/.zshrc.backup.*` (home directory)

## Safety Features

- Before restoring, current `.zshrc` is automatically backed up
- Timestamps ensure unique backup names
- Script validates file existence before operations