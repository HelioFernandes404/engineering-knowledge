import json
import tempfile
from pathlib import Path
from datetime import datetime, timezone
import pytest
from cli.session_manager import (
    load_sessions,
    save_sessions,
    create_session,
    get_active_sessions,
    update_session_status,
    delete_resolved_sessions,
    get_session_by_id,
    format_session_display,
)


def test_load_sessions_creates_empty_file_if_missing(tmp_path):
    """Test that load_sessions creates .cli-sessions.json if it doesn't exist."""
    sessions_file = tmp_path / ".cli-sessions.json"
    sessions = load_sessions(sessions_file)

    assert sessions == {"sessions": []}
    assert sessions_file.exists()


def test_load_sessions_reads_existing_file(tmp_path):
    """Test that load_sessions reads existing sessions."""
    sessions_file = tmp_path / ".cli-sessions.json"
    expected_data = {
        "sessions": [
            {
                "id": "fire_20251030_153045_abc",
                "timestamp": "2025-10-30T15:30:45Z",
                "payload_file": "test.json",
                "fingerprint": "abc123",
                "problem_id": "123",
                "status": "active",
            }
        ]
    }
    sessions_file.write_text(json.dumps(expected_data))

    sessions = load_sessions(sessions_file)
    assert sessions == expected_data


def test_load_sessions_validates_data_is_dict(tmp_path):
    """Test that load_sessions raises ValueError if data is not a dict."""
    sessions_file = tmp_path / ".cli-sessions.json"
    sessions_file.write_text(json.dumps([]))  # List instead of dict

    with pytest.raises(ValueError, match="expected dict, got list"):
        load_sessions(sessions_file)


def test_load_sessions_validates_sessions_key_exists(tmp_path):
    """Test that load_sessions raises ValueError if 'sessions' key is missing."""
    sessions_file = tmp_path / ".cli-sessions.json"
    sessions_file.write_text(json.dumps({"data": []}))  # Wrong key

    with pytest.raises(ValueError, match='missing required "sessions" key'):
        load_sessions(sessions_file)


def test_load_sessions_validates_sessions_is_list(tmp_path):
    """Test that load_sessions raises ValueError if 'sessions' is not a list."""
    sessions_file = tmp_path / ".cli-sessions.json"
    sessions_file.write_text(json.dumps({"sessions": "not a list"}))

    with pytest.raises(ValueError, match='"sessions" must be a list, got str'):
        load_sessions(sessions_file)


def test_save_sessions_writes_file(tmp_path):
    """Test that save_sessions writes to file."""
    sessions_file = tmp_path / ".cli-sessions.json"
    data = {"sessions": [{"id": "fire_123", "status": "active"}]}

    save_sessions(sessions_file, data)

    assert sessions_file.exists()
    saved = json.loads(sessions_file.read_text())
    assert saved == data


def test_create_session_adds_new_session(tmp_path):
    """Test that create_session adds to sessions list."""
    sessions_file = tmp_path / ".cli-sessions.json"
    sessions = load_sessions(sessions_file)

    timestamp = "2025-10-30T15:30:45Z"
    new_session = create_session(
        payload_file="request_payload.json",
        fingerprint="abc123xyz",
        problem_id="12345",
        timestamp=timestamp,
    )

    assert new_session["payload_file"] == "request_payload.json"
    assert new_session["fingerprint"] == "abc123xyz"
    assert new_session["problem_id"] == "12345"
    assert new_session["status"] == "active"
    assert "id" in new_session
    assert new_session["timestamp"] == timestamp


def test_get_active_sessions_filters_by_status(tmp_path):
    """Test that get_active_sessions returns only active sessions."""
    sessions_file = tmp_path / ".cli-sessions.json"
    data = {
        "sessions": [
            {"id": "fire_1", "status": "active", "fingerprint": "aaa"},
            {"id": "fire_2", "status": "resolved", "fingerprint": "bbb"},
            {"id": "fire_3", "status": "active", "fingerprint": "ccc"},
        ]
    }
    sessions_file.write_text(json.dumps(data))

    active = get_active_sessions(sessions_file)

    assert len(active) == 2
    assert all(s["status"] == "active" for s in active)


def test_update_session_status_changes_status(tmp_path):
    """Test that update_session_status modifies session."""
    sessions_file = tmp_path / ".cli-sessions.json"
    data = {
        "sessions": [
            {"id": "fire_1", "status": "active", "fingerprint": "aaa"},
        ]
    }
    sessions_file.write_text(json.dumps(data))

    update_session_status(sessions_file, "fire_1", "resolved")

    updated = load_sessions(sessions_file)
    assert updated["sessions"][0]["status"] == "resolved"


def test_update_session_status_raises_on_not_found(tmp_path):
    """Test that update_session_status raises ValueError for missing session."""
    sessions_file = tmp_path / ".cli-sessions.json"
    load_sessions(sessions_file)  # Create empty file

    with pytest.raises(ValueError, match="Session not found"):
        update_session_status(sessions_file, "fire_nonexistent", "resolved")


def test_get_session_by_id_returns_session(tmp_path):
    """Test that get_session_by_id retrieves correct session."""
    sessions_file = tmp_path / ".cli-sessions.json"
    data = {
        "sessions": [
            {"id": "fire_1", "problem_id": "123", "fingerprint": "aaa"},
            {"id": "fire_2", "problem_id": "456", "fingerprint": "bbb"},
        ]
    }
    sessions_file.write_text(json.dumps(data))

    session = get_session_by_id(sessions_file, "fire_2")

    assert session["problem_id"] == "456"
    assert session["fingerprint"] == "bbb"


def test_get_session_by_id_raises_on_not_found(tmp_path):
    """Test that get_session_by_id raises ValueError for missing session."""
    sessions_file = tmp_path / ".cli-sessions.json"
    load_sessions(sessions_file)

    with pytest.raises(ValueError, match="Session not found"):
        get_session_by_id(sessions_file, "fire_nonexistent")


def test_delete_resolved_sessions_removes_resolved(tmp_path):
    """Test that delete_resolved_sessions removes resolved sessions."""
    sessions_file = tmp_path / ".cli-sessions.json"
    data = {
        "sessions": [
            {"id": "fire_1", "status": "active"},
            {"id": "fire_2", "status": "resolved"},
            {"id": "fire_3", "status": "resolved"},
        ]
    }
    sessions_file.write_text(json.dumps(data))

    delete_resolved_sessions(sessions_file)

    updated = load_sessions(sessions_file)
    assert len(updated["sessions"]) == 1
    assert updated["sessions"][0]["id"] == "fire_1"


def test_format_session_display_empty_list():
    """Test that format_session_display returns 'No active sessions' for empty list."""
    result = format_session_display([])
    assert result == "No active sessions found."


def test_format_session_display_shows_correct_output():
    """Test that format_session_display formats sessions with [1], [2], etc."""
    sessions = [
        {
            "id": "fire_20251030_153045_abc123",
            "timestamp": "2025-10-30T15:30:45Z",
            "payload_file": "request_payload_1.json",
            "fingerprint": "abc123xyz789",
            "problem_id": "12345",
            "status": "active",
        },
        {
            "id": "fire_20251030_160000_def456",
            "timestamp": "2025-10-30T16:00:00Z",
            "payload_file": "request_payload_2.json",
            "fingerprint": "def456uvw321",
            "problem_id": "67890",
            "status": "active",
        },
    ]

    result = format_session_display(sessions)

    # Check that it includes the numbering
    assert "[1]" in result
    assert "[2]" in result

    # Check that it includes session details
    assert "fire_20251030_153045_abc123" in result
    assert "fire_20251030_160000_def456" in result
    assert "2025-10-30T15:30:45Z" in result
    assert "2025-10-30T16:00:00Z" in result
    assert "request_payload_1.json" in result
    assert "request_payload_2.json" in result
    assert "12345" in result
    assert "67890" in result

    # Check that fingerprints are truncated to 8 chars
    assert "abc123xy" in result
    assert "def456uv" in result
