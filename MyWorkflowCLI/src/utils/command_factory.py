# command_factory.py
# This is a command factory that registers commands dynamically
from abc import ABC, abstractmethod


class ICommand(ABC):
    """Interface for all commands"""

    @abstractmethod
    def execute(self, args: list[str]) -> None:
        """Execute the command with given arguments"""
        pass


class CommandFactory:
    """Factory class to create command instances"""

    @staticmethod
    def create_command(command_name: str) -> ICommand | None:
        """Create a command instance based on the command name string"""
        # import commands here to avoid circular imports
        from commands.argocd_command import ArgoCdCommand
        from commands.default_command import DefaultCommand
        from commands.docker_command import DockerCommand
        from commands.git_command import GitCommand
        from commands.help_command import HelpCommand

        command_map = {
            "-h": HelpCommand,
            "git": GitCommand,
            "argocd": ArgoCdCommand,
            "docker": DockerCommand,
            # Add other commands here
        }

        command_class = command_map.get(command_name.lower(), DefaultCommand)
        return command_class()
