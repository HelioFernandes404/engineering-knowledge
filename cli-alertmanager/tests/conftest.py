import pytest
import sys
import os
import json
from unittest.mock import patch, MagicMock

# Add the parent directory to the path so we can import our modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Mock sf_common.metrics.metric at module level
sys.modules['sf_common'] = MagicMock()
sys.modules['sf_common.metrics'] = MagicMock()
sys.modules['sf_common.metrics.metric'] = MagicMock()

mock_counter = MagicMock()
mock_counter.add = MagicMock()
mock_metric_manager = MagicMock()
mock_metric_manager.create_counter.return_value = mock_counter
sys.modules['sf_common.metrics.metric'].MetricManager = MagicMock(return_value=mock_metric_manager)

# Mock environment variables before any imports
@pytest.fixture(scope="session", autouse=True)
def mock_environment_variables():
    """Mock environment variables required for tests."""
    with patch.dict(os.environ, {
        'API_HOST_GLPI': 'http://test-glpi-host.local',
        'API_TOKEN': 'test_api_token',
        'USER_TOKEN': 'test_user_token',
        'ACCOUNT_SID': 'test_account_sid',
        'AUTH_TOKEN_TWILIO': 'test_twilio_token',
        'FROM_NUMBER': '+1234567890',
        'TO_NUMBER': '+0987654321',
        'LAUNCHDARKLY_SDK_KEY': 'test_ld_key',
    }, clear=False):
        yield

# Mock LaunchDarkly client before any imports that use it
@pytest.fixture(scope="session", autouse=True)
def mock_launchdarkly():
    """Mock LaunchDarkly SDK to prevent initialization errors during tests."""
    with patch('webhook_glpi.scripts.config.ldclient') as mock_ld:
        mock_client = MagicMock()
        mock_client.is_initialized.return_value = True
        mock_client.variation.return_value = True
        mock_ld.get.return_value = mock_client
        yield mock_ld

# Mock Redis/memoization layer before any imports
@pytest.fixture(scope="session", autouse=True)
def mock_redis():
    """Mock Redis and memoization layer to prevent connection errors during tests."""
    try:
        with patch('webhook_glpi.scripts.glpi.m') as mock_memoizer:
            # Mock the invalidate_memoize method to do nothing
            mock_memoizer.invalidate_memoize = MagicMock()
            yield mock_memoizer
    except (ImportError, AttributeError):
        # If glpi module doesn't exist, skip mocking (for session_manager tests)
        yield MagicMock()

@pytest.fixture
def app():
    """Create and configure a test instance of the Flask app."""
    from app import app
    app.config['TESTING'] = True
    return app

@pytest.fixture
def client(app):
    """Create a test client for the Flask app."""
    return app.test_client()

@pytest.fixture
def sample_alert():
    """Sample alert data for testing."""
    return {
        "alerts": [
            {
                "status": "firing",
                "labels": {
                    "alertname": "TestAlert",
                    "alertgroup": "TestGroup",
                    "customer": "test_customer",
                    "glpi_item_id": "123",
                    "glpi_item_type": "Computer"
                },
                "annotations": {
                    "description": "Test alert description"
                },
                "fingerprint": "test_fingerprint",
                "startsAt": "2023-01-01T00:00:00Z",
                "generatorURL": "http://test.com/metrics"
            }
        ]
    }

@pytest.fixture(scope="session")
def request_payload():
    """Load the real request payload from request_payload.json."""
    payload_path = os.path.join(os.path.dirname(__file__), '..', 'request_payload.json')
    with open(payload_path, 'r') as f:
        return json.load(f)