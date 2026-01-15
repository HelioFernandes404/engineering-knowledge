"""Session management for CLI fire/resolve workflow."""

import json
from pathlib import Path
from datetime import datetime, timezone
from typing import Dict, List, Optional


DEFAULT_SESSIONS_FILE = ".cli-sessions.json"


def get_sessions_file(custom_path: Optional[str] = None) -> Path:
    """Get the sessions file path."""
    if custom_path:
        return Path(custom_path)
    return Path(DEFAULT_SESSIONS_FILE)


def load_sessions(sessions_file: Path) -> Dict:
    """
    Load sessions from file. Creates empty file if missing.

    Args:
        sessions_file: Path to .cli-sessions.json

    Returns:
        Dict with "sessions" key containing list of session dicts

    Raises:
        ValueError: If file contains invalid data structure
    """
    sessions_file = Path(sessions_file)

    if not sessions_file.exists():
        data = {"sessions": []}
        sessions_file.write_text(json.dumps(data, indent=2))
        return data

    data = json.loads(sessions_file.read_text())

    # Validate data structure
    if not isinstance(data, dict):
        raise ValueError(
            f"Invalid sessions file format: expected dict, got {type(data).__name__}"
        )

    if "sessions" not in data:
        raise ValueError(
            'Invalid sessions file format: missing required "sessions" key'
        )

    if not isinstance(data["sessions"], list):
        raise ValueError(
            f'Invalid sessions file format: "sessions" must be a list, got {type(data["sessions"]).__name__}'
        )

    return data


def save_sessions(sessions_file: Path, data: Dict) -> None:
    """
    Save sessions to file.

    Args:
        sessions_file: Path to .cli-sessions.json
        data: Dict with "sessions" key
    """
    Path(sessions_file).write_text(json.dumps(data, indent=2))


def create_session(
    payload_file: str,
    fingerprint: str,
    problem_id: Optional[str],
    timestamp: str,
) -> Dict:
    """
    Create a new session dict.

    Args:
        payload_file: Relative path to original payload JSON
        fingerprint: SHA256 fingerprint of payload
        problem_id: GLPI problem ID (can be None)
        timestamp: ISO 8601 timestamp

    Returns:
        Session dict ready to add to sessions list
    """
    # Generate session ID from timestamp and fingerprint prefix
    ts_clean = timestamp.replace(":", "").replace("-", "").replace("T", "_").split(".")[0]
    fp_prefix = fingerprint[:6] if fingerprint else "unknown"
    session_id = f"fire_{ts_clean}_{fp_prefix}"

    return {
        "id": session_id,
        "timestamp": timestamp,
        "payload_file": payload_file,
        "fingerprint": fingerprint,
        "problem_id": problem_id,
        "status": "active",
    }


def get_active_sessions(sessions_file: Path) -> List[Dict]:
    """
    Get all active (unresolved) sessions.

    Args:
        sessions_file: Path to .cli-sessions.json

    Returns:
        List of session dicts with status == "active"
    """
    sessions = load_sessions(sessions_file)
    return [s for s in sessions["sessions"] if s.get("status") == "active"]


def get_session_by_id(sessions_file: Path, session_id: str) -> Dict:
    """
    Get a specific session by ID.

    Args:
        sessions_file: Path to .cli-sessions.json
        session_id: The session ID to look up

    Returns:
        Session dict

    Raises:
        ValueError: If session not found
    """
    sessions = load_sessions(sessions_file)
    for session in sessions["sessions"]:
        if session["id"] == session_id:
            return session

    raise ValueError(f"Session not found: {session_id}")


def update_session_status(
    sessions_file: Path,
    session_id: str,
    new_status: str,
) -> None:
    """
    Update a session's status.

    Args:
        sessions_file: Path to .cli-sessions.json
        session_id: The session ID to update
        new_status: New status value (e.g., "resolved")

    Raises:
        ValueError: If session not found
    """
    sessions = load_sessions(sessions_file)

    for session in sessions["sessions"]:
        if session["id"] == session_id:
            session["status"] = new_status
            save_sessions(sessions_file, sessions)
            return

    raise ValueError(f"Session not found: {session_id}")


def delete_resolved_sessions(sessions_file: Path) -> int:
    """
    Delete all resolved sessions.

    Args:
        sessions_file: Path to .cli-sessions.json

    Returns:
        Number of sessions deleted
    """
    sessions = load_sessions(sessions_file)
    original_count = len(sessions["sessions"])

    sessions["sessions"] = [
        s for s in sessions["sessions"]
        if s.get("status") != "resolved"
    ]

    deleted = original_count - len(sessions["sessions"])
    save_sessions(sessions_file, sessions)

    return deleted


def format_session_display(sessions: List[Dict]) -> str:
    """
    Format sessions for CLI display.

    Args:
        sessions: List of session dicts

    Returns:
        Formatted string for display
    """
    if not sessions:
        return "No active sessions found."

    lines = ["Available sessions:\n"]
    for idx, session in enumerate(sessions, 1):
        ts = session.get("timestamp", "unknown")
        fp = session.get("fingerprint", "unknown")[:8]
        pid = session.get("problem_id", "N/A")
        file = session.get("payload_file", "unknown")

        lines.append(
            f"[{idx}] {session['id']}\n"
            f"    Timestamp: {ts}\n"
            f"    File: {file}\n"
            f"    Problem ID: {pid}\n"
            f"    Fingerprint: {fp}...\n"
        )

    return "".join(lines)
