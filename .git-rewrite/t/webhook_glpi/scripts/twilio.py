from loguru import logger
import requests
import json
from twilio.rest import Client
from twilio.twiml.voice_response import VoiceResponse
from flask import Flask, request, jsonify
from webhook_glpi.utils import get_account_sid, get_api_token, get_glpi_host, get_from_number, get_to_number, get_auth_token_twilio

def alertmanager_twilio(request, from_number=get_from_number(), to_number=get_to_number(), account_sid=get_account_sid(), auth_token=get_auth_token_twilio()):
    try:
        logger.info("Request on /make_call")
        data = request.json
        logger.debug(data)
        if not data or 'alerts' not in data:
            return jsonify({'error': 'Invalid data received'}), 400
        logger.debug("Alerts from Alertmanager")
        logger.debug(json.dumps(data['alerts'], indent=4))
        has_called = False
        for alert in data['alerts']:
            cliente = alert.get('labels', {}).get('host_group')
            client = Client(account_sid, auth_token)
            response = VoiceResponse()
            response.pause(length=10)
            response.play(digits="1")
            response.pause(length=20)
            response.play(digits="3")
            response.pause(length=15)
            response.play(digits="1")
            response.pause(length=30)
            response.say(f"Atenção! Alerta SystemFreime! Este é um comunicado importante informando o incidente do cliente {cliente}. "
                         "Foi detectado um problema. Por favor, verifique o painel de chamados para mais detalhes. "
                         "Esta mensagem é gerada automaticamente. A SystemFreime agradece.",
                         voice='alice', language='pt-BR')

            call = client.calls.create(
                twiml=response,
                from_=from_number,
                to=to_number
            )
            logger.info("Ligação realizada com sucesso.")
            return jsonify({'message': 'Ligação realizada com sucesso', 'call_sid': call.sid}), 200
    except Exception as e:
        logger.error(f"Falha ao realizar a ligação: {e}")
        return jsonify({'error': str(e)}), 500
