from utils.command_factory import ICommand


class DefaultCommand(ICommand):
    """Default command that handles unknown commands"""

    def execute(self, args: list[str]) -> None:
        """Execute the default command"""
        print(f"Unknown command: {' '.join(args)}. Use '-h' for help.")
