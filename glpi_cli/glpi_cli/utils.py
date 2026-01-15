"""Utility functions for GLPI CLI."""


# Common GLPI ItemTypes with their correct PascalCase format
KNOWN_ITEMTYPES = {
    # Assets
    "computer": "Computer",
    "monitor": "Monitor",
    "printer": "Printer",
    "networkequipment": "NetworkEquipment",
    "peripheral": "Peripheral",
    "phone": "Phone",
    "software": "Software",
    "softwarelicense": "SoftwareLicense",
    "softwareversion": "SoftwareVersion",

    # Helpdesk
    "ticket": "Ticket",
    "ticketfollowup": "TicketFollowup",
    "tickettask": "TicketTask",
    "ticketvalidation": "TicketValidation",
    "itilcategory": "ITILCategory",
    "problem": "Problem",
    "change": "Change",
    "solution": "Solution",
    "solutiontemplate": "SolutionTemplate",

    # Management
    "user": "User",
    "group": "Group",
    "entity": "Entity",
    "profile": "Profile",
    "location": "Location",
    "supplier": "Supplier",
    "contact": "Contact",
    "contract": "Contract",
    "budget": "Budget",
    "document": "Document",
    "documenttype": "DocumentType",
    "knowbaseitem": "KnowbaseItem",

    # Administration
    "log": "Log",
    "event": "Event",
    "crontask": "CronTask",
    "config": "Config",
    "plugin": "Plugin",

    # Network
    "network": "Network",
    "networkport": "NetworkPort",
    "networkname": "NetworkName",
    "ipaddress": "IPAddress",
    "ipnetwork": "IPNetwork",
    "fqdn": "FQDN",
    "vlan": "Vlan",

    # Other
    "project": "Project",
    "projecttask": "ProjectTask",
    "reminder": "Reminder",
    "rssfeed": "RSSFeed",
    "reservation": "Reservation",
}


def normalize_itemtype(itemtype: str) -> str:
    """Convert ItemType to correct PascalCase format.

    Supports case-insensitive input and automatically converts to GLPI's
    expected PascalCase format.

    Examples:
        >>> normalize_itemtype("ticket")
        'Ticket'
        >>> normalize_itemtype("COMPUTER")
        'Computer'
        >>> normalize_itemtype("NetworkEquipment")
        'NetworkEquipment'
        >>> normalize_itemtype("unknown")
        'Unknown'

    Args:
        itemtype: Item type in any case format

    Returns:
        ItemType in PascalCase format
    """
    # Convert to lowercase for lookup
    itemtype_lower = itemtype.lower()

    # Check if it's a known itemtype
    if itemtype_lower in KNOWN_ITEMTYPES:
        return KNOWN_ITEMTYPES[itemtype_lower]

    # If not found, capitalize first letter (best effort)
    return itemtype.capitalize()


def get_available_itemtypes() -> list[str]:
    """Get list of commonly used ItemTypes.

    Returns:
        List of ItemType names in PascalCase
    """
    return sorted(set(KNOWN_ITEMTYPES.values()))
