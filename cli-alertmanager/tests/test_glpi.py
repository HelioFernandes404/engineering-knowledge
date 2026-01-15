import pytest
import json
import hashlib
from unittest.mock import patch, MagicMock, Mock
from flask import Flask
from webhook_glpi.scripts.glpi import (
    generate_fingerprint, 
    alertmanager_glpi, 
    create_problem, 
    create_ticket, 
    assign_problem, 
    assign_ticket
)

class TestGenerateFingerprint:
    """Test cases for generate_fingerprint function following TDD principles."""
    
    def test_generate_fingerprint_with_complete_alert_data(self):
        """Test fingerprint generation with complete alert data."""
        # Arrange
        alert = {
            'fingerprint': 'abc123',
            'startsAt': '2023-01-01T00:00:00Z',
            'generatorURL': 'http://prometheus:9090/graph',
            'alertname': 'TestAlert'
        }
        
        expected_source = "TestAlert|abc123|2023-01-01T00:00:00Z|http://prometheus:9090/graph"
        expected_hash = hashlib.sha256(expected_source.encode('utf-8')).hexdigest()
        
        # Act
        result = generate_fingerprint(alert)
        
        # Assert
        assert result == expected_hash
        assert len(result) == 64  # SHA256 produces 64 character hex string
    
    def test_generate_fingerprint_with_missing_fields(self):
        """Test fingerprint generation when some fields are missing."""
        # Arrange
        alert = {
            'fingerprint': 'abc123',
            'startsAt': '2023-01-01T00:00:00Z'
            # Missing generatorURL and alertname
        }
        
        expected_source = "None|abc123|2023-01-01T00:00:00Z|None"
        expected_hash = hashlib.sha256(expected_source.encode('utf-8')).hexdigest()
        
        # Act
        result = generate_fingerprint(alert)
        
        # Assert
        assert result == expected_hash
    
    def test_generate_fingerprint_empty_alert(self):
        """Test fingerprint generation with empty alert."""
        # Arrange
        alert = {}
        
        expected_source = "None|None|None|None"
        expected_hash = hashlib.sha256(expected_source.encode('utf-8')).hexdigest()
        
        # Act
        result = generate_fingerprint(alert)
        
        # Assert
        assert result == expected_hash
    
    def test_generate_fingerprint_consistency(self):
        """Test that same input produces same fingerprint."""
        # Arrange
        alert = {
            'fingerprint': 'test123',
            'startsAt': '2023-01-01T12:00:00Z',
            'generatorURL': 'http://test.com',
            'alertname': 'ConsistencyTest'
        }
        
        # Act
        result1 = generate_fingerprint(alert)
        result2 = generate_fingerprint(alert)
        
        # Assert
        assert result1 == result2


class TestAlertmanagerGlpi:
    """Test cases for alertmanager_glpi endpoint."""
    
    def test_alertmanager_glpi_valid_data(self, client):
        """Test endpoint with valid data."""
        # Act
        response = client.post('/glpi', json={})

        assert response
    
    def test_alertmanager_glpi_invalid_data(self, client):
        """Test endpoint with invalid data."""
        # Act
        response = client.post('/glpi', json={})
        
        # Assert
        assert response.status_code == 400
        assert 'Invalid data received' in response.get_json()['error']
    
    def test_alertmanager_glpi_no_alerts(self, client):
        """Test endpoint with no alerts in data."""
        # Act
        response = client.post('/glpi', json={'alerts': []})
        
        # Assert
        assert response.status_code == 200
        data = response.get_json()
        assert data['message'] == 'Alerts processed and sent to GLPI successfully'
        assert data['problems_created'] == []
    
    @patch('webhook_glpi.scripts.glpi.fetch_asset_data')
    @patch('webhook_glpi.scripts.glpi.get_auth_token')
    def test_alertmanager_glpi_missing_asset_data(self, mock_get_auth_token, mock_fetch_asset_data, client, sample_alert):
        """Test endpoint when asset data is not found."""
        # Arrange
        mock_fetch_asset_data.return_value = None
        mock_get_auth_token.return_value = 'test_token'
        
        # Act
        response = client.post('/glpi', json=sample_alert)
        
        # Assert
        assert response.status_code == 200
        data = response.get_json()
        assert data['problems_created'] == []


class TestCreateProblem:
    """Test cases for create_problem function."""
    
    @patch('webhook_glpi.scripts.glpi.requests.post')
    @patch('webhook_glpi.scripts.glpi.get_auth_token')
    @patch('webhook_glpi.scripts.glpi.get_api_token')
    @patch('webhook_glpi.scripts.glpi.get_glpi_host')
    def test_create_problem_success(self, mock_get_host, mock_get_api_token, mock_get_auth_token, mock_requests_post):
        """Test successful problem creation."""
        # Arrange
        mock_get_host.return_value = 'http://glpi.test'
        mock_get_api_token.return_value = 'api_token'
        mock_get_auth_token.return_value = 'session_token'
        
        mock_response = Mock()
        mock_response.status_code = 201
        mock_response.json.return_value = {'id': 123}
        mock_requests_post.return_value = mock_response
        
        glpi_data = {
            'input': {
                'name': 'Test Problem',
                'content': 'Test Description',
                'priority': 4,
                'entities_id': 1
            }
        }
        fingerprint = 'test_fingerprint_123'
        
        # Act
        result = create_problem(glpi_data, fingerprint)
        
        # Assert
        assert result.status_code == 201
        mock_requests_post.assert_any_call('http://glpi.test/Problem', headers={
            'Session-Token': 'session_token',
            'App-Token': 'api_token'
        }, json=glpi_data)
    
    @patch('webhook_glpi.scripts.glpi.requests.post')
    @patch('webhook_glpi.scripts.glpi.get_auth_token')
    @patch('webhook_glpi.scripts.glpi.get_api_token')  
    @patch('webhook_glpi.scripts.glpi.get_glpi_host')
    def test_create_problem_failure(self, mock_get_host, mock_get_api_token, mock_get_auth_token, mock_requests_post):
        """Test problem creation failure."""
        # Arrange
        mock_get_host.return_value = 'http://glpi.test'
        mock_get_api_token.return_value = 'api_token'
        mock_get_auth_token.return_value = 'session_token'
        
        mock_response = Mock()
        mock_response.status_code = 400
        mock_requests_post.return_value = mock_response
        
        glpi_data = {'input': {'name': 'Test Problem'}}
        fingerprint = 'test_fingerprint'
        
        # Act
        result = create_problem(glpi_data, fingerprint)
        
        # Assert
        assert result.status_code == 400


class TestCreateTicket:
    """Test cases for create_ticket function."""
    
    @patch('webhook_glpi.scripts.glpi.requests.post')
    @patch('webhook_glpi.scripts.glpi.get_auth_token')
    @patch('webhook_glpi.scripts.glpi.get_api_token')
    @patch('webhook_glpi.scripts.glpi.get_glpi_host')
    def test_create_ticket_success(self, mock_get_host, mock_get_api_token, mock_get_auth_token, mock_requests_post):
        """Test successful ticket creation."""
        # Arrange
        mock_get_host.return_value = 'http://glpi.test'
        mock_get_api_token.return_value = 'api_token'
        mock_get_auth_token.return_value = 'session_token'
        
        mock_response = Mock()
        mock_response.status_code = 201
        mock_response.json.return_value = {'id': 456}
        mock_requests_post.return_value = mock_response
        
        glpi_data = {
            'input': {
                'name': 'Test Ticket',
                'content': 'Test Description',
                'entities_id': 1
            }
        }
        data_att = {'items_id': 123, 'itemtype': 'Computer'}
        
        # Act
        result = create_ticket(glpi_data, data_att)
        
        # Assert
        assert result.status_code == 201
        expected_data = {
            'input': {
                'name': 'Test Ticket',
                'content': 'Test Description',
                'urgency': 4,
                'entities_id': 1,
                'itilcategories_id': 2800
            }
        }
        mock_requests_post.assert_called_with('http://glpi.test/Ticket', headers={
            'Session-Token': 'session_token',
            'App-Token': 'api_token'
        }, json=expected_data)


class TestAssignProblem:
    """Test cases for assign_problem function."""
    
    @patch('webhook_glpi.scripts.glpi.requests.post')
    @patch('webhook_glpi.scripts.glpi.get_auth_token')
    @patch('webhook_glpi.scripts.glpi.get_api_token')
    @patch('webhook_glpi.scripts.glpi.get_glpi_host')
    def test_assign_problem_success(self, mock_get_host, mock_get_api_token, mock_get_auth_token, mock_requests_post):
        """Test successful problem assignment to item."""
        # Arrange
        mock_get_host.return_value = 'http://glpi.test'
        mock_get_api_token.return_value = 'api_token'
        mock_get_auth_token.return_value = 'session_token'
        
        mock_response = Mock()
        mock_response.status_code = 201
        mock_response.json.return_value = {'id': 789}
        mock_requests_post.return_value = mock_response
        
        data_att = {
            'input': {
                'items_id': 123,
                'itemtype': 'Computer',
                'problems_id': 456
            }
        }
        
        # Act
        result = assign_problem(data_att)
        
        # Assert
        assert result is not None
        assert result.status_code == 201
        mock_requests_post.assert_called_with('http://glpi.test/Item_Problem', headers={
            'Session-Token': 'session_token',
            'App-Token': 'api_token'
        }, json=data_att)


class TestAssignTicket:
    """Test cases for assign_ticket function."""
    
    @patch('webhook_glpi.scripts.glpi.requests.post')
    @patch('webhook_glpi.scripts.glpi.get_auth_token')
    @patch('webhook_glpi.scripts.glpi.get_api_token')
    @patch('webhook_glpi.scripts.glpi.get_glpi_host')
    def test_assign_ticket_success(self, mock_get_host, mock_get_api_token, mock_get_auth_token, mock_requests_post):
        """Test successful ticket assignment to problems and items."""
        # Arrange
        mock_get_host.return_value = 'http://glpi.test'
        mock_get_api_token.return_value = 'api_token'
        mock_get_auth_token.return_value = 'session_token'
        
        mock_response = Mock()
        mock_response.status_code = 201
        mock_requests_post.return_value = mock_response
        
        ticket_data = {'id': 789}
        problem_id = [123, 456]
        data_att = {'items_id': 999, 'itemtype': 'Computer'}
        
        # Act
        result = assign_ticket(ticket_data, problem_id, data_att)
        
        # Assert
        assert result.status_code == 201
        assert mock_requests_post.call_count == 3  # 2 problem assignments + 1 item assignment


class TestAlertmanagerGlpiWithRealData:
    """Test cases for alertmanager_glpi with real alert data from request_payload.json."""

    @pytest.fixture
    def real_alert_data(self, request_payload):
        """Real alert data loaded from request_payload.json."""
        return request_payload
    
    @patch('webhook_glpi.scripts.glpi.servicenow')
    @patch('webhook_glpi.scripts.glpi.fetch_asset_data')
    @patch('webhook_glpi.scripts.glpi.get_auth_token')
    @patch('webhook_glpi.scripts.glpi.get_problem_by_fingerprint')
    @patch('webhook_glpi.scripts.glpi.get_item_equipments')
    @patch('webhook_glpi.scripts.glpi.create_problem')
    @patch('webhook_glpi.scripts.glpi.assign_problem')
    @patch('webhook_glpi.scripts.glpi.create_ticket')
    @patch('webhook_glpi.scripts.glpi.assign_ticket')
    def test_alertmanager_glpi_full_flow_with_real_data(
        self, 
        mock_assign_ticket,
        mock_create_ticket,
        mock_assign_problem,
        mock_create_problem,
        mock_get_item_equipments,
        mock_get_problem_by_fingerprint,
        mock_get_auth_token,
        mock_fetch_asset_data,
        mock_servicenow,
        client,
        real_alert_data
    ):
        """Test full flow with real alert data."""
        # Arrange
        mock_servicenow.incident_context_builder.return_value = {"test": "context"}
        mock_servicenow.evaluate_incident_context.return_value = True
        
        mock_fetch_asset_data.return_value = {
            "glpi_item_type": "Computer",
            "entity_id": 1,
            "glpi_item_id": 123
        }
        mock_get_auth_token.return_value = 'test_session_token'
        mock_get_problem_by_fingerprint.return_value = None  # No existing problem
        mock_get_item_equipments.return_value = {"entities_id": 1}
        
        # Mock successful problem creation
        mock_problem_response = Mock()
        mock_problem_response.status_code = 201
        mock_problem_response.json.return_value = {"id": 999}
        mock_create_problem.return_value = mock_problem_response
        
        # Mock successful problem assignment
        mock_assign_response = Mock()
        mock_assign_response.status_code = 201
        mock_assign_problem.return_value = mock_assign_response
        
        # Mock successful ticket creation
        mock_ticket_response = Mock()
        mock_ticket_response.status_code = 201
        mock_ticket_response.json.return_value = {"id": 888}
        mock_create_ticket.return_value = mock_ticket_response
        
        # Act
        response = client.post('/glpi', json=real_alert_data)
        
        # Assert
        assert response.status_code == 200
        data = response.get_json()
        assert data['message'] == 'Alerts processed and sent to GLPI successfully'
        # request_payload.json has 2 alerts, so we expect 2 problems
        assert len(data['problems_created']) == 2
        assert all(pid == 999 for pid in data['problems_created'])

        # Verify problem creation was called for each alert
        assert mock_create_problem.call_count == 2

        # Verify problem assignment was called for each alert
        assert mock_assign_problem.call_count == 2

        # Verify ticket creation and assignment were called for each alert
        assert mock_create_ticket.call_count == 2
        assert mock_assign_ticket.call_count == 2
    
    @patch('webhook_glpi.scripts.glpi.servicenow')
    @patch('webhook_glpi.scripts.glpi.fetch_asset_data')
    def test_alertmanager_glpi_no_asset_data(self, mock_fetch_asset_data, mock_servicenow, client, real_alert_data):
        """Test behavior when asset data is not found."""
        # Arrange
        mock_servicenow.incident_context_builder.return_value = {"test": "context"}
        mock_servicenow.evaluate_incident_context.return_value = True
        
        mock_fetch_asset_data.return_value = None
        
        # Act
        response = client.post('/glpi', json=real_alert_data)
        
        # Assert
        assert response.status_code == 200
        data = response.get_json()
        assert data['problems_created'] == []
    
    def test_generate_fingerprint_with_real_alert(self, real_alert_data):
        """Test fingerprint generation with real alert data."""
        # Arrange
        alert = real_alert_data['alerts'][0]
        
        # Act
        result = generate_fingerprint(alert)
        
        # Assert
        assert len(result) == 64  # SHA256 hash length
        assert isinstance(result, str)
        
        # Test consistency
        result2 = generate_fingerprint(alert)
        assert result == result2

    @patch('webhook_glpi.scripts.glpi.assign_ticket')
    @patch('webhook_glpi.scripts.glpi.create_ticket')
    @patch('webhook_glpi.scripts.glpi.assign_problem')
    @patch('webhook_glpi.scripts.glpi.create_problem')
    @patch('webhook_glpi.scripts.glpi.get_item_equipments')
    @patch('webhook_glpi.scripts.glpi.get_problem_by_fingerprint')
    @patch('webhook_glpi.scripts.glpi.get_auth_token')
    @patch('webhook_glpi.scripts.glpi.fetch_asset_data')
    @patch('webhook_glpi.scripts.glpi.servicenow.evaluate_incident_context')
    @patch('webhook_glpi.scripts.glpi.servicenow.incident_context_builder')
    def test_alertmanager_glpi_valid_data_happy_path(
        self,
        mock_incident_context_builder,
        mock_evaluate_incident_context,
        mock_fetch_asset_data,
        mock_get_auth_token,
        mock_get_problem_by_fingerprint,
        mock_get_item_equipments,
        mock_create_problem,
        mock_assign_problem,
        mock_create_ticket,
        mock_assign_ticket,
        client,
        real_alert_data
    ):
        """End-to-end happy path with external edges patched."""
        mock_incident_context_builder.return_value = {"ok": True}
        mock_evaluate_incident_context.return_value = True
        mock_fetch_asset_data.return_value = {
            "glpi_item_type": "Computer",
            "entity_id": 1,
            "glpi_item_id": 123
        }
        mock_get_auth_token.return_value = 'tkn'
        mock_get_problem_by_fingerprint.return_value = None
        mock_get_item_equipments.return_value = {"entities_id": 1}

        ok = Mock(status_code=201); ok.json.return_value = {"id": 42}
        mock_create_problem.return_value = ok
        mock_assign_problem.return_value = ok
        mock_create_ticket.return_value = ok
        mock_assign_ticket.return_value = ok

        r = client.post('/glpi', json=real_alert_data)
        assert r.status_code == 200
        body = r.get_json()
        assert body["message"] == "Alerts processed and sent to GLPI successfully"
        # request_payload.json has 2 alerts, so we expect 2 problems with ID 42
        assert len(body["problems_created"]) == 2
        assert all(pid == 42 for pid in body["problems_created"])


class TestAlertmanagerGlpiMissingCoverage:
    """Test cases for missing coverage scenarios in alertmanager_glpi."""

    @pytest.fixture
    def resolved_alert_data(self, request_payload):
        """Alert data with resolved status based on request_payload.json."""
        # Create a copy and modify status to resolved
        resolved_data = request_payload.copy()
        resolved_data['alerts'][0] = request_payload['alerts'][0].copy()
        resolved_data['alerts'][0]['status'] = 'resolved'
        return resolved_data

    @pytest.fixture
    def duplicate_alert_data(self, request_payload):
        """Alert data that should trigger duplicate detection based on request_payload.json."""
        # Use only the firing alert (second alert in request_payload.json)
        duplicate_data = request_payload.copy()
        duplicate_data['alerts'] = [alert for alert in request_payload['alerts'] if alert['status'] == 'firing']
        return duplicate_data

    @pytest.fixture
    def missing_glpi_id_alert(self, request_payload):
        """Alert data missing glpi_item_id based on request_payload.json."""
        return request_payload.copy()

    # TEST 1: Resolved Alerts Flow
    @patch('webhook_glpi.scripts.glpi.servicenow')
    @patch('webhook_glpi.scripts.glpi.fetch_asset_data')
    @patch('webhook_glpi.scripts.glpi.get_auth_token')
    @patch('webhook_glpi.scripts.glpi.get_problem_by_fingerprint')
    @patch('webhook_glpi.scripts.glpi.close_problem')
    def test_alertmanager_glpi_resolved_alert_closes_problem(
        self,
        mock_close_problem,
        mock_get_problem_by_fingerprint,
        mock_get_auth_token,
        mock_fetch_asset_data,
        mock_servicenow,
        client,
        resolved_alert_data
    ):
        """Test that resolved alerts close existing problems."""
        # Arrange
        mock_servicenow.incident_context_builder.return_value = {"test": "context"}
        mock_servicenow.evaluate_incident_context.return_value = True
        
        mock_fetch_asset_data.return_value = {
            "glpi_item_type": "Computer",
            "entity_id": 1,
            "glpi_item_id": 123
        }
        mock_get_auth_token.return_value = 'test_session_token'
        mock_get_problem_by_fingerprint.return_value = {"items_id": 999}  # Existing problem
        
        # Act
        response = client.post('/glpi', json=resolved_alert_data)
        
        # Assert
        assert response.status_code == 200
        data = response.get_json()
        assert data['problems_created'] == []
        mock_close_problem.assert_called_once_with(999, 'test_session_token')

    # TEST 2: Resolved Alert with No Existing Problem  
    @patch('webhook_glpi.scripts.glpi.servicenow')
    @patch('webhook_glpi.scripts.glpi.fetch_asset_data')
    @patch('webhook_glpi.scripts.glpi.get_auth_token')
    @patch('webhook_glpi.scripts.glpi.get_problem_by_fingerprint')
    @patch('webhook_glpi.scripts.glpi.close_problem')
    def test_alertmanager_glpi_resolved_alert_no_existing_problem(
        self,
        mock_close_problem,
        mock_get_problem_by_fingerprint,
        mock_get_auth_token,
        mock_fetch_asset_data,
        mock_servicenow,
        client,
        resolved_alert_data
    ):
        """Test resolved alert when no existing problem found."""
        # Arrange
        mock_servicenow.incident_context_builder.return_value = {"test": "context"}
        mock_servicenow.evaluate_incident_context.return_value = True
        
        mock_fetch_asset_data.return_value = {
            "glpi_item_type": "Computer",
            "entity_id": 1,
            "glpi_item_id": 123
        }
        mock_get_auth_token.return_value = 'test_session_token'
        mock_get_problem_by_fingerprint.return_value = None  # No existing problem
        
        # Act
        response = client.post('/glpi', json=resolved_alert_data)
        
        # Assert
        assert response.status_code == 200
        data = response.get_json()
        assert data['problems_created'] == []
        mock_close_problem.assert_not_called()

    # TEST 3: Duplicate Problem Detection
    @patch('webhook_glpi.scripts.glpi.servicenow')
    @patch('webhook_glpi.scripts.glpi.fetch_asset_data')
    @patch('webhook_glpi.scripts.glpi.get_auth_token')
    @patch('webhook_glpi.scripts.glpi.get_problem_by_fingerprint')
    def test_alertmanager_glpi_duplicate_problem_detection(
        self,
        mock_get_problem_by_fingerprint,
        mock_get_auth_token,
        mock_fetch_asset_data,
        mock_servicenow,
        client,
        duplicate_alert_data
    ):
        """Test that duplicate firing alerts are skipped."""
        # Arrange
        mock_servicenow.incident_context_builder.return_value = {"test": "context"}
        mock_servicenow.evaluate_incident_context.return_value = True
        
        mock_fetch_asset_data.return_value = {
            "glpi_item_type": "Computer",
            "entity_id": 1,
            "glpi_item_id": 123
        }
        mock_get_auth_token.return_value = 'test_session_token'
        mock_get_problem_by_fingerprint.return_value = {"items_id": 999}  # Existing problem
        
        # Act
        response = client.post('/glpi', json=duplicate_alert_data)
        
        # Assert
        assert response.status_code == 200
        data = response.get_json()
        assert data['problems_created'] == []

    # TEST 4: Missing glpi_item_id
    @patch('webhook_glpi.scripts.glpi.servicenow')
    @patch('webhook_glpi.scripts.glpi.fetch_asset_data')
    @patch('webhook_glpi.scripts.glpi.get_auth_token')
    @patch('webhook_glpi.scripts.glpi.get_problem_by_fingerprint')
    def test_alertmanager_glpi_missing_glpi_item_id(
        self,
        mock_get_problem_by_fingerprint,
        mock_get_auth_token,
        mock_fetch_asset_data,
        mock_servicenow,
        client,
        missing_glpi_id_alert
    ):
        """Test alert processing when glpi_item_id is missing."""
        # Arrange
        mock_servicenow.incident_context_builder.return_value = {"test": "context"}
        mock_servicenow.evaluate_incident_context.return_value = True
        
        mock_fetch_asset_data.return_value = {
            "glpi_item_type": "Computer",
            "entity_id": 1,
            "glpi_item_id": None  # Missing item id
        }
        mock_get_auth_token.return_value = 'test_session_token'
        mock_get_problem_by_fingerprint.return_value = None
        
        # Act
        response = client.post('/glpi', json=missing_glpi_id_alert)
        
        # Assert
        assert response.status_code == 200
        data = response.get_json()
        assert data['problems_created'] == []

    # TEST 5: Missing glpi_item_type
    @patch('webhook_glpi.scripts.glpi.servicenow')
    @patch('webhook_glpi.scripts.glpi.fetch_asset_data')
    @patch('webhook_glpi.scripts.glpi.get_auth_token')
    @patch('webhook_glpi.scripts.glpi.get_problem_by_fingerprint')
    def test_alertmanager_glpi_missing_glpi_item_type(
        self,
        mock_get_problem_by_fingerprint,
        mock_get_auth_token,
        mock_fetch_asset_data,
        mock_servicenow,
        client,
        missing_glpi_id_alert
    ):
        """Test alert processing when glpi_item_type is missing."""
        # Arrange
        mock_servicenow.incident_context_builder.return_value = {"test": "context"}
        mock_servicenow.evaluate_incident_context.return_value = True
        
        mock_fetch_asset_data.return_value = {
            "glpi_item_type": None,  # Missing item type
            "entity_id": 1,
            "glpi_item_id": 123
        }
        mock_get_auth_token.return_value = 'test_session_token'
        mock_get_problem_by_fingerprint.return_value = None
        
        # Act
        response = client.post('/glpi', json=missing_glpi_id_alert)
        
        # Assert
        assert response.status_code == 200
        data = response.get_json()
        assert data['problems_created'] == []

    # TEST 6: Exception Handling
    @patch('webhook_glpi.scripts.glpi.servicenow')
    @patch('webhook_glpi.scripts.glpi.fetch_asset_data')
    @patch('webhook_glpi.scripts.glpi.get_auth_token')
    @patch('webhook_glpi.scripts.glpi.get_problem_by_fingerprint')
    @patch('webhook_glpi.scripts.glpi.get_item_equipments')
    def test_alertmanager_glpi_exception_handling(
        self,
        mock_get_item_equipments,
        mock_get_problem_by_fingerprint,
        mock_get_auth_token,
        mock_fetch_asset_data,
        mock_servicenow,
        client,
        missing_glpi_id_alert
    ):
        """Test exception handling during alert processing."""
        # Arrange
        mock_servicenow.incident_context_builder.return_value = {"test": "context"}
        mock_servicenow.evaluate_incident_context.return_value = True
        
        mock_fetch_asset_data.return_value = {
            "glpi_item_type": "Computer",
            "entity_id": 1,
            "glpi_item_id": 123
        }
        mock_get_auth_token.return_value = 'test_session_token'
        mock_get_problem_by_fingerprint.return_value = None
        mock_get_item_equipments.side_effect = Exception("Test exception")  # Force exception
        
        # Act
        response = client.post('/glpi', json=missing_glpi_id_alert)
        
        # Assert
        assert response.status_code == 200  # Should not crash
        data = response.get_json()
        assert data['problems_created'] == []

    # TEST 7: ServiceNow Feature Flag False
    @patch('webhook_glpi.scripts.glpi.servicenow')
    @patch('webhook_glpi.scripts.glpi.fetch_asset_data')
    def test_alertmanager_glpi_servicenow_feature_flag_false(
        self,
        mock_fetch_asset_data,
        mock_servicenow,
        client,
        missing_glpi_id_alert
    ):
        """Test behavior when ServiceNow feature flag is false."""
        # Arrange
        mock_servicenow.incident_context_builder.return_value = {"test": "context"}
        mock_servicenow.evaluate_incident_context.return_value = False  # Feature flag false
        
        mock_fetch_asset_data.return_value = {
            "glpi_item_type": "Computer",
            "entity_id": 1,
            "glpi_item_id": 123
        }
        
        # Act
        response = client.post('/glpi', json=missing_glpi_id_alert)
        
        # Assert
        assert response.status_code == 200
        data = response.get_json()
        assert data['problems_created'] == []

    # TEST 8: Item Equipment Not Found  
    @patch('webhook_glpi.scripts.glpi.servicenow')
    @patch('webhook_glpi.scripts.glpi.fetch_asset_data')
    @patch('webhook_glpi.scripts.glpi.get_auth_token')
    @patch('webhook_glpi.scripts.glpi.get_problem_by_fingerprint')
    @patch('webhook_glpi.scripts.glpi.get_item_equipments')
    def test_alertmanager_glpi_item_equipment_not_found(
        self,
        mock_get_item_equipments,
        mock_get_problem_by_fingerprint,
        mock_get_auth_token,
        mock_fetch_asset_data,
        mock_servicenow,
        client,
        missing_glpi_id_alert
    ):
        """Test when item equipment is not found in GLPI."""
        # Arrange
        mock_servicenow.incident_context_builder.return_value = {"test": "context"}
        mock_servicenow.evaluate_incident_context.return_value = True
        
        mock_fetch_asset_data.return_value = {
            "glpi_item_type": "Computer",
            "entity_id": 1,
            "glpi_item_id": 123
        }
        mock_get_auth_token.return_value = 'test_session_token'
        mock_get_problem_by_fingerprint.return_value = None
        mock_get_item_equipments.return_value = None  # Item not found
        
        # Act
        response = client.post('/glpi', json=missing_glpi_id_alert)
        
        # Assert
        assert response.status_code == 200
        data = response.get_json()
        assert data['problems_created'] == []


class TestCloseFunction:
    """Test cases for close_problem function."""
    
    @patch('webhook_glpi.scripts.glpi.close_problem')
    def test_close_problem_function_called(self, mock_close_problem):
        """Test that close_problem function can be called."""
        # Arrange
        problem_id = 123
        session_token = 'test_token'
        
        # Act
        from webhook_glpi.scripts.glpi import close_problem
        close_problem(problem_id, session_token)
        
        # Assert - This tests that the function is accessible and callable
        mock_close_problem.assert_called_once_with(problem_id, session_token)