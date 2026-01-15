import os
from flask import json, jsonify
from loguru import logger
import requests
from webhook_glpi.utils import get_discord_webhook
from webhook_glpi.scripts.metrics import post_discord_counter,post_failed_discord_counter
def alertmanager_discord(request):
    try:
        logger.info("Request on /discord")
        data = request.json
        if not data or 'alerts' not in data:
            logger.error("No alerts found in request.")
            return jsonify({"error": "No alerts found"}), 400

        has_called = False
        for alert in data['alerts']:
            status = alert.get('status', '').capitalize()
            description = alert.get('annotations', {}).get('description', 'No description provided')
            summary = alert.get('annotations', {}).get('summary', 'No summary provided')
            labels = alert.get('labels', {})
            starts_at = alert.get('startsAt', '')
            ends_at = alert.get('endsAt', '')
            generator_url = alert.get('generatorURL', 'No URL provided')

            logger.info("About to send webhook to Discord")

            # Define the webhook URL
            webhook_url = get_discord_webhook()

            alert_content = (
                f"**Alert Status**: `{status}`\n"
                f"**Summary**: {summary}\n"
                f"**Description**: {description}\n"
                f"**Start Time**: `{starts_at}`\n"
                f"**End Time**: `{ends_at}`\n"
                f"**Labels**:\n"
                f"```json\n{json.dumps(labels, indent=4)}\n```\n"
            )

            # Define the payload for the message
            payload = {
                'content': alert_content,
                'username': 'Systemframe Alerts',  # Optional: Change the username of the bot that sends the message
                'avatar_url': 'https://example.com/avatar.png'  # Optional: Change the avatar of the bot
            }

            discord_webhook_response = requests.post(webhook_url, json=payload)
            logger.debug(f"Response: {discord_webhook_response.text}")
            logger.debug(f"Status Code: {discord_webhook_response.status_code}")
            
            # Check for successful response
            if discord_webhook_response.status_code == 204:  # 204 is Discord's "No Content" response for success
                post_discord_counter.add(1)
                logger.info("Alert sent to Discord successfully.")
                has_called = True
            else:
                logger.error("Failed to send alert to Discord.")
                return jsonify({"error": "Failed to send alert"}), discord_webhook_response.status_code

        if has_called:
            return jsonify({"status": "Alerts sent to Discord successfully"}), 200
        else:
            post_failed_discord_counter.add(1)
            return jsonify({"error": "No alerts were processed"}), 400

    except Exception as e:
        post_failed_discord_counter.add(1)
        logger.error(f"Falha ao realizar a criação do webhook: {e}")
        return jsonify({"error": "Falha ao realizar a criação do webhook", "details": str(e)}), 500
