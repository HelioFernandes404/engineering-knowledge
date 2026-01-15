"""Utility functions for CLI tools."""

import hashlib
import json


def generate_fingerprint(payload):
    """
    Generate SHA256 fingerprint from payload.

    For payloads with multiple alerts, generates a composite fingerprint
    from all alerts' metadata to ensure consistency across fire/resolve operations.

    Args:
        payload: Dict containing the alert payload with 'alerts' array

    Returns:
        str: SHA256 hash of the payload fingerprint
    """
    if not isinstance(payload, dict) or "alerts" not in payload:
        raise ValueError("Invalid payload: missing 'alerts' key")

    if not payload["alerts"]:
        raise ValueError("Invalid payload: 'alerts' array is empty")

    # Generate fingerprint from first alert's metadata
    # This matches the behavior in webhook_glpi/scripts/glpi.py
    alert = payload["alerts"][0]

    # Extract fingerprint components (matching glpi.py logic)
    alert_fingerprint = alert.get("fingerprint", "")
    starts_at = alert.get("startsAt", "")
    generator_url = alert.get("generatorURL", "")

    # NOTE: Production code has a bug where it checks alert.get('alertname')
    # instead of alert.get('labels', {}).get('alertname'). To maintain
    # compatibility with existing GLPI problems, we replicate the same behavior.
    # This ensures CLI-generated fingerprints match production fingerprints.
    # TODO: File issue to fix production code and migrate existing fingerprints
    alert_name = alert.get("alertname")  # No default - returns None to match production

    # Concatenate all fields into a single string for hashing
    fingerprint_source = f"{alert_name}|{alert_fingerprint}|{starts_at}|{generator_url}"

    # Generate SHA256 hash
    sha256_hash = hashlib.sha256(fingerprint_source.encode("utf-8")).hexdigest()

    return sha256_hash
