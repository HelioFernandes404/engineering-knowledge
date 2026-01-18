import subprocess

from utils.command_factory import ICommand


class ArgoCdCommand(ICommand):
    def execute(self, args: list[str]) -> None:
        if len(args) < 3:
            self._show_help()
            return

        option = args[2].lower()

        if option in ["--help", "-h"]:
            self._show_help()
        elif option == "login":
            self._handle_login(args[3:] if len(args) > 3 else [])
        elif option == "app":
            self._handle_app(args[3:] if len(args) > 3 else [])
        elif option == "proj":
            self._handle_proj(args[3:] if len(args) > 3 else [])
        else:
            print(f"Unknown option: {option}")
            self._show_help()

    def _handle_login(self, args: list[str]) -> None:
        if not args:
            print("Error: Server URL is required for argocd login")
            return

        server = args[0]
        login_args = ["argocd", "login", server]
        if len(args) > 1:
            login_args.extend(args[1:])
        self._run_argocd_command(login_args)

    def _handle_app(self, args: list[str]) -> None:
        if not args:
            print(
                "Error: App subcommand is required (list, get, sync, create, delete, rollback, history, diff)"
            )
            return

        subcommand = args[0].lower()
        if subcommand == "list":
            self._run_argocd_command(["argocd", "app", "list"])
        elif subcommand == "get":
            if len(args) < 2:
                print("Error: App name is required for 'app get'")
                return
            self._run_argocd_command(["argocd", "app", "get", args[1]])
        elif subcommand == "sync":
            if len(args) < 2:
                print("Error: App name is required for 'app sync'")
                return
            sync_args = ["argocd", "app", "sync", args[1]]
            if len(args) > 2:
                sync_args.extend(args[2:])
            self._run_argocd_command(sync_args)
        elif subcommand == "create":
            self._handle_app_create(args[1:] if len(args) > 1 else [])
        elif subcommand == "delete":
            if len(args) < 2:
                print("Error: App name is required for 'app delete'")
                return
            self._run_argocd_command(["argocd", "app", "delete", args[1]])
        elif subcommand == "rollback":
            if len(args) < 3:
                print("Error: App name and revision are required for 'app rollback'")
                return
            self._run_argocd_command(["argocd", "app", "rollback", args[1], args[2]])
        elif subcommand == "history":
            if len(args) < 2:
                print("Error: App name is required for 'app history'")
                return
            self._run_argocd_command(["argocd", "app", "history", args[1]])
        elif subcommand == "diff":
            if len(args) < 2:
                print("Error: App name is required for 'app diff'")
                return
            self._run_argocd_command(["argocd", "app", "diff", args[1]])
        else:
            print(f"Unknown app subcommand: {subcommand}")

    def _handle_app_create(self, args: list[str]) -> None:
        if len(args) < 8:
            print(
                "Error: App create requires: <APPNAME> --repo <REPO> --path <PATH> --dest-server <SERVER> --dest-namespace <NAMESPACE>"
            )
            return

        create_args = ["argocd", "app", "create"] + args
        self._run_argocd_command(create_args)

    def _handle_proj(self, args: list[str]) -> None:
        if not args:
            print("Error: Project subcommand is required (list)")
            return

        subcommand = args[0].lower()
        if subcommand == "list":
            self._run_argocd_command(["argocd", "proj", "list"])
        else:
            print(f"Unknown project subcommand: {subcommand}")

    def _run_argocd_command(self, command: list[str]) -> None:
        try:
            result = subprocess.run(command, capture_output=True, text=True)

            if result.returncode == 0:
                if result.stdout:
                    print(result.stdout.strip())
            else:
                print(f"Error: {result.stderr.strip()}")

        except Exception as e:
            print(f"Failed to execute command: {e}")

    def workflow_command(self) -> None:
        pass

    def _show_help(self):
        """
        Displays help information for the Argocd command, including usage instructions and available options.
        """
        print("ArgoCD Command Help")
        print("Usage: myworkflow argocd [command] [args...]")
        print("Commands:")
        print("  --help, -h                             Show this help")
        print("  login <SERVER> [options]               Login to ArgoCD server")
        print("  app list                               List applications")
        print("  app get <APPNAME>                      Get application details")
        print("  app sync <APPNAME> [options]           Sync application")
        print("  app create <APPNAME> [options]         Create new application")
        print("  app delete <APPNAME>                   Delete application")
        print(
            "  app rollback <APPNAME> <REVISION>      Rollback application to revision"
        )
        print("  app history <APPNAME>                  Show application history")
        print("  app diff <APPNAME>                     Show application diff")
        print("  proj list                              List projects")
