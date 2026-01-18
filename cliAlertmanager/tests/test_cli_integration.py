"""Integration tests for CLI fire/resolve session workflow.

These tests verify the end-to-end flow:
1. fire command creates a valid session
2. resolve command with --session-id finds and uses that session
3. --list-sessions shows correct sessions
4. --clear-resolved removes only resolved sessions
"""

import json
import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock
from cli.send import fire_alert, resolve_alert
from cli.session_manager import load_sessions, get_active_sessions


class TestFireResolveIntegration:
    """Integration tests for fire/resolve workflow."""

    def test_fire_then_resolve_with_session_id(self, tmp_path):
        """Test complete workflow: fire alert -> resolve using session ID."""
        # Setup payload file
        payload_file = tmp_path / "alert_payload.json"
        payload = {
            "alerts": [
                {
                    "fingerprint": "abc123def456",
                    "startsAt": "2025-10-30T10:00:00Z",
                    "generatorURL": "http://prometheus:9090/graph",
                    "labels": {
                        "alertname": "HighCPU",
                        "severity": "critical",
                        "instance": "server-01"
                    },
                    "annotations": {
                        "description": "CPU usage above 90%"
                    }
                }
            ]
        }
        payload_file.write_text(json.dumps(payload))

        sessions_file = tmp_path / ".cli-sessions.json"

        # Step 1: Fire the alert (creates session)
        with patch("cli.send.send_request") as mock_send:
            mock_send.return_value = (True, "12345")  # success with problem_id

            with patch("cli.send.get_sessions_file") as mock_get_file:
                mock_get_file.return_value = sessions_file

                fire_success = fire_alert(str(payload_file), dry_run=False, timeout=60)

        # Verify fire succeeded
        assert fire_success is True

        # Verify session was created
        sessions = load_sessions(sessions_file)
        assert len(sessions["sessions"]) == 1
        session = sessions["sessions"][0]
        assert session["status"] == "active"
        assert session["problem_id"] == "12345"
        assert session["payload_file"] == str(payload_file)
        assert "fingerprint" in session
        assert "id" in session

        session_id = session["id"]

        # Step 2: Resolve using the session ID
        with patch("cli.send.send_request") as mock_send:
            mock_send.return_value = (True, None)  # success, no problem_id on resolve

            with patch("cli.send.get_sessions_file") as mock_get_file:
                mock_get_file.return_value = sessions_file

                resolve_success = resolve_alert(
                    file_path=None,
                    dry_run=False,
                    timeout=60,
                    session_id=session_id,
                )

        # Verify resolve succeeded
        assert resolve_success is True

        # Verify session status was updated
        sessions = load_sessions(sessions_file)
        assert len(sessions["sessions"]) == 1
        assert sessions["sessions"][0]["status"] == "resolved"
        assert sessions["sessions"][0]["id"] == session_id

    def test_fire_multiple_then_resolve_specific_session(self, tmp_path):
        """Test firing multiple alerts and resolving a specific one."""
        sessions_file = tmp_path / ".cli-sessions.json"

        # Create two different payloads
        payload1_file = tmp_path / "alert1.json"
        payload1 = {
            "alerts": [{
                "fingerprint": "aaa111",
                "startsAt": "2025-10-30T10:00:00Z",
                "generatorURL": "http://prometheus:9090/graph",
                "labels": {"alertname": "Alert1", "severity": "warning"}
            }]
        }
        payload1_file.write_text(json.dumps(payload1))

        payload2_file = tmp_path / "alert2.json"
        payload2 = {
            "alerts": [{
                "fingerprint": "bbb222",
                "startsAt": "2025-10-30T11:00:00Z",
                "generatorURL": "http://prometheus:9090/graph",
                "labels": {"alertname": "Alert2", "severity": "critical"}
            }]
        }
        payload2_file.write_text(json.dumps(payload2))

        # Fire first alert
        with patch("cli.send.send_request") as mock_send, \
             patch("cli.send.get_sessions_file") as mock_get_file:
            mock_send.return_value = (True, "100")
            mock_get_file.return_value = sessions_file
            fire_alert(str(payload1_file), dry_run=False, timeout=60)

        # Fire second alert
        with patch("cli.send.send_request") as mock_send, \
             patch("cli.send.get_sessions_file") as mock_get_file:
            mock_send.return_value = (True, "200")
            mock_get_file.return_value = sessions_file
            fire_alert(str(payload2_file), dry_run=False, timeout=60)

        # Verify both sessions exist
        sessions = load_sessions(sessions_file)
        assert len(sessions["sessions"]) == 2
        assert all(s["status"] == "active" for s in sessions["sessions"])

        # Get first session ID
        session1_id = sessions["sessions"][0]["id"]

        # Resolve only the first alert
        with patch("cli.send.send_request") as mock_send, \
             patch("cli.send.get_sessions_file") as mock_get_file:
            mock_send.return_value = (True, None)
            mock_get_file.return_value = sessions_file
            resolve_alert(
                file_path=None,
                dry_run=False,
                timeout=60,
                session_id=session1_id,
            )

        # Verify only first session is resolved
        sessions = load_sessions(sessions_file)
        assert len(sessions["sessions"]) == 2
        assert sessions["sessions"][0]["status"] == "resolved"
        assert sessions["sessions"][1]["status"] == "active"

    def test_list_sessions_shows_correct_active_sessions(self, tmp_path, monkeypatch):
        """Test --list-sessions displays only active sessions in correct format."""
        sessions_file = tmp_path / ".cli-sessions.json"
        payload_file = tmp_path / "test.json"
        payload = {
            "alerts": [{
                "startsAt": "2025-10-30T10:00:00Z",
                "labels": {"alertname": "TestAlert"}
            }]
        }
        payload_file.write_text(json.dumps(payload))

        # Pre-create sessions with different statuses
        sessions_data = {
            "sessions": [
                {
                    "id": "fire_20251030_100000_abc123",
                    "timestamp": "2025-10-30T10:00:00Z",
                    "payload_file": str(payload_file),
                    "fingerprint": "abc123def456",
                    "problem_id": "100",
                    "status": "active",
                },
                {
                    "id": "fire_20251030_110000_def456",
                    "timestamp": "2025-10-30T11:00:00Z",
                    "payload_file": str(payload_file),
                    "fingerprint": "def456ghi789",
                    "problem_id": "200",
                    "status": "resolved",  # Should not appear in list
                },
                {
                    "id": "fire_20251030_120000_ghi789",
                    "timestamp": "2025-10-30T12:00:00Z",
                    "payload_file": str(payload_file),
                    "fingerprint": "ghi789jkl012",
                    "problem_id": "300",
                    "status": "active",
                }
            ]
        }
        sessions_file.write_text(json.dumps(sessions_data))

        # Mock user selecting first active session (index 1)
        monkeypatch.setattr("builtins.input", lambda _: "1")

        # Capture output to verify display format
        displayed_sessions = []

        with patch("cli.send.send_request") as mock_send, \
             patch("cli.send.get_sessions_file") as mock_get_file, \
             patch("cli.send.format_session_display") as mock_format:
            mock_send.return_value = (True, None)
            mock_get_file.return_value = sessions_file

            # Capture what gets passed to format_session_display
            def capture_display(sessions):
                displayed_sessions.extend(sessions)
                # Return a realistic formatted string
                return f"Available sessions:\n\n[1] {sessions[0]['id']}\n"

            mock_format.side_effect = capture_display

            resolve_alert(
                file_path=None,
                dry_run=False,
                timeout=60,
                session_id=None,
                list_sessions=True,
            )

        # Verify only active sessions were displayed
        assert len(displayed_sessions) == 2
        assert all(s["status"] == "active" for s in displayed_sessions)
        assert displayed_sessions[0]["id"] == "fire_20251030_100000_abc123"
        assert displayed_sessions[1]["id"] == "fire_20251030_120000_ghi789"

        # Verify the resolved session was NOT in the list
        assert not any(s["id"] == "fire_20251030_110000_def456" for s in displayed_sessions)

    def test_clear_resolved_removes_only_resolved_sessions(self, tmp_path):
        """Test --clear-resolved removes resolved sessions but keeps active ones."""
        sessions_file = tmp_path / ".cli-sessions.json"

        # Create mix of active and resolved sessions
        sessions_data = {
            "sessions": [
                {
                    "id": "fire_1",
                    "timestamp": "2025-10-30T10:00:00Z",
                    "payload_file": "test1.json",
                    "fingerprint": "aaa",
                    "problem_id": "100",
                    "status": "active",
                },
                {
                    "id": "fire_2",
                    "timestamp": "2025-10-30T11:00:00Z",
                    "payload_file": "test2.json",
                    "fingerprint": "bbb",
                    "problem_id": "200",
                    "status": "resolved",
                },
                {
                    "id": "fire_3",
                    "timestamp": "2025-10-30T12:00:00Z",
                    "payload_file": "test3.json",
                    "fingerprint": "ccc",
                    "problem_id": "300",
                    "status": "resolved",
                },
                {
                    "id": "fire_4",
                    "timestamp": "2025-10-30T13:00:00Z",
                    "payload_file": "test4.json",
                    "fingerprint": "ddd",
                    "problem_id": "400",
                    "status": "active",
                }
            ]
        }
        sessions_file.write_text(json.dumps(sessions_data))

        # Run clear-resolved
        with patch("cli.send.get_sessions_file") as mock_get_file:
            mock_get_file.return_value = sessions_file

            success = resolve_alert(
                file_path=None,
                dry_run=False,
                timeout=60,
                clear_resolved=True,
            )

        assert success is True

        # Verify only active sessions remain
        sessions = load_sessions(sessions_file)
        assert len(sessions["sessions"]) == 2
        assert all(s["status"] == "active" for s in sessions["sessions"])
        assert sessions["sessions"][0]["id"] == "fire_1"
        assert sessions["sessions"][1]["id"] == "fire_4"

    def test_fire_with_dry_run_does_not_create_session(self, tmp_path):
        """Test that fire --dry-run does not create a session."""
        payload_file = tmp_path / "test.json"
        payload = {
            "alerts": [{
                "startsAt": "2025-10-30T10:00:00Z",
                "labels": {"alertname": "TestAlert"}
            }]
        }
        payload_file.write_text(json.dumps(payload))

        sessions_file = tmp_path / ".cli-sessions.json"

        with patch("cli.send.send_request") as mock_send, \
             patch("cli.send.get_sessions_file") as mock_get_file:
            mock_send.return_value = (True, None)  # Dry run returns success
            mock_get_file.return_value = sessions_file

            success = fire_alert(str(payload_file), dry_run=True, timeout=60)

        assert success is True

        # Verify no session was created
        if sessions_file.exists():
            sessions = load_sessions(sessions_file)
            assert len(sessions["sessions"]) == 0

    def test_resolve_with_invalid_session_id_fails(self, tmp_path):
        """Test that resolve with non-existent session ID fails gracefully."""
        sessions_file = tmp_path / ".cli-sessions.json"
        sessions_data = {"sessions": []}
        sessions_file.write_text(json.dumps(sessions_data))

        with patch("cli.send.get_sessions_file") as mock_get_file:
            mock_get_file.return_value = sessions_file

            success = resolve_alert(
                file_path=None,
                dry_run=False,
                timeout=60,
                session_id="fire_nonexistent_12345",
            )

        assert success is False

    def test_resolve_preserves_original_payload_data(self, tmp_path):
        """Test that resolve uses the exact original payload from fire."""
        payload_file = tmp_path / "original.json"
        original_payload = {
            "alerts": [{
                "fingerprint": "original123",
                "startsAt": "2025-10-30T10:00:00Z",
                "generatorURL": "http://prometheus:9090/original",
                "labels": {
                    "alertname": "OriginalAlert",
                    "severity": "critical",
                    "custom_label": "important_value"
                }
            }]
        }
        payload_file.write_text(json.dumps(original_payload))

        sessions_file = tmp_path / ".cli-sessions.json"

        # Fire the alert
        with patch("cli.send.send_request") as mock_send, \
             patch("cli.send.get_sessions_file") as mock_get_file:
            mock_send.return_value = (True, "999")
            mock_get_file.return_value = sessions_file
            fire_alert(str(payload_file), dry_run=False, timeout=60)

        sessions = load_sessions(sessions_file)
        session_id = sessions["sessions"][0]["id"]

        # Track what payload gets sent to resolve
        sent_payload = None

        def capture_payload(payload, dry_run, timeout):
            nonlocal sent_payload
            sent_payload = payload
            return True, None

        # Resolve the alert
        with patch("cli.send.send_request") as mock_send, \
             patch("cli.send.get_sessions_file") as mock_get_file:
            mock_send.side_effect = capture_payload
            mock_get_file.return_value = sessions_file
            resolve_alert(
                file_path=None,
                dry_run=False,
                timeout=60,
                session_id=session_id,
            )

        # Verify the sent payload has the original labels
        assert sent_payload is not None
        assert sent_payload["alerts"][0]["labels"]["alertname"] == "OriginalAlert"
        assert sent_payload["alerts"][0]["labels"]["custom_label"] == "important_value"
        # Status should be updated to resolved
        assert sent_payload["status"] == "resolved"
        assert sent_payload["alerts"][0]["status"] == "resolved"

    def test_session_file_survives_multiple_operations(self, tmp_path):
        """Test that session file maintains integrity across multiple fire/resolve cycles."""
        sessions_file = tmp_path / ".cli-sessions.json"

        payload1_file = tmp_path / "alert1.json"
        payload1 = {
            "alerts": [{
                "startsAt": "2025-10-30T10:00:00Z",
                "labels": {"alertname": "Alert1"}
            }]
        }
        payload1_file.write_text(json.dumps(payload1))

        payload2_file = tmp_path / "alert2.json"
        payload2 = {
            "alerts": [{
                "startsAt": "2025-10-30T11:00:00Z",
                "labels": {"alertname": "Alert2"}
            }]
        }
        payload2_file.write_text(json.dumps(payload2))

        # Fire alert 1
        with patch("cli.send.send_request") as mock_send, \
             patch("cli.send.get_sessions_file") as mock_get_file:
            mock_send.return_value = (True, "100")
            mock_get_file.return_value = sessions_file
            fire_alert(str(payload1_file), dry_run=False, timeout=60)

        assert len(load_sessions(sessions_file)["sessions"]) == 1

        # Fire alert 2
        with patch("cli.send.send_request") as mock_send, \
             patch("cli.send.get_sessions_file") as mock_get_file:
            mock_send.return_value = (True, "200")
            mock_get_file.return_value = sessions_file
            fire_alert(str(payload2_file), dry_run=False, timeout=60)

        assert len(load_sessions(sessions_file)["sessions"]) == 2

        # Resolve alert 1
        session1_id = load_sessions(sessions_file)["sessions"][0]["id"]
        with patch("cli.send.send_request") as mock_send, \
             patch("cli.send.get_sessions_file") as mock_get_file:
            mock_send.return_value = (True, None)
            mock_get_file.return_value = sessions_file
            resolve_alert(session_id=session1_id, dry_run=False, timeout=60)

        # Check state: 1 resolved, 1 active
        sessions = load_sessions(sessions_file)
        assert len(sessions["sessions"]) == 2
        assert sessions["sessions"][0]["status"] == "resolved"
        assert sessions["sessions"][1]["status"] == "active"

        # Clear resolved sessions
        with patch("cli.send.get_sessions_file") as mock_get_file:
            mock_get_file.return_value = sessions_file
            resolve_alert(clear_resolved=True, dry_run=False, timeout=60)

        # Only 1 active session should remain
        sessions = load_sessions(sessions_file)
        assert len(sessions["sessions"]) == 1
        assert sessions["sessions"][0]["status"] == "active"
        assert sessions["sessions"][0]["problem_id"] == "200"  # Alert 2

    def test_interactive_session_selection_with_invalid_input(self, tmp_path, monkeypatch):
        """Test that invalid user input during session selection fails gracefully."""
        sessions_file = tmp_path / ".cli-sessions.json"
        payload_file = tmp_path / "test.json"
        payload = {
            "alerts": [{
                "startsAt": "2025-10-30T10:00:00Z",
                "labels": {"alertname": "TestAlert"}
            }]
        }
        payload_file.write_text(json.dumps(payload))

        sessions_data = {
            "sessions": [{
                "id": "fire_1",
                "timestamp": "2025-10-30T10:00:00Z",
                "payload_file": str(payload_file),
                "fingerprint": "abc123",
                "problem_id": "100",
                "status": "active",
            }]
        }
        sessions_file.write_text(json.dumps(sessions_data))

        # Test with out-of-range selection
        monkeypatch.setattr("builtins.input", lambda _: "99")

        with patch("cli.send.get_sessions_file") as mock_get_file:
            mock_get_file.return_value = sessions_file

            success = resolve_alert(
                file_path=None,
                dry_run=False,
                timeout=60,
                list_sessions=True,
            )

        assert success is False

    def test_fire_creates_sessions_for_same_payload(self, tmp_path):
        """Test that firing the same payload twice creates two separate sessions."""
        import time

        payload_file = tmp_path / "test.json"
        payload = {
            "alerts": [{
                "startsAt": "2025-10-30T10:00:00Z",
                "labels": {"alertname": "TestAlert"}
            }]
        }
        payload_file.write_text(json.dumps(payload))

        sessions_file = tmp_path / ".cli-sessions.json"

        # Fire the same payload twice with enough delay to get different second timestamps
        with patch("cli.send.send_request") as mock_send, \
             patch("cli.send.get_sessions_file") as mock_get_file:
            mock_send.return_value = (True, "123")
            mock_get_file.return_value = sessions_file
            fire_alert(str(payload_file), dry_run=False, timeout=60)

        time.sleep(1.1)  # Wait more than 1 second to ensure different timestamps

        with patch("cli.send.send_request") as mock_send, \
             patch("cli.send.get_sessions_file") as mock_get_file:
            mock_send.return_value = (True, "456")
            mock_get_file.return_value = sessions_file
            fire_alert(str(payload_file), dry_run=False, timeout=60)

        # Verify both sessions were created
        sessions = load_sessions(sessions_file)
        assert len(sessions["sessions"]) == 2

        # Both sessions should reference the same payload file
        assert sessions["sessions"][0]["payload_file"] == str(payload_file)
        assert sessions["sessions"][1]["payload_file"] == str(payload_file)

        # But have different problem IDs
        assert sessions["sessions"][0]["problem_id"] == "123"
        assert sessions["sessions"][1]["problem_id"] == "456"

        # Session IDs should be different (different timestamps)
        assert sessions["sessions"][0]["id"] != sessions["sessions"][1]["id"]
