from flask import Flask, request, jsonify
import os
import hashlib
import json
from loguru import logger
from typing import Union
import requests
from datetime import datetime
from webhook_glpi.scripts.utils import close_problem, fetch_asset_data, get_auth_token, get_glpi_info_by_sf_id, get_item_equipments, get_entities_name, get_problem_by_fingerprint,get_sub_entities,get_problem_by_id,get_item_problems,verify_duplicates
from webhook_glpi.utils import get_api_token, get_glpi_host, get_user_token, get_account_sid,get_auth_token_twilio,get_from_number,get_to_number
from webhook_glpi.scripts.metrics import glpi_problem_created, notification_received_counter,item_equipment_failed_counter, glpi_exception_counter
from webhook_glpi.scripts.create_incident import ServiceNowIncident

servicenow = ServiceNowIncident()

# Test the cache v2
def format_alert_content(alert):
    """
    Format alert content for GLPI (clean format without markdown)
    """
    labels = alert.get('labels', {})
    annotations = alert.get('annotations', {})
    
    # Get basic alert information
    status = alert.get('status', 'Unknown').capitalize()
    alert_name = labels.get('alertname', 'Unknown Alert')
    description = annotations.get('description', 'No description provided')
    summary = annotations.get('summary', alert_name)
    
    # Get severity for emoji selection
    severity = labels.get('severity', '').lower()
    
    # Choose emoji based on severity
    if severity == 'critical':
        severity_emoji = '🔥 Critical Alerts 🔥'
    elif severity == 'warning':
        severity_emoji = '⚠️ Warning Alerts ⚠️'
    elif severity == 'info':
        severity_emoji = 'ℹ️ Info Alerts ℹ️'
    else:
        severity_emoji = '🚨 Alerts 🚨'
    
    # Format timestamps
    starts_at = alert.get('startsAt', '')
    ends_at = alert.get('endsAt', '')
    
    # Start building the content
    content_parts = [
        severity_emoji,
        "",
        "---",
        f"🪪 {alert_name}",
        f"📝 {summary}",
        f"📖 {description}",
    ]
    
    # Add documentation link if available
    docs_url = labels.get('docs', '')
    if docs_url:
        content_parts.append(f"📚 Documentação do alerta ({docs_url})")
    
    # Add timestamps if available
    if starts_at:
        content_parts.append(f"🕐 Início: {starts_at}")
    
    if ends_at and status.lower() == 'resolved':
        content_parts.append(f"🕐 Fim: {ends_at}")
    
    # Add labels section with dynamic formatting
    content_parts.append("🏷 Labels:")
    
    # Sort labels for consistent display
    sorted_labels = sorted(labels.items())
    for key, value in sorted_labels:
        content_parts.append(f"• {key}: {value}")
    
    # Add annotations if there are additional ones beyond description and summary
    additional_annotations = {k: v for k, v in annotations.items() 
                            if k not in ['description', 'summary']}
    
    if additional_annotations:
        content_parts.append("📋 Annotations:")
        sorted_annotations = sorted(additional_annotations.items())
        for key, value in sorted_annotations:
            content_parts.append(f"• {key}: {value}")
    
    return "\n".join(content_parts)


def format_alert_title(alert):
    """
    Create a simple title for the alert (only alertname)
    """
    labels = alert.get('labels', {})
    
    alert_name = labels.get('alertname', 'Alert')
    
    return alert_name


def format_alert_content_minimal(alert):
    """
    Alternative minimal format for alerts (if you prefer simpler output)
    """
    labels = alert.get('labels', {})
    annotations = alert.get('annotations', {})
    
    alert_name = labels.get('alertname', 'Unknown Alert')
    description = annotations.get('description', 'No description provided')
    summary = annotations.get('summary', alert_name)
    severity = labels.get('severity', '').lower()
    
    # Choose appropriate emoji
    if severity == 'critical':
        emoji = '🔥'
    elif severity == 'warning':
        emoji = '⚠️'
    elif severity == 'info':
        emoji = 'ℹ️'
    else:
        emoji = '🚨'
    
    content_parts = [
        f"{emoji} {alert_name}",
        f"Resumo: {summary}",
        f"Descrição: {description}",
        ""
    ]
    
    # Add documentation if available
    docs_url = labels.get('docs', '')
    if docs_url:
        content_parts.append(f"Documentação: {docs_url}")
        content_parts.append("")
    
    # Add key labels
    important_labels = ['customer', 'severity', 'systemframe_id', 'host', 'instance']
    content_parts.append("Informações:")
    
    for label in important_labels:
        if label in labels:
            content_parts.append(f"• {label}: {labels[label]}")
    
    # Add all other labels
    other_labels = {k: v for k, v in labels.items() if k not in important_labels}
    if other_labels:
        content_parts.append("")
        content_parts.append("Labels adicionais:")
        for key, value in sorted(other_labels.items()):
            content_parts.append(f"• {key}: {value}")
    
    return "\n".join(content_parts)

def assign_ticket(ticket_data, problem_id, data_att):
    SESSION_TOKEN = get_auth_token('nope')  # data["alerts"].get('labels', {}).get('glpi_entity_id'))
    
    session_token = SESSION_TOKEN
    headers = {
        'Session-Token': session_token,
        'App-Token': get_api_token()
    }

    # Prepare the data to be sent to GLPI
    for id in problem_id:
        data = {
            'input': {
                'tickets_id': ticket_data['id'],
                'problems_id': id,
            }
        }

        response = requests.post(f'{get_glpi_host()}/Problem_Ticket', headers=headers, json=data)

        if response.status_code == 201:
            logger.success(f"Ticket {ticket_data['id']} successfully linked to Problem {problem_id}")
        else:
            logger.error(f"Failed to link Ticket {ticket_data['id']} to Problem {problem_id}")
            logger.debug(f"Status code: {response.status_code}")
            logger.debug(f"Response: {response.text}")
    data = {
        'input': {
            "tickets_id": ticket_data['id'],
            'items_id': data_att['items_id'],
            "itemtype": data_att['itemtype'],
        }
    }
    response = requests.post(f"{get_glpi_host()}/Ticket/{ticket_data['id']}/Item_Ticket", headers=headers, json=data)
    if response.status_code == 200 or response.status_code == 201:
        logger.success(f"Ticket {ticket_data['id']} successfully linked to Item {data_att['items_id']}")

    else:
        logger.error(f"Failed to link Ticket {ticket_data['id']} to Item {data_att['items_id']}")
        logger.debug(f"Status code: {response.status_code}")
        logger.debug(f"Response: {response.text}")
    
    return response


def create_ticket(glpi_data, data_att):
    SESSION_TOKEN = get_auth_token('nope') # data["alerts"].get('labels', {}).get('glpi_entity_id'))
            
    session_token = SESSION_TOKEN
    headers = {
        'Session-Token': session_token,
        'App-Token': get_api_token()
    }

    # Prepare the data to be sent to GLPI
    logger.debug(f"Request: {glpi_data}")
    glpi_data = {
        'input': {
            'name': glpi_data['input']['name'],
            'content': glpi_data['input']['content'],
            'urgency': 4,  # Adjust the priority as needed
            'entities_id': glpi_data['input']['entities_id'],
            'itilcategories_id': 2800
        }
    }
    response = requests.post(f'{get_glpi_host()}/Ticket', headers=headers, json=glpi_data)

    if response.status_code == 201 or response.status_code == 204:
    
        result = response.json()
        logger.success(f"Ticket created successfully with ID {result['id']}")

    return response

def generate_fingerprint(alert):

    alert_fingerprint = alert.get('fingerprint')
    starts_at = alert.get('startsAt')
    generator_url = alert.get('generatorURL')
    alert_name = alert.get('alertname')

    # Concatenate all fields into a single string for hashing
    fingerprint_source = f"{alert_name}|{alert_fingerprint}|{starts_at}|{generator_url}"

    logger.debug(f"Using string to generate fingerprint {fingerprint_source}")

    # Generate SHA256 hash
    sha256_hash = hashlib.sha256(fingerprint_source.encode('utf-8')).hexdigest()

    logger.info(f"Generated composite fingerprint: {sha256_hash}")

    return sha256_hash

def create_problem(glpi_data, fingerprint):
    SESSION_TOKEN = get_auth_token('nope') # data["alerts"].get('labels', {}).get('glpi_entity_id'))
            
    session_token = SESSION_TOKEN
    headers = {
        'Session-Token': session_token,
        'App-Token': get_api_token()
    }

    # Prepare the data to be sent to GLPI
    logger.debug(f"Request: {glpi_data}")

    response = requests.post(f'{get_glpi_host()}/Problem', headers=headers, json=glpi_data)

    if response.status_code == 201 or response.status_code == 204:
        glpi_problem_created.add(1)
        result = response.json()
        logger.success(f"Problem created successfully with ID {result['id']}")
        
        # Agora atualiza o campo adicional do plugin
        problem_id = result['id']
        fingerprint_data = {
            'input': {
                'items_id': problem_id,
                'fingerprintfield': fingerprint  # Valor padrão como solicitado
            }
        }
        
        # Atualiza o campo adicional
        fingerprint_response = requests.post(
            f'{get_glpi_host()}/PluginFieldsProblemfingerprint',
            headers=headers,
            json=fingerprint_data
        )
        
        if fingerprint_response.status_code in [200, 201]:
            logger.success(f"Fingerprint field successfully updated for Problem {problem_id}")
        else:
            logger.error(f"Failed to update fingerprint field for Problem {problem_id}")
            logger.debug(f"Status code: {fingerprint_response.status_code}")
            logger.debug(f"Response: {fingerprint_response.text}")

    return response

def assign_problem(data_att):
    SESSION_TOKEN = get_auth_token('nope') # data["alerts"].get('labels', {}).get('glpi_entity_id'))
            
    session_token = SESSION_TOKEN
    headers = {
        'Session-Token': session_token,
        'App-Token': get_api_token()
    }
    response = requests.post(f'{get_glpi_host()}/Item_Problem', headers=headers, json=data_att)
    if response.status_code == 201:
        logger.debug(f'Item assigned to problem on GLPI: {response.json()}')
        return response
    else:
        logger.debug(f'Failed to Item assigned to problem on GLPI: {response.json()}')


    
def alertmanager_glpi(request):
    logger.info("Request on /glpi")
    data = request.json
    logger.debug(data)
    if not data or 'alerts' not in data:
        return jsonify({'error': 'Invalid data received'}), 400
    
    params = {}
    # glpi.params['url'] = glpi.url_check_format(GLPI_URL)

    logger.debug("Alerts from Alertmanager")
    #logger.debug(json.dumps(data['alerts'], indent=4))
    problems_id = []  # Lista para armazenar os IDs dos problemas criados
    
    for alert in data['alerts']:
        labels = alert.get('labels', {})
        alert_name = alert.get('labels', {}).get('alertname', 'Alert')
        alert_group = alert.get('labels', {}).get('alertgroup', 'Alert')

        context = servicenow.incident_context_builder({"alert_name": alert_name, "alert_group": alert_group, "customer": labels.get('customer')})
        context_evaluation = servicenow.evaluate_incident_context(context)
        
        if not context_evaluation:
            logger.warning(f"Alert with name {alert_name} was not validated by the feature flag, skipping...")
            continue

        notification_received_counter.add(1)
        
        # Use the new formatting functions
        formatted_title = format_alert_title(alert)
        formatted_content = format_alert_content(alert)
        
        logger.info(f"Processing alert {formatted_title}")

        asset_data = fetch_asset_data(alert)
        if not asset_data:
            continue
        glpi_item_type = asset_data["glpi_item_type"]
        entity_id = asset_data["entity_id"]
        glpi_item_id = asset_data["glpi_item_id"]

        SESSION_TOKEN = get_auth_token(entity_id) # data["alerts"].get('labels', {}).get('glpi_entity_id'))

        if alert.get('status') == "resolved":
            fingerprint = generate_fingerprint(alert)

            problem_id = get_problem_by_fingerprint(fingerprint,SESSION_TOKEN)
            if problem_id:
                problem_id = problem_id["items_id"]
                if problem_id:
                    close_problem(problem_id, SESSION_TOKEN)
                    logger.debug(f"Problem {problem_id} closed successfully.")
                    continue
        else:
            fingerprint = generate_fingerprint(alert)

            problem_id = get_problem_by_fingerprint(fingerprint,SESSION_TOKEN)
            if problem_id:
                logger.warning("Firing alert already has a problem, skipping...")
                continue

        if not glpi_item_id:    
            logger.warning("Alert is missing glpi_item_id, skipping...")
            logger.debug(json.dumps(alert, indent=4))
            continue

        if not glpi_item_type:
            logger.warning("Alert is missing glpi_item_type, skipping...")
            logger.debug(json.dumps(alert, indent=4))
            continue
        # try catch foda-se
        try:
            item = get_item_equipments(entity_id, glpi_item_id, glpi_item_type, SESSION_TOKEN)
            if not item:
                item_equipment_failed_counter.add(1)
                logger.warning(f"Could not find item {glpi_item_id} of type {glpi_item_type}")
                continue
            entity_id = item["entities_id"]
            
                    
            glpi_data = {
                'input': {
                    'name': formatted_title,  # Use formatted title
                    'content': formatted_content,  # Use formatted content
                    'priority': 4,  # Adjust the priority as needed
                    'uuid': alert.get('fingerprint', ''),
                    'entities_id': entity_id
                }
            }
            fingerprint = generate_fingerprint(alert)
            response = create_problem(glpi_data,fingerprint)
            if response.status_code == 201 or response.status_code == 204:
                result = response.json()
                problem_id = result["id"]
                problems_id.append(problem_id)  # Adiciona o ID do problema à lista
                logger.debug(f'Problem created in GLPI: {result}')
                
                data_att = {
                    "input": {
                        "items_id": glpi_item_id,
                        "itemtype": glpi_item_type,
                        "problems_id": problem_id
                    }
                }
                resp = assign_problem(data_att)
                if resp.status_code == 201:
                    logger.debug(f'Item assigned to problem on GLPI: {resp.json()}')

                    
                else:
                    logger.error(f"Error while assigning Item to problem_id {problem_id}")
                    logger.debug(f"Status code: {resp.status_code}")
                    logger.debug(f"Response: {resp.text}")
                    logger.error("Impossivel criar problem. Item não existe no glpi")

        except Exception:
            logger.exception("We got exception:") 
            glpi_exception_counter.add(1)
            
    if len(problems_id) >0: 
        context = servicenow.incident_context_builder({"alert_name": alert_name, "customer": labels.get('customer')})
        context_evaluation = servicenow.evaluate_incident_context(context)
        if context_evaluation:
            ticket = create_ticket(glpi_data, data_att).json()
            if ticket.get('id'):
                logger.debug(f"Ticket created successfully with ID {ticket['id']}")
                assign_ticket(ticket, problems_id, data_att["input"])  # Assign ticket to problem
            else:
                logger.error(f"Error while creating Ticket to problem_id {problem_id}")
                logger.debug(f"Status code: {resp.status_code}")
                logger.debug(f"Response: {resp.text}")
                logger.error("Impossivel criar ticket. Item não existe no glpi")
        else:
            logger.debug("Skipping ticket creation due to feature flag evaluation being false.")
    else:
        logger.warning("Not creating ticket due to not existis problems createds.")

    return jsonify({'message': 'Alerts processed and sent to GLPI successfully', 'problems_created': problems_id}), 200
