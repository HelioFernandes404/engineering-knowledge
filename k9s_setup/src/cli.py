"""
CLI utilities for k9s-config.

Handles interactive prompts for selecting companies and hosts from inventories.
"""

import sys
from pathlib import Path
from typing import Tuple, Dict, Any, Optional
import questionary
from .inventory import load_inventories, extract_hosts_from_inventory
from .network import check_vpn_requirement, check_network_requirement


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
        company = questionary.select(
            "Select company:",
            choices=companies
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

    # Build choices with indicators
    choices = []
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

        choices.append(questionary.Choice(title=label, value=host_name))

    try:
        host_name = questionary.select(
            f"Select host in {company}:",
            choices=choices
        ).ask()

        if host_name is None:  # ESC or Ctrl+C
            return None, None

        return host_name, hosts[host_name]
    except KeyboardInterrupt:
        return None, None
