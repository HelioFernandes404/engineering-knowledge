# -*- coding: utf-8 -*-
"""Output formatters for GLPI CLI."""
import json
from typing import Any, Dict, List
from rich.console import Console
from rich.table import Table
from rich import box


def format_json(data: Any) -> str:
    """Format data as JSON string.

    Args:
        data: Data to format (dict, list, etc.)

    Returns:
        Formatted JSON string with indentation
    """
    return json.dumps(data, indent=2, ensure_ascii=False)


def format_table(data: List[Dict[str, Any]], max_fields: int = 10) -> None:
    """Format list of items as a rich table.

    Args:
        data: List of dictionaries to display
        max_fields: Maximum number of fields to show
    """
    console = Console()

    if not data:
        console.print("[yellow]Nenhum item encontrado[/yellow]")
        return

    # Get all unique keys from all items
    all_keys = set()
    for item in data:
        all_keys.update(item.keys())

    # Prioritize common fields
    priority_fields = ["id", "name", "title", "status", "priority", "type", "date", "date_mod"]
    other_fields = [k for k in all_keys if k not in priority_fields]

    # Build ordered field list
    fields = []
    for pf in priority_fields:
        if pf in all_keys:
            fields.append(pf)

    # Add other fields up to max_fields
    remaining_slots = max_fields - len(fields)
    fields.extend(other_fields[:remaining_slots])

    # Create table
    table = Table(box=box.ROUNDED, show_header=True, header_style="bold cyan")

    # Add columns
    for field in fields:
        table.add_column(field.upper(), overflow="fold")

    # Add rows
    for item in data:
        row = []
        for field in fields:
            value = item.get(field, "")
            # Convert to string and truncate if too long
            str_value = str(value) if value is not None else ""
            if len(str_value) > 50:
                str_value = str_value[:47] + "..."
            row.append(str_value)
        table.add_row(*row)

    console.print(table)

    # Show info about hidden fields
    if len(all_keys) > max_fields:
        hidden = len(all_keys) - max_fields
        console.print(f"\n[dim]({hidden} campos ocultados. Use --json para ver todos)[/dim]")


def format_single_item(data: Dict[str, Any]) -> None:
    """Format single item as key-value pairs.

    Args:
        data: Dictionary with item data
    """
    console = Console()

    if not data:
        console.print("[yellow]Item vazio[/yellow]")
        return

    table = Table(box=box.SIMPLE, show_header=False, padding=(0, 2))
    table.add_column("Campo", style="cyan", no_wrap=True)
    table.add_column("Valor", overflow="fold")

    for key, value in data.items():
        # Skip empty values
        if value is None or value == "":
            continue

        # Format complex values
        if isinstance(value, (dict, list)):
            value_str = json.dumps(value, indent=2, ensure_ascii=False)
        else:
            value_str = str(value)

        table.add_row(key, value_str)

    console.print(table)


def print_error(message: str) -> None:
    """Print error message in red.

    Args:
        message: Error message to display
    """
    console = Console()
    console.print(f"[bold red]\u274c {message}[/bold red]")


def print_success(message: str) -> None:
    """Print success message in green.

    Args:
        message: Success message to display
    """
    console = Console()
    console.print(f"[bold green]\u2714 {message}[/bold green]")


def print_info(message: str) -> None:
    """Print info message in blue.

    Args:
        message: Info message to display
    """
    console = Console()
    console.print(f"[bold blue]\u2139 {message}[/bold blue]")
