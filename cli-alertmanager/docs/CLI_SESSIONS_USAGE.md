# CLI Sessions Usage Guide

## Overview

The `cli/send.py` tool now includes session-based tracking that automatically saves metadata from `fire` commands to `.cli-sessions.json`. This allows you to easily resolve alerts without manually managing payload files or remembering which alerts you fired.

**Key Benefits:**
- Automatic session tracking when firing alerts
- Easy resolution using saved session metadata
- Interactive or automated resolution workflows
- Cleanup utilities for resolved sessions

## Workflow: Fire an Alert

### Basic Fire Command

Fire an alert and automatically create a session:

```bash
python cli/send.py fire --file request_payload.json
```

**Output:**
```
Sent to http://localhost:5000/glpi
HTTP Status: 200 OK
Response: {"problem_id": "12345", "status": "created"}

Session saved: fire_20251030_153045_abc123
```

### What Gets Saved

Each fire command creates a session entry with:
- **Session ID**: Unique identifier (timestamp + fingerprint prefix)
- **Timestamp**: ISO 8601 timestamp of when alert was fired
- **Payload File**: Path to original payload JSON
- **Fingerprint**: SHA256 hash for deduplication (first 8 chars shown)
- **Problem ID**: GLPI problem ID from response (if available)
- **Status**: `active` (ready for resolution) or `resolved`

### Dry Run Mode

Preview what would be sent without creating a session:

```bash
python cli/send.py fire --file request_payload.json --dry-run
```

**Output:**
```
[DRY RUN] Would send to http://localhost:5000/glpi

Payload preview:
{
  "alerts": [
    {
      "startsAt": "2025-10-30T15:30:45.123456Z",
      ...
    }
  ]
}
```

Note: Dry run mode does NOT create a session entry.

## Workflow: Resolve the Alert (Interactive)

### List and Select Sessions

The interactive mode displays all active sessions and lets you choose:

```bash
python cli/send.py resolve --list-sessions
```

**Output:**
```
Available sessions:

[1] fire_20251030_153045_abc123
    Timestamp: 2025-10-30T15:30:45Z
    File: request_payload.json
    Problem ID: 12345
    Fingerprint: abc123xy...

[2] fire_20251030_160000_def456
    Timestamp: 2025-10-30T16:00:00Z
    File: critical_alert.json
    Problem ID: 12346
    Fingerprint: def456ab...

Select session number: 1
```

After you select a number, the tool will:
1. Load the original payload from the saved file path
2. Update timestamps for resolution (set `endsAt` to current time)
3. Send the resolved alert to the webhook endpoint
4. Mark the session as `resolved`

**Output after selection:**
```
Sent to http://localhost:5000/glpi
HTTP Status: 200 OK
Response: {"problem_id": "12345", "status": "resolved"}

Session marked as resolved: fire_20251030_153045_abc123
```

## Workflow: Resolve the Alert (Automated)

### Direct Session ID Resolution

If you know the session ID (from logs, scripts, or previous output), resolve it directly:

```bash
python cli/send.py resolve --session-id fire_20251030_153045_abc123
```

**Output:**
```
Sent to http://localhost:5000/glpi
HTTP Status: 200 OK
Response: {"problem_id": "12345", "status": "resolved"}

Session marked as resolved: fire_20251030_153045_abc123
```

This is ideal for:
- Shell scripts and automation
- CI/CD pipelines
- Batch resolution operations

### Example Automation Script

```bash
#!/bin/bash
# Fire multiple alerts and resolve them after 5 minutes

# Fire alerts and capture session IDs
SESSION_1=$(python cli/send.py fire --file alert1.json | grep "Session saved:" | awk '{print $3}')
SESSION_2=$(python cli/send.py fire --file alert2.json | grep "Session saved:" | awk '{print $3}')

echo "Fired sessions: $SESSION_1, $SESSION_2"
echo "Waiting 5 minutes..."
sleep 300

# Resolve using saved session IDs
python cli/send.py resolve --session-id "$SESSION_1"
python cli/send.py resolve --session-id "$SESSION_2"

echo "All alerts resolved"
```

## Workflow: Cleanup Resolved Sessions

### Clear Resolved Sessions

Remove all sessions with `status: "resolved"` from the tracking file:

```bash
python cli/send.py resolve --clear-resolved
```

**Output:**
```
Deleted 3 resolved session(s)
```

This keeps `.cli-sessions.json` manageable by removing:
- Successfully resolved alerts
- Old historical data you no longer need

**Best Practice:** Run this periodically (daily/weekly) to prevent the file from growing unbounded.

## Session File Format

### File Location

Sessions are stored in `.cli-sessions.json` in the current working directory.

### JSON Structure

```json
{
  "sessions": [
    {
      "id": "fire_20251030_153045_abc123",
      "timestamp": "2025-10-30T15:30:45.123456Z",
      "payload_file": "request_payload.json",
      "fingerprint": "abc123xyz789...",
      "problem_id": "12345",
      "status": "active"
    },
    {
      "id": "fire_20251030_160000_def456",
      "timestamp": "2025-10-30T16:00:00.789012Z",
      "payload_file": "critical_alert.json",
      "fingerprint": "def456abc123...",
      "problem_id": "12346",
      "status": "resolved"
    }
  ]
}
```

### Field Descriptions

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Unique session identifier (format: `fire_YYYYMMDD_HHMMSS_<fp_prefix>`) |
| `timestamp` | string | ISO 8601 timestamp when alert was fired |
| `payload_file` | string | Relative or absolute path to original payload JSON |
| `fingerprint` | string | SHA256 hash of alert metadata (for deduplication) |
| `problem_id` | string or null | GLPI problem ID from response (null if not available) |
| `status` | string | `"active"` (not resolved) or `"resolved"` (completed) |

## Best Practices

### 1. Keep Payload Files Intact

Do NOT delete or move payload files until their sessions are resolved:

```bash
# Bad: This breaks the session reference
rm request_payload.json

# Good: Resolve first, then clean up
python cli/send.py resolve --session-id fire_20251030_153045_abc123
python cli/send.py resolve --clear-resolved
rm request_payload.json
```

### 2. Periodic Cleanup

Add a cron job or scheduled task to clean up old sessions:

```bash
# Add to crontab: Clean up resolved sessions every Sunday at 2 AM
0 2 * * 0 cd /path/to/webhooks-alertmanager && python cli/send.py resolve --clear-resolved
```

### 3. Use Session IDs in Scripts

For automation, prefer `--session-id` over `--list-sessions`:

```bash
# Good for automation
SESSION_ID=$(python cli/send.py fire --file alert.json | grep "Session saved:" | awk '{print $3}')
python cli/send.py resolve --session-id "$SESSION_ID"

# Bad for automation (requires interactive input)
python cli/send.py resolve --list-sessions
```

### 4. Organize Payload Files

Keep payload files organized by environment or alert type:

```bash
payloads/
  dev/
    alert1.json
    alert2.json
  prod/
    critical_disk.json
    critical_memory.json
```

Session tracking works with any file path structure.

### 5. Version Control Session Files

Add `.cli-sessions.json` to `.gitignore` since it contains runtime state:

```gitignore
# .gitignore
.cli-sessions.json
```

### 6. Backup Sessions Before Cleanup

If you need historical records, backup before cleanup:

```bash
cp .cli-sessions.json .cli-sessions.backup.$(date +%Y%m%d).json
python cli/send.py resolve --clear-resolved
```

## Troubleshooting

### Error: "No active sessions found"

**Cause:** You haven't fired any alerts yet, or all sessions are already resolved.

**Solution:**
```bash
# Fire an alert first
python cli/send.py fire --file request_payload.json

# Then try resolving
python cli/send.py resolve --list-sessions
```

### Error: "Session not found: fire_20251030_153045_abc123"

**Cause:** The session ID doesn't exist or was already resolved and cleaned up.

**Solution:**
```bash
# List available sessions to see what's active
python cli/send.py resolve --list-sessions

# Or check the sessions file directly
cat .cli-sessions.json | python -m json.tool
```

### Error: "Original payload file not found: request_payload.json"

**Cause:** The payload file was moved, renamed, or deleted after firing.

**Solution:**
```bash
# Option 1: Restore the original file
git checkout request_payload.json

# Option 2: Manually edit .cli-sessions.json to update the path
# (Use a text editor to change "payload_file" value)

# Option 3: Remove the broken session
# Edit .cli-sessions.json and delete the problematic session entry
```

### Error: "Could not connect to http://localhost:5000/glpi"

**Cause:** The Flask application is not running.

**Solution:**
```bash
# In a separate terminal, start the Flask app
python app.py

# Then try the CLI command again
python cli/send.py fire --file request_payload.json
```

### Warning: "Could not save session: <error>"

**Cause:** Permission issues or disk space problems when writing `.cli-sessions.json`.

**Solution:**
```bash
# Check file permissions
ls -la .cli-sessions.json

# Check disk space
df -h .

# Verify JSON syntax is valid
python -m json.tool .cli-sessions.json

# If corrupted, restore from backup or recreate
echo '{"sessions": []}' > .cli-sessions.json
```

### Session File Corrupted

**Cause:** Manual edits or interrupted writes.

**Solution:**
```bash
# Validate JSON syntax
python -m json.tool .cli-sessions.json

# If invalid, restore from backup
cp .cli-sessions.backup.json .cli-sessions.json

# Or start fresh (loses all session history)
echo '{"sessions": []}' > .cli-sessions.json
```

## Advanced Usage

### Custom Timeout for Slow Endpoints

```bash
# Default timeout is 60 seconds
python cli/send.py fire --file alert.json --timeout 120

# Also works for resolve
python cli/send.py resolve --session-id fire_xxx --timeout 120
```

### Debugging with Dry Run

Test resolution without actually sending:

```bash
python cli/send.py resolve --session-id fire_20251030_153045_abc123 --dry-run
```

**Output:**
```
[DRY RUN] Would send to http://localhost:5000/glpi

Payload preview:
{
  "alerts": [
    {
      "startsAt": "2025-10-30T15:30:45.123456Z",
      "endsAt": "2025-10-30T15:35:45.789012Z",
      ...
    }
  ]
}
```

### Inspect Session Details

```bash
# Pretty-print all sessions
cat .cli-sessions.json | python -m json.tool

# Count active vs resolved
cat .cli-sessions.json | python -c "
import json, sys
data = json.load(sys.stdin)
active = sum(1 for s in data['sessions'] if s['status'] == 'active')
resolved = sum(1 for s in data['sessions'] if s['status'] == 'resolved')
print(f'Active: {active}, Resolved: {resolved}')
"

# Find sessions by problem ID
cat .cli-sessions.json | python -c "
import json, sys
data = json.load(sys.stdin)
problem_id = '12345'
matches = [s for s in data['sessions'] if s.get('problem_id') == problem_id]
print(json.dumps(matches, indent=2))
"
```

## Migration Guide

### From Manual File Management

**Old workflow:**
```bash
python cli/send.py fire --file alert.json
# ... manually track which file you used ...
python cli/send.py resolve --file alert.json
```

**New workflow:**
```bash
python cli/send.py fire --file alert.json
# Session automatically saved
python cli/send.py resolve --list-sessions
# Select from list, no need to remember filename
```

### Backward Compatibility

The `--file` parameter is still supported for `resolve` command:

```bash
# Still works (bypasses session system)
python cli/send.py resolve --file request_payload.json
```

This is useful for:
- One-off resolutions
- Testing without tracking
- Legacy scripts that haven't migrated to sessions

## Examples

### Example 1: Single Alert Lifecycle

```bash
# Fire alert
python cli/send.py fire --file disk_full.json
# Output: Session saved: fire_20251030_153045_abc123

# Wait for remediation...

# Resolve interactively
python cli/send.py resolve --list-sessions
# Select [1]

# Clean up
python cli/send.py resolve --clear-resolved
```

### Example 2: Multiple Alerts

```bash
# Fire three alerts
python cli/send.py fire --file alert1.json  # Session: fire_xxx1
python cli/send.py fire --file alert2.json  # Session: fire_xxx2
python cli/send.py fire --file alert3.json  # Session: fire_xxx3

# Check all active
python cli/send.py resolve --list-sessions

# Resolve one by one as issues are fixed
python cli/send.py resolve --session-id fire_xxx1
python cli/send.py resolve --session-id fire_xxx3

# Later resolve the last one
python cli/send.py resolve --list-sessions  # Shows only fire_xxx2
```

### Example 3: Automated Testing

```bash
# test_alert_flow.sh
#!/bin/bash
set -e

# Fire test alert
SESSION_ID=$(python cli/send.py fire --file test_alert.json | grep "Session saved:" | awk '{print $3}')
echo "Test alert fired: $SESSION_ID"

# Verify in GLPI...

# Auto-resolve after test
sleep 10
python cli/send.py resolve --session-id "$SESSION_ID"

# Cleanup
python cli/send.py resolve --clear-resolved

echo "Test complete"
```

## Summary

The CLI sessions feature streamlines alert management by:
- Automatically tracking fired alerts
- Eliminating manual file/ID management
- Supporting both interactive and automated workflows
- Providing cleanup utilities for resolved sessions

For questions or issues, refer to the main project documentation or open a GitHub issue.
