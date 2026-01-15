import os
from dataclasses import dataclass
import json

@dataclass
class GLPICredential:
    app_token: str
    user_token: str
    entity_id: str
    
#@dataclass
class GLPICredentials:
    creds: list[GLPICredential] = []

    def read_glpi_credentials(self, file_name: str = "credentials.json"):
        
        with open(file_name, "r") as json_file:
            credz = json.load(json_file)
            app_token = credz["app_token"]
            credentials = []
            for item in credz["entity_users"]:
                cred = GLPICredential(
                    app_token, 
                    item["user_token"], 
                    item["entity_id"]
                )
                credentials.append(cred)
            self.creds = credentials

    def get_user_entity_creds(self, entity_id) -> GLPICredential | None:
        for credential in self.creds:

            if int(credential.entity_id) == entity_id:
                return credential



