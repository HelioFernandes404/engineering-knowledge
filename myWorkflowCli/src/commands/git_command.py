import subprocess

from utils.command_factory import ICommand


class GitCommand(ICommand):
    def execute(self, args: list[str]) -> None:
        if len(args) < 3:
            self._show_help()
            return

        option = args[2].lower()

        if option in ["--help", "-h"]:
            self._show_help()
        elif option == "--status":
            self._run_git_command(["git", "status"])
        elif option == "--commit":
            self._handle_commit(args[3:] if len(args) > 3 else [])
        elif option == "--stash":
            self._handle_stash(args[3:] if len(args) > 3 else [])
        elif option == "--config-aliases":
            self._run_git_command(["git", "config", "--global", "--list"], grep="alias")
        else:
            print(f"Unknown option: {option}")
            self._show_help()

    def _run_git_command(self, command: list[str], grep: str = None) -> None:
        """Run the git command with the provided arguments."""
        try:
            if grep:
                # Use shell pipeline for grep
                full_command = " ".join(command) + f" | grep {grep}"
                result = subprocess.run(
                    full_command, shell=True, capture_output=True, text=True
                )
            else:
                result = subprocess.run(command, capture_output=True, text=True)

            if result.returncode == 0:
                if result.stdout:
                    print(result.stdout.strip())
            else:
                print(f"Error: {result.stderr.strip()}")

        except Exception as e:
            print(f"Failed to execute command: {e}")

    def _handle_commit(self, args: list[str]) -> None:
        if not args:
            # Interactive commit - let user provide commit message
            message = input("Enter commit message: ").strip()
            if message:
                self._run_git_command(["git", "add", "."])
                self._run_git_command(["git", "commit", "-m", message])
            else:
                print("Commit cancelled - no message provided")
        else:
            # Commit with provided message
            message = " ".join(args)
            self._run_git_command(["git", "add", "."])
            self._run_git_command(["git", "commit", "-m", message])

    def _handle_stash(self, args: list[str]) -> None:
        if not args:
            print("Stash command requires an action (push, list, pop)")
            return

        action = args[0].lower()
        if action == "push":
            self._run_git_command(["git", "stash", "push"])
        elif action == "list":
            self._run_git_command(["git", "stash", "list"])
        elif action == "pop":
            self._run_git_command(["git", "stash", "pop"])
        else:
            print(f"Unknown stash action: {action}")

    def _show_help(self):
        """Display help information for the git command."""
        print("Git Command Help")
        print("Usage: myworkflow git [options]")
        print("Options:")
        print("  --help, -h                    Show this help")
        print("  --status                      Show git status")
        print(
            "  --commit [message]            Make a commit (interactive if no message)"
        )
        print("  --stash push                  Push changes to stash")
        print("  --stash list                  List all stashed changes")
        print("  --stash pop                   Pop changes from stash")
        print("  --config-aliases              Show all git alias configs")
