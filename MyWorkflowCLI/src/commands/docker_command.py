import subprocess

from utils.command_factory import ICommand


class DockerCommand(ICommand):
    """Docker command that handles docker operations"""

    def execute(self, args: list[str]) -> None:
        """Execute the Docker command"""
        if len(args) < 3:
            self._show_help()
            return

        option = args[2].lower()

        if option in ["--help", "-h"]:
            self._show_help()
        elif option == "build":
            self._handle_build(args[3:] if len(args) > 3 else [])
        elif option == "run":
            self._handle_run(args[3:] if len(args) > 3 else [])
        elif option == "ps":
            self._run_docker_command(["docker", "ps"])
        elif option == "images":
            self._run_docker_command(["docker", "images"])
        elif option == "logs":
            self._handle_logs(args[3:] if len(args) > 3 else [])
        elif option == "exec":
            self._handle_exec(args[3:] if len(args) > 3 else [])
        elif option == "rm":
            self._handle_rm(args[3:] if len(args) > 3 else [])
        elif option == "rmi":
            self._handle_rmi(args[3:] if len(args) > 3 else [])
        else:
            print(f"Unknown option: {option}")
            self._show_help()

    def _handle_build(self, args: list[str]) -> None:
        if not args:
            # Default to current directory
            self._run_docker_command(["docker", "build", "."])
        else:
            path = args[0]
            build_args = ["docker", "build"]
            if len(args) > 1:
                # Handle build options like -t tag
                build_args.extend(args[:-1])
            build_args.append(path)
            self._run_docker_command(build_args)

    def _handle_run(self, args: list[str]) -> None:
        if not args:
            print("Error: Image name is required for docker run")
            return

        run_args = ["docker", "run"] + args
        self._run_docker_command(run_args)

    def _handle_logs(self, args: list[str]) -> None:
        if not args:
            print("Error: Container name/ID is required for docker logs")
            return

        container = args[0]
        log_args = ["docker", "logs", container]
        if len(args) > 1:
            log_args = ["docker", "logs"] + args
        self._run_docker_command(log_args)

    def _handle_exec(self, args: list[str]) -> None:
        if len(args) < 2:
            print("Error: Container name and command are required for docker exec")
            return

        exec_args = ["docker", "exec", "-it"] + args
        self._run_docker_command(exec_args)

    def _handle_rm(self, args: list[str]) -> None:
        if not args:
            print("Error: Container name/ID is required for docker rm")
            return

        rm_args = ["docker", "rm"] + args
        self._run_docker_command(rm_args)

    def _handle_rmi(self, args: list[str]) -> None:
        if not args:
            print("Error: Image name/ID is required for docker rmi")
            return

        rmi_args = ["docker", "rmi"] + args
        self._run_docker_command(rmi_args)

    def _run_docker_command(self, command: list[str]) -> None:
        try:
            result = subprocess.run(command, capture_output=True, text=True)

            if result.returncode == 0:
                if result.stdout:
                    print(result.stdout.strip())
            else:
                print(f"Error: {result.stderr.strip()}")

        except Exception as e:
            print(f"Failed to execute command: {e}")

    def _show_help(self):
        """
        Displays help information for the Docker command, including usage instructions and available options.
        """
        print("Docker Command Help")
        print("Usage: myworkflow docker [command] [args...]")
        print("Commands:")
        print("  --help, -h                    Show this help")
        print("  build [options] <PATH>        Build a Docker image from a Dockerfile")
        print("  run <IMAGE> [options]         Run a Docker container from an image")
        print("  ps                            List running Docker containers")
        print("  images                        List available Docker images")
        print("  rmi <IMAGE>                   Remove a Docker image")
        print("  rm <CONTAINER>                Remove a stopped Docker container")
        print("  logs <CONTAINER> [options]    View logs of a Docker container")
        print(
            "  exec <CONTAINER> <COMMAND>    Execute a command in a running Docker container"
        )
