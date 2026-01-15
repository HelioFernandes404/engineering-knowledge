import json
import requests
from ldclient import Context

from webhook_glpi.scripts.config import api_config

feature_flag_client = api_config.initialize_ld_client()


class ServiceNowIncident:
    def __init__(self):
        self.instance = api_config.servicenow_instance
        self.api_key = api_config.servicenow_api_key
        self.base_url = f'https://{self.instance}.service-now.com/api/now/table/incident'
        self.headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'x-sn-apikey': self.api_key
        }

    def incident_context_builder(self, context_dict):

        context = context_dict | {'key': 'api-servicenow', 'kind': 'user'}
        user_context = Context.from_dict(context)
        
        return user_context


    def evaluate_incident_context(self, context):
        context_enabled = feature_flag_client.variation(api_config.feature_incident_context_key, context, False)

        return context_enabled
    

    def handle_incident_data(self, labels, annotations, alert_timestamp):

        incident_urgency = "1" if labels.get('severity') == 'critical' else ("2" if labels.get('severity') == 'warning' else "3")
        incident_impact = "1" if labels.get('severity') == 'critical' else ("2" if labels.get('severity') == 'warning' else "3")

        servicenow_data = {
            "short_description": annotations.get('summary', labels.get('alertname', 'Unknown Alert')),
            "description":alert_timestamp,
            "urgency": incident_urgency,
            "impact": incident_impact,
        }

        incident_data = servicenow_data | api_config.servicenow_defaults

        return incident_data


    def create_incident(self, incident_data):
        """
        Create a new incident in ServiceNow
        
        Args:
            incident_data (dict): The incident data to be created
                Example format:
                {
                    "caller_id": "svcnoc",
                    "contact_type": "Self-service",
                    "incident_state": "1",
                    "short_description": "Servidor xpto reiniciado",
                    "description": "2025-04-08 23:07:12",
                    "category": "Infrastructure",
                    "subcategory": "Servers",
                    "urgency": "3",
                    "impact": "3",
                    "priority": "4",
                    "assignment_group": "G_SN_DATACENTER_TI"
                }
                
        Returns:
            tuple: (success, response_data or error_message)
        """
        try:

            response = requests.post(
                self.base_url,
                headers=self.headers,
                data=json.dumps(incident_data),
                timeout=10
            )
            
            response.raise_for_status()

            # print(f"Status code: {response.status_code}")
            # print(f"Response body: {response.text}")

            return True, response.json()
        
        except requests.exceptions.HTTPError as http_err:
            error_message = f"HTTP error occurred: {http_err}"
            if response.text:
                try:
                    error_details = response.json()
                    error_message += f"\nDetails: {error_details}"
                except json.JSONDecodeError:
                    error_message += f"\nResponse: {response.text}"
            return False, error_message
            
        except requests.exceptions.ConnectionError:
            return False, "Failed to connect to ServiceNow instance"
            
        except requests.exceptions.Timeout:
            return False, "Request timed out"
            
        except requests.exceptions.RequestException as err:
            return False, f"Error occurred: {err}"
            
        except json.JSONDecodeError:
            return False, "Failed to parse ServiceNow response"