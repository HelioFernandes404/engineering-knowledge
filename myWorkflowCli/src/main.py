# main.py
import sys

from utils.command_factory import CommandFactory


def show_help():
    print("MyWorkflow CLI - Development Command Shortcuts")
    print("Usage: myworkflow <command> [options]")
    print("")
    print("Available commands:")
    print("  -h                Show help")
    print("  git               Git workflow shortcuts")
    print("  docker            Docker command shortcuts")
    print("  argocd            ArgoCD operations")
    print("")
    print("Use 'myworkflow <command> --help' for command-specific help.")


def main():
    """Main entry point for the CLI application"""
    if len(sys.argv) <= 1:
        show_help()
        return

    command = sys.argv[1].lower()
    command_handler = CommandFactory.create_command(command)

    if command_handler is None:
        print(f"Command '{command}' not found. Use '-h' for help.")
        return

    try:
        command_handler.execute(sys.argv)
    except KeyboardInterrupt:
        print("\nProcess interrupted by user.")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
