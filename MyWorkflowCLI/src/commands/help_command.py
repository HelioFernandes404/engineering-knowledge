# commands / help_command.py

from utils.command_factory import ICommand


class HelpCommand(ICommand):
    def execute(self, args: list[str]) -> None:
        print("Use: wf [module] [option]")
        print()
        print("For exemple: wf git -h")
        print("Commands available:")
        print(" -h      Show all commands")
