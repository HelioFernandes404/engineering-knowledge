"""Tests for CLI send.py fire/resolve functionality."""

import json
import pytest
import tempfile
from pathlib import Path
from unittest.mock import patch, MagicMock
from cli.send import fire_alert, send_request
from cli.session_manager import load_sessions
from cli.utils import generate_fingerprint


def test_fire_alert_saves_session_on_success(tmp_path):
    """Test that fire_alert saves a session after successful send."""
    # Setup payload file
    payload_file = tmp_path / "test_payload.json"
    payload = {
        "alerts": [
            {
                "startsAt": "2025-10-30T10:00:00Z",
                "labels": {"alertname": "TestAlert"},
            }
        ]
    }
    payload_file.write_text(json.dumps(payload))

    # Mock sessions file in tmp_path
    sessions_file = tmp_path / ".cli-sessions.json"

    # Mock the send_request to return a problem_id
    with patch("cli.send.send_request") as mock_send:
        mock_send.return_value = (True, "12345")  # success, problem_id

        # Mock session_manager to use our tmp sessions file
        with patch("cli.send.get_sessions_file") as mock_get_file:
            mock_get_file.return_value = sessions_file

            success = fire_alert(str(payload_file), dry_run=False, timeout=60)

    assert success

    # Verify session was saved
    sessions = load_sessions(sessions_file)
    assert len(sessions["sessions"]) == 1
    session = sessions["sessions"][0]
    assert session["status"] == "active"
    assert session["problem_id"] == "12345"
    assert "payload_file" in session
    assert "fingerprint" in session


def test_fire_alert_handles_missing_problem_id(tmp_path):
    """Test that fire_alert saves session even if problem_id is None."""
    payload_file = tmp_path / "test_payload.json"
    payload = {
        "alerts": [
            {
                "startsAt": "2025-10-30T10:00:00Z",
                "labels": {"alertname": "TestAlert"},
            }
        ]
    }
    payload_file.write_text(json.dumps(payload))

    sessions_file = tmp_path / ".cli-sessions.json"

    # Mock send_request to return None problem_id
    with patch("cli.send.send_request") as mock_send:
        mock_send.return_value = (True, None)  # success but no problem_id

        with patch("cli.send.get_sessions_file") as mock_get_file:
            mock_get_file.return_value = sessions_file

            success = fire_alert(str(payload_file), dry_run=False, timeout=60)

    assert success

    sessions = load_sessions(sessions_file)
    assert len(sessions["sessions"]) == 1
    assert sessions["sessions"][0]["problem_id"] is None


def test_fire_alert_does_not_save_session_on_dry_run(tmp_path):
    """Test that fire_alert does not save session when dry_run is True."""
    payload_file = tmp_path / "test_payload.json"
    payload = {
        "alerts": [
            {
                "startsAt": "2025-10-30T10:00:00Z",
                "labels": {"alertname": "TestAlert"},
            }
        ]
    }
    payload_file.write_text(json.dumps(payload))

    sessions_file = tmp_path / ".cli-sessions.json"

    with patch("cli.send.send_request") as mock_send:
        mock_send.return_value = (True, None)

        with patch("cli.send.get_sessions_file") as mock_get_file:
            mock_get_file.return_value = sessions_file

            success = fire_alert(str(payload_file), dry_run=True, timeout=60)

    assert success

    # Verify no session was saved (dry run mode)
    # The file shouldn't exist or should be empty
    if sessions_file.exists():
        sessions = load_sessions(sessions_file)
        assert len(sessions["sessions"]) == 0


def test_send_request_returns_tuple_with_problem_id():
    """Test that send_request returns (success, problem_id) tuple."""
    payload = {
        "alerts": [
            {
                "startsAt": "2025-10-30T10:00:00Z",
                "labels": {"alertname": "TestAlert"},
            }
        ]
    }

    # Mock successful response with problem_id
    mock_response = MagicMock()
    mock_response.getcode.return_value = 200
    mock_response.read.return_value = json.dumps({"problem_id": "12345"}).encode("utf-8")
    mock_response.__enter__ = MagicMock(return_value=mock_response)
    mock_response.__exit__ = MagicMock(return_value=False)

    with patch("cli.send.urlopen", return_value=mock_response):
        success, problem_id = send_request(payload, dry_run=False, timeout=60)

    assert success is True
    assert problem_id == "12345"


def test_send_request_dry_run_returns_none_problem_id():
    """Test that send_request returns None problem_id in dry_run mode."""
    payload = {"alerts": [{"startsAt": "2025-10-30T10:00:00Z", "labels": {"alertname": "TestAlert"}}]}

    success, problem_id = send_request(payload, dry_run=True, timeout=60)

    assert success is True
    assert problem_id is None


def test_generate_fingerprint_matches_production_bug():
    """Test that fingerprint generation matches production behavior.

    Production code (webhook_glpi/scripts/glpi.py:245) has a bug where it
    extracts alertname from alert.get('alertname') instead of
    alert.get('labels', {}).get('alertname'). This test verifies the CLI
    replicates the same behavior for compatibility with existing GLPI problems.

    When alertname is missing from the root level (which is always the case
    in real Alertmanager payloads), the fingerprint should be generated with
    "None" as the alert_name component, matching the production bug.
    """
    # Real Alertmanager payload structure (alertname in labels, not root)
    payload = {
        "alerts": [
            {
                "fingerprint": "abc123",
                "startsAt": "2025-10-30T10:00:00Z",
                "generatorURL": "http://prometheus:9090/graph",
                "labels": {"alertname": "HighCPU"},
            }
        ]
    }

    fingerprint = generate_fingerprint(payload)

    # The fingerprint should be generated with "None" for alert_name
    # because alert.get('alertname') returns None (production bug behavior)
    import hashlib
    expected_source = "None|abc123|2025-10-30T10:00:00Z|http://prometheus:9090/graph"
    expected_fingerprint = hashlib.sha256(expected_source.encode("utf-8")).hexdigest()

    assert fingerprint == expected_fingerprint, (
        f"CLI fingerprint should match production bug behavior. "
        f"Expected alert_name='None' in fingerprint source, got fingerprint={fingerprint}"
    )


def test_resolve_alert_with_session_id(tmp_path):
    """Test that resolve uses correct session when --session-id provided."""
    from cli.send import resolve_alert

    # Create a session first
    sessions_file = tmp_path / ".cli-sessions.json"
    original_payload_file = tmp_path / "original.json"
    payload = {
        "alerts": [
            {
                "startsAt": "2025-10-30T10:00:00Z",
                "labels": {"alertname": "TestAlert"},
            }
        ]
    }
    original_payload_file.write_text(json.dumps(payload))

    sessions_data = {
        "sessions": [
            {
                "id": "fire_20251030_153045_abc123",
                "timestamp": "2025-10-30T15:30:45Z",
                "payload_file": str(original_payload_file),
                "fingerprint": "abc123",
                "problem_id": "12345",
                "status": "active",
            }
        ]
    }
    sessions_file.write_text(json.dumps(sessions_data))

    # Mock send_request
    with patch("cli.send.send_request") as mock_send:
        mock_send.return_value = (True, None)

        with patch("cli.send.get_sessions_file") as mock_get_file:
            mock_get_file.return_value = sessions_file

            success = resolve_alert(
                file_path=None,  # Not used when session_id provided
                dry_run=False,
                timeout=60,
                session_id="fire_20251030_153045_abc123",
            )

    assert success

    # Verify session status was updated to resolved
    sessions = load_sessions(sessions_file)
    resolved_session = sessions["sessions"][0]
    assert resolved_session["status"] == "resolved"


def test_resolve_alert_with_list_sessions_interactive(tmp_path, monkeypatch):
    """Test that resolve lists sessions when --list-sessions provided."""
    from cli.send import resolve_alert

    sessions_file = tmp_path / ".cli-sessions.json"
    original_payload_file = tmp_path / "original.json"
    payload = {
        "alerts": [
            {
                "startsAt": "2025-10-30T10:00:00Z",
                "labels": {"alertname": "TestAlert"},
            }
        ]
    }
    original_payload_file.write_text(json.dumps(payload))

    sessions_data = {
        "sessions": [
            {
                "id": "fire_20251030_153045_abc123",
                "timestamp": "2025-10-30T15:30:45Z",
                "payload_file": str(original_payload_file),
                "fingerprint": "abc123",
                "problem_id": "12345",
                "status": "active",
            }
        ]
    }
    sessions_file.write_text(json.dumps(sessions_data))

    # Mock user selecting session [1]
    monkeypatch.setattr("builtins.input", lambda _: "1")

    with patch("cli.send.send_request") as mock_send:
        mock_send.return_value = (True, None)

        with patch("cli.send.get_sessions_file") as mock_get_file:
            mock_get_file.return_value = sessions_file

            success = resolve_alert(
                file_path=None,
                dry_run=False,
                timeout=60,
                session_id=None,
                list_sessions=True,
            )

    assert success


def test_resolve_alert_no_active_sessions(tmp_path):
    """Test that resolve fails if no active sessions found."""
    from cli.send import resolve_alert

    sessions_file = tmp_path / ".cli-sessions.json"
    sessions_data = {"sessions": []}
    sessions_file.write_text(json.dumps(sessions_data))

    with patch("cli.send.get_sessions_file") as mock_get_file:
        mock_get_file.return_value = sessions_file

        success = resolve_alert(
            file_path=None,
            dry_run=False,
            timeout=60,
            session_id=None,
            list_sessions=True,
        )

    assert not success


def test_resolve_alert_with_clear_resolved(tmp_path):
    """Test that resolve --clear-resolved deletes resolved sessions."""
    from cli.send import resolve_alert

    sessions_file = tmp_path / ".cli-sessions.json"
    sessions_data = {
        "sessions": [
            {"id": "fire_1", "status": "active"},
            {"id": "fire_2", "status": "resolved"},
            {"id": "fire_3", "status": "resolved"},
        ]
    }
    sessions_file.write_text(json.dumps(sessions_data))

    with patch("cli.send.get_sessions_file") as mock_get_file:
        mock_get_file.return_value = sessions_file

        success = resolve_alert(
            file_path=None,
            dry_run=False,
            timeout=60,
            session_id=None,
            list_sessions=False,
            clear_resolved=True,
        )

    assert success

    # Verify resolved sessions were deleted
    sessions = load_sessions(sessions_file)
    assert len(sessions["sessions"]) == 1
    assert sessions["sessions"][0]["id"] == "fire_1"
