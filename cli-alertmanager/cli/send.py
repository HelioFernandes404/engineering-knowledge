#!/usr/bin/env python3
"""
CLI tool for sending alert payloads to webhooks-alertmanager.

Usage:
    python cli/send.py fire [--file payload.json] [--dry-run]
    python cli/send.py resolve [--file payload.json] [--dry-run]
"""

import argparse
import json
import sys
from copy import deepcopy
from datetime import datetime, timezone
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError
from .session_manager import (
    load_sessions,
    save_sessions,
    create_session,
    get_sessions_file,
    get_active_sessions,
    get_session_by_id,
    update_session_status,
    delete_resolved_sessions,
    format_session_display,
)
from .utils import generate_fingerprint


ENDPOINT = "http://localhost:5000/glpi"


def validate_payload(payload):
    """
    Validate payload structure before processing.

    Args:
        payload: Dict containing the alert payload

    Returns:
        tuple: (valid: bool, error_message: str or None)
    """
    if not isinstance(payload, dict):
        return False, "Payload must be a JSON object"

    if "alerts" not in payload:
        return False, "Missing 'alerts' array in payload"

    if not isinstance(payload["alerts"], list):
        return False, "'alerts' must be an array"

    if len(payload["alerts"]) == 0:
        return False, "'alerts' array is empty"

    for idx, alert in enumerate(payload["alerts"]):
        if not isinstance(alert, dict):
            return False, f"Alert {idx} must be an object"

        if "startsAt" not in alert:
            return False, f"Missing 'startsAt' in alert {idx}"

        if "labels" not in alert:
            return False, f"Missing 'labels' in alert {idx}"

        # Validate startsAt format
        try:
            datetime.fromisoformat(alert["startsAt"].replace("Z", "+00:00"))
        except (ValueError, AttributeError):
            return False, (
                f"Invalid startsAt timestamp in alert {idx}\n"
                f"Expected ISO 8601 format (e.g., 2025-10-16T10:00:00Z)"
            )

    return True, None


def update_timestamps(payload, mode):
    """
    Update timestamps in payload based on mode.

    Guarantees unique startsAt on every CLI run by using current time
    with microsecond precision. Preserves time offsets between alerts.

    Args:
        payload: Dict containing the alert payload
        mode: 'fire' or 'resolve'

    Returns:
        Dict: Modified payload with updated timestamps
    """
    modified = deepcopy(payload)
    now = datetime.now(timezone.utc)

    # Parse all original startsAt timestamps
    original_times = []
    for alert in payload["alerts"]:
        starts_at_str = alert["startsAt"].replace("Z", "+00:00")
        starts_at = datetime.fromisoformat(starts_at_str)
        original_times.append(starts_at)

    # Find earliest time and calculate offsets
    earliest = min(original_times)
    offsets = [(t - earliest).total_seconds() for t in original_times]

    # Update each alert
    for idx, alert in enumerate(modified["alerts"]):
        # Apply offset to current time
        new_starts_at = now.timestamp() + offsets[idx]
        new_starts_at_dt = datetime.fromtimestamp(new_starts_at, tz=timezone.utc)

        # Format as ISO 8601 with microseconds
        alert["startsAt"] = new_starts_at_dt.strftime("%Y-%m-%dT%H:%M:%S.%fZ")

        if mode == "fire":
            alert["status"] = "firing"
            alert["endsAt"] = "0001-01-01T00:00:00Z"
        elif mode == "resolve":
            alert["status"] = "resolved"
            alert["endsAt"] = now.strftime("%Y-%m-%dT%H:%M:%S.%fZ")

    # Update top-level status for consistency
    modified["status"] = "firing" if mode == "fire" else "resolved"

    return modified


def send_request(payload, dry_run=False, timeout=60):
    """
    Send HTTP POST request to webhook endpoint.

    Args:
        payload: Dict containing the alert payload
        dry_run: If True, only print payload without sending
        timeout: Request timeout in seconds (default: 60)

    Returns:
        tuple: (success: bool, problem_id: str or None)
    """
    payload_json = json.dumps(payload, indent=2)

    if dry_run:
        print(f"[DRY RUN] Would send to {ENDPOINT}")
        print("\nPayload preview:")
        print(payload_json)
        return True, None

    try:
        # Prepare request
        data = payload_json.encode("utf-8")
        req = Request(
            ENDPOINT,
            data=data,
            headers={"Content-Type": "application/json"}
        )

        # Send request
        with urlopen(req, timeout=timeout) as response:
            status_code = response.getcode()
            response_body = response.read().decode("utf-8")

            print(f"Sent to {ENDPOINT}")
            print(f"HTTP Status: {status_code} OK")
            print(f"Response: {response_body}")

            # Try to extract problem_id from response
            problem_id = None
            try:
                response_json = json.loads(response_body)
                problem_id = response_json.get("problem_id")
            except (json.JSONDecodeError, AttributeError):
                pass

            return True, problem_id

    except HTTPError as e:
        error_body = e.read().decode("utf-8") if e.fp else "No response body"
        print(f"Error: HTTP {e.code} {e.reason}", file=sys.stderr)
        print(f"Response: {error_body}", file=sys.stderr)
        return False, None

    except URLError as e:
        print(f"Error: Could not connect to {ENDPOINT}", file=sys.stderr)
        print(f"Reason: {e.reason}", file=sys.stderr)
        print("\nIs the Flask application running? Try: python app.py", file=sys.stderr)
        return False, None

    except Exception as e:
        print(f"Error: {type(e).__name__}: {e}", file=sys.stderr)
        return False, None


def fire_alert(file_path, dry_run, timeout):
    """Handle fire command."""
    try:
        with open(file_path, "r") as f:
            payload = json.load(f)
    except FileNotFoundError:
        print(f"Error: Payload file not found: {file_path}", file=sys.stderr)
        return False
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in {file_path}", file=sys.stderr)
        print(f"JSONDecodeError: {e}", file=sys.stderr)
        return False

    # Validate payload
    valid, error_msg = validate_payload(payload)
    if not valid:
        print(f"Error: Invalid payload structure", file=sys.stderr)
        print(error_msg, file=sys.stderr)
        return False

    # Generate fingerprint for session tracking
    fingerprint = generate_fingerprint(payload)

    # Get current timestamp in ISO 8601
    now = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

    # Update timestamps for firing
    modified_payload = update_timestamps(payload, mode="fire")

    # Send request
    success, problem_id = send_request(modified_payload, dry_run=dry_run, timeout=timeout)

    if success and not dry_run:
        # Save session for later resolve
        try:
            sessions_file = get_sessions_file()
            sessions = load_sessions(sessions_file)
            new_session = create_session(
                payload_file=file_path,
                fingerprint=fingerprint,
                problem_id=problem_id,
                timestamp=now,
            )
            sessions["sessions"].append(new_session)
            save_sessions(sessions_file, sessions)
            print(f"\nSession saved: {new_session['id']}")
        except Exception as e:
            print(f"Warning: Could not save session: {e}", file=sys.stderr)

    return success


def resolve_alert(
    file_path=None,
    dry_run=False,
    timeout=60,
    session_id=None,
    list_sessions=False,
    clear_resolved=False,
):
    """Handle resolve command."""

    # Handle --clear-resolved flag
    if clear_resolved:
        try:
            sessions_file = get_sessions_file()
            deleted = delete_resolved_sessions(sessions_file)
            print(f"Deleted {deleted} resolved session(s)")
            return True
        except Exception as e:
            print(f"Error: Could not clear resolved sessions: {e}", file=sys.stderr)
            return False

    # Handle --session-id flag
    if session_id:
        try:
            sessions_file = get_sessions_file()
            session = get_session_by_id(sessions_file, session_id)
            payload_file = session["payload_file"]
        except ValueError as e:
            print(f"Error: {e}", file=sys.stderr)
            return False
    # Handle --list-sessions flag
    elif list_sessions:
        try:
            sessions_file = get_sessions_file()
            active = get_active_sessions(sessions_file)

            if not active:
                print("Error: No active sessions found. Run 'fire' first.", file=sys.stderr)
                return False

            # Display sessions
            print(format_session_display(active))

            # Get user selection
            selection = input("Select session number: ").strip()
            try:
                idx = int(selection) - 1
                if idx < 0 or idx >= len(active):
                    print(f"Error: Invalid selection", file=sys.stderr)
                    return False
                session_id = active[idx]["id"]
                session = active[idx]
                payload_file = session["payload_file"]
            except ValueError:
                print("Error: Please enter a valid number", file=sys.stderr)
                return False
        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)
            return False
    else:
        # Fallback to file_path (backward compatibility)
        if file_path:
            payload_file = file_path
        else:
            print(
                "Error: Use --session-id, --list-sessions, --clear-resolved, or --file",
                file=sys.stderr
            )
            return False

    # Load original payload from file
    try:
        with open(payload_file, "r") as f:
            payload = json.load(f)
    except FileNotFoundError:
        print(f"Error: Original payload file not found: {payload_file}", file=sys.stderr)
        return False
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in {payload_file}", file=sys.stderr)
        print(f"JSONDecodeError: {e}", file=sys.stderr)
        return False

    # Validate payload
    valid, error_msg = validate_payload(payload)
    if not valid:
        print(f"Error: Invalid payload structure", file=sys.stderr)
        print(error_msg, file=sys.stderr)
        return False

    # Update timestamps for resolution
    modified_payload = update_timestamps(payload, mode="resolve")

    # Send request
    success, _ = send_request(modified_payload, dry_run=dry_run, timeout=timeout)

    # Update session status if successful and not dry-run
    if success and not dry_run and session_id:
        try:
            sessions_file = get_sessions_file()
            update_session_status(sessions_file, session_id, "resolved")
            print(f"Session marked as resolved: {session_id}")
        except Exception as e:
            print(f"Warning: Could not update session status: {e}", file=sys.stderr)

    return success


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Send alert payloads to webhooks-alertmanager",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python cli/send.py fire
  python cli/send.py resolve --file custom_payload.json
  python cli/send.py fire --dry-run
        """
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    # Fire command
    fire_parser = subparsers.add_parser(
        "fire",
        help="Send firing alert"
    )
    fire_parser.add_argument(
        "--file", "-f",
        default="request_payload.json",
        help="Path to JSON payload file (default: request_payload.json)"
    )
    fire_parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview request without sending"
    )
    fire_parser.add_argument(
        "--timeout", "-t",
        type=int,
        default=60,
        help="Request timeout in seconds (default: 60)"
    )

    # Resolve command
    resolve_parser = subparsers.add_parser(
        "resolve",
        help="Send resolved alert"
    )
    resolve_parser.add_argument(
        "--file", "-f",
        default="request_payload.json",
        help="Path to JSON payload file (default: request_payload.json, ignored if --session-id used)"
    )
    resolve_parser.add_argument(
        "--session-id",
        help="Use specific saved session (e.g., fire_20251030_153045_abc123)"
    )
    resolve_parser.add_argument(
        "--list-sessions",
        action="store_true",
        help="List active sessions and select one interactively"
    )
    resolve_parser.add_argument(
        "--clear-resolved",
        action="store_true",
        help="Delete all resolved sessions"
    )
    resolve_parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview request without sending"
    )
    resolve_parser.add_argument(
        "--timeout", "-t",
        type=int,
        default=60,
        help="Request timeout in seconds (default: 60)"
    )

    args = parser.parse_args()

    # Execute command
    if args.command == "fire":
        success = fire_alert(args.file, args.dry_run, args.timeout)
    elif args.command == "resolve":
        success = resolve_alert(
            file_path=args.file,
            dry_run=args.dry_run,
            timeout=args.timeout,
            session_id=args.session_id,
            list_sessions=args.list_sessions,
            clear_resolved=args.clear_resolved,
        )
    else:
        parser.print_help()
        sys.exit(1)

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
