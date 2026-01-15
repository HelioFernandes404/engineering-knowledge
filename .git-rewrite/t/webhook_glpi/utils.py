import os

def get_api_token():
    return os.environ["API_TOKEN"]

def get_user_token():
    return os.environ["USER_TOKEN"]

def get_glpi_host():
    url = os.environ["API_HOST_GLPI"] 
    # add trailing slash whether it exists or not
    url = url.rstrip('/') + '/'
    return url
    
def get_account_sid():
    return os.environ["ACCOUNT_SID"]

def get_auth_token_twilio():
    return os.environ["AUTH_TOKEN_TWILIO"]

def get_from_number():
    return os.environ.get("FROM_NUMBER","+15623520469")

def get_to_number():
    return os.environ.get("TO_NUMBER","+5508005802626")

def get_discord_webhook():
    return os.environ["DISCORD_WEBHOOK"]