import os
import ldclient
from ldclient.config import Config

from dotenv import load_dotenv

load_dotenv()

class APIConfig:
    def __init__(self):

        self.port = int(os.getenv('PORT', "5000"))
        self.api_key = os.getenv('API_KEY')
        self.servicenow_api_key = os.getenv('SERVICENOW_API_KEY')
        self.servicenow_instance = os.getenv('SERVICENOW_INSTANCE')
        self.launchdarkly_sdk_key = os.getenv('LAUNCHDARKLY_SDK_KEY')
        self.feature_incident_context_key = os.getenv('FEATURE_INCIDENT_CONTEXT_KEY', "incident_availability" )
        self.feature_incident_availability_key = os.getenv('FEATURE_INCIDENT_AVAILABILITY_KEY')
        self.feature_customer_availability_key = os.getenv('FEATURE_CUSTOMER_AVAILABILITY_KEY')

        self.servicenow_defaults = {
            "caller_id": os.getenv('SERVICENOW_CALLER_ID'),
            "incident_state": os.getenv('SERVICENOW_INCIDENT_STATE'),
            "category": os.getenv('SERVICENOW_CATEGORY'),
            "subcategory": os.getenv('SERVICENOW_SUB_CATEGORY'),
            "contact_type": os.getenv('SERVICENOW_CONTACT_TYPE'),
            "assignment_group": os.getenv('SERVICENOW_ASSIGMENT_GROUP')
        }

    def initialize_ld_client(self):
        ldclient.set_config(Config(self.launchdarkly_sdk_key))

        if ldclient.get().is_initialized():
            return ldclient.get()
        else:
            raise RuntimeError("LaunchDarkly SDK failed to initialize.")

api_config = APIConfig()
