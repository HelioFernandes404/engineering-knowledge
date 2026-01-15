from flask import Flask, request, jsonify
# import requests
from loguru import logger
# import json
# from dotenv import load_dotenv
# import os
# import uuid
# from webhook_glpi.credential import GLPICredentials
# from webhook_glpi.utils import get_api_token, get_glpi_host, get_user_token, get_account_sid,get_auth_token_twilio,get_from_number,get_to_number
# from twilio.rest import Client
# from twilio.twiml.voice_response import VoiceResponse
from webhook_glpi.scripts.glpi import alertmanager_glpi
from webhook_glpi.scripts.twilio import alertmanager_twilio
from webhook_glpi.scripts.discord import alertmanager_discord
from webhook_glpi.scripts.metrics import app_started_counter, app_stopped_counter
# load_dotenv()
import signal
import atexit

    
app = Flask(__name__) 
app_started_counter.add(1)
logger.info("application Start")
@app.route('/glpi', methods=['POST'])
def glpi_alert():
    return alertmanager_glpi(request)

@app.route('/discord', methods=['POST'])
def discord_alert():
    return alertmanager_discord(request)

@app.route('/twilio', methods=['POST'])
def twilio_alert():
    return alertmanager_twilio(request)

# Graceful shutdown
def handle_shutdown(*args):
    app_stopped_counter.add(1)
    logger.info("application Stopped")

if __name__ == '__main__':
    # Register the shutdown handler
    signal.signal(signal.SIGTERM, handle_shutdown)
    signal.signal(signal.SIGINT, handle_shutdown)
    atexit.register(handle_shutdown)
    
    app.run(host='0.0.0.0', port=5000, debug=True)
