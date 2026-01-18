"""
CLI utilities for k9s-config.

Handles interactive prompts for selecting companies and hosts from inventories.
"""

import sys
from pathlib import Path
from typing import Tuple, Dict, Any, Optional
import questionary
from questionary import Style
from .inventory import load_inventories, extract_hosts_from_inventory
from .network import check_vpn_requirement, check_network_requirement


# Define a custom style to override terminal defaults and ensure visibility
custom_style = Style([
    ('qmark', 'fg:#E91E63 bold'),       # Pink question mark
    ('question', 'bold'),               # Bold question text
    ('answer', 'fg:#2196F3 bold'),      # Blue submitted answer
    ('pointer', 'fg:#E91E63 bold'),     # Pink pointer
    ('highlighted', 'fg:#E91E63 bold'), # Pink highlighted choice
    ('selected', 'fg:#E91E63'),         # Pink selected item
    ('separator', 'fg:#cc5454'),        # Red separator
    ('instruction', ''),                # User instructions
    ('text', ''),                       # Plain text
    ('disabled', 'fg:#858585 italic')   # Gray disabled choices
])


def select_company(inventory_path: Path) -> Tuple[Optional[str], Optional[Dict[str, Any]]]:
    """
    Interactively select a company from available inventories.

    Args:
        inventory_path: Path to inventory directory

    Returns:
        tuple: (company_name, inventory_data) or (None, None) if cancelled

    Exits:
        If no inventories found
    """
    inventories = load_inventories(inventory_path)

    if not inventories:
        print("No inventories found in inventory/ directory.", file=sys.stderr)
        sys.exit(1)

    companies = sorted(inventories.keys())

    try:
        # Use autocomplete for searchable list
        company = questionary.autocomplete(
            "Select company (type to search):",
            choices=companies,
            match_middle=True,  # Allow matching anywhere in the string
            style=custom_style
        ).ask()

        if company is None:  # ESC or Ctrl+C
            return None, None

        return company, inventories[company]
    except KeyboardInterrupt:
        return None, None


def select_host(company: str, inv_data: Dict[str, Any]) -> Tuple[Optional[str], Optional[Dict[str, Any]]]:
    """
    Interactively select a host from a company's inventory.

    Displays hosts with indicators for VPN and sshuttle requirements.

    Args:
        company: Company name (for display)
        inv_data: Inventory data dict

    Returns:
        tuple: (host_name, host_info_dict) or (None, None) if cancelled

    Exits:
        If no hosts found
    """
    hosts = extract_hosts_from_inventory(inv_data)

    if not hosts:
        print(f"No hosts found in {company} inventory.", file=sys.stderr)
        sys.exit(1)

    # Build choices with indicators - autocomplete needs string labels
    choices = []
    label_to_host = {}  # Map display label -> host_name

    for host_name in sorted(hosts.keys()):
        group = hosts[host_name]["group"]
        host_info = hosts[host_name]

        needs_vpn = check_vpn_requirement(inv_data, group, host_name)
        network_type, network_range = check_network_requirement(host_name, host_info)

        indicators = []
        if needs_vpn:
            indicators.append("[VPN]")
        if network_type == "sshuttle":
            indicators.append(f"[sshuttle {network_range}]")

        label = f"{host_name} ({group})"
        if indicators:
            label += " " + " ".join(indicators)

        choices.append(label)
        label_to_host[label] = host_name

    try:
        # Use autocomplete for searchable/filterable list
        selected_label = questionary.autocomplete(
            f"Select host in {company} (type to search):",
            choices=choices,
            match_middle=True,  # Allow matching anywhere in the string
            style=custom_style
        ).ask()

        if selected_label is None:  # ESC or Ctrl+C
            return None, None

        # Map label back to host_name
        host_name = label_to_host[selected_label]
        return host_name, hosts[host_name]
    except KeyboardInterrupt:
        return None, None
