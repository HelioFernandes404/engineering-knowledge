import json
from typing import Union
import requests
from webhook_glpi.utils import get_api_token, get_glpi_host, get_user_token, get_account_sid,get_auth_token_twilio,get_from_number,get_to_number
import os
from loguru import logger
import os

import boto3
from botocore.exceptions import ClientError
from memoizit import Memoizer

from webhook_glpi.scripts.metrics import sf_id_lookup_failed_counter , request_dynamodb_counter,resolved_problem_counter

m = Memoizer(backend="redis")

@m.memoize(
    expiration=60*60*1,
)
def get_auth_token(entity_id):
    token=get_user_token()
    app_token=get_api_token()
    url=get_glpi_host()

    headers = {
        'Authorization': f'user_token {token}',
        'App-Token': f'{app_token}'
    }
    logger.debug(f"Sending request: {headers}")


    # Make the GET request with query string parameters
    response = requests.get(f'{url}/initSession', headers=headers)
    logger.debug(f"Status code: {response.status_code}")
    response_data = response.json()
    
    logger.debug(f"Got response {response.json()}")
    if response.status_code != 200:
        logger.error(f'Failed to receive authentication token from GLPi. Status code: {response.status_code}')
        logger.error('Failed to parse response from GLPi when getting authentication token.')
    if 'session_token' not in response_data:
        logger.error('Failed to process response received from GLPi. No session token found.')
    return response_data['session_token']

@m.memoize(
    expiration=60*60*1,
    unique_on=['entity_id'],
)
def get_entities_name(entity_id,session_token):
    url = get_glpi_host()
    app_token = get_api_token()
    headers = {
        'Session-Token': session_token,
        'App-Token': app_token
    }
    
    response = requests.get(f'{url}/Entity/{entity_id}', headers=headers)
    if response.status_code == 200:
        entity_info = response.json()
        return entity_info["name"]
    else:
        logger.warning(f"Failed to get names entities for entity {entity_id}. Status code: {response.status_code}")

        return{}

def translate_item_type_to_glpi_terminology(item_type): 

    item_type_to_glpi = {
        'networkequipment': 'NetworkEquipment',
        'link_wan': 'NetworkEquipment',
        'software':'Software',
        'computer':'Computer'
    }
    return item_type_to_glpi[item_type] 

@m.memoize(
    expiration=60*15,
)
def get_item_problems(session_token):
    api_url = f'{get_glpi_host()}/Item_Problem'
    headers = {
        'Session-Token': session_token,
        'App-Token': get_api_token()
    }
    problems = []
    offset = 0
    page = 1
    per_page = 50
    # Fazer a requisição GET para buscar todos os problemas
    while len(problems)<100:
        params = {
            'start':offset,
            'limit':per_page
        }
        response = requests.get(f"{api_url}?range=0-99999", headers=headers,params=params)
        logger.debug(f"Status code: {response.status_code}")
    
        if response.status_code == 200:
            data = response.json()

            if not data:
                break
            problems.extend(data)
            if len(data) < per_page:
                break
            page += 1
        else:
            print(f"Falha ao buscar problemas. Status Code: {response.status_code}")
            print("Detalhes do erro:", response.text)
            break

    return problems

@m.memoize(
    expiration=60*60*24*3,
)
def get_problem_by_fingerprint(fingerprint,session_token):
    logger.debug(f"Looking up problems with fingerprint: {fingerprint}")
    url = get_glpi_host()
    headers = {
        'Session-Token': session_token,
        'App-Token': get_api_token()
    }
    request_url = f'{url}PluginFieldsProblemfingerprint?searchText[fingerprintfield]={fingerprint}'
    logger.debug(f'Using request URL: {request_url}')
    response = requests.get(request_url, headers=headers)
    logger.debug(json.dumps(response.json(),indent=4))
    if response.status_code == 200:

        json_resp = response.json()

        if len(json_resp) > 0:
            return json_resp[0]
        
        return json_resp
    
    else:
        logger.error(f"Failed to fetch problem by fingerprint {fingerprint}. Status code: {response.status_code}")
        return None


def close_problem(problem_id, session_token):
    url = get_glpi_host()
    headers = {
        'Session-Token': session_token,
        'App-Token': get_api_token(),
        'Content-Type': 'application/json'
    }
    data = {
        "input": {
            "id": problem_id,
            "status": 5  # 5 = Fechado
        }
    }
    response = requests.put(
        os.path.join(get_glpi_host(), 'Problem'),
        headers=headers,
        json=data
    )
    if response.status_code == 200:
        logger.info(f"Problem {problem_id} closed successfully.")
        return True
    else:
        logger.error(f"Failed to close problem {problem_id}. Status code: {response.status_code}")
        return False
        
def assign_ticket_to_user(ticket_id, session_token,glpi_item_id,glpi_item_type, user_id=2874, category_id=2800):
    url = get_glpi_host()
    headers = {
        'Session-Token': session_token,
        'App-Token': get_api_token(),
        'Content-Type': 'application/json'
    }
    data = {
            "input": {
                "tickets_id": ticket_id,
                "users_id": 3665,  # ID do usuário para atribuir o ticket
                "type": 1,  # 1 = Atribuído (responsável pelo ticket)
                "use_notification": True  # Opcional: envia notificação
            }
        }
    response = requests.post(f'{get_glpi_host()}/Ticket_User', headers=headers, json=data)
    if response.status_code == 200 or response.status_code == 201:
        logger.success(f"Ticket {ticket_id} successfully linked to User {data['input']['users_id']}")




    location = None
    response = requests.get(f'{url}/{glpi_item_type}/{glpi_item_id}', headers=headers)
    if response.status_code == 200:
        data = response.json()
        location = data.get('locations_id','')
    data = {
        "input": {
            "id": ticket_id,
            "_users_id_assign": user_id,  # ID do usuário para atribuir o ticket
            "itilcategories_id": category_id,
            "locations_id": location  # ID da localização (opcional)
        }
    }
    response = requests.put(f'{url}/Ticket/{ticket_id}', headers=headers, json=data)
    if response.status_code == 200:
        logger.info(f"Ticket {ticket_id} assigned to user {user_id} (predefined resolver).")
        data = {
            "input": {
                "tickets_id": ticket_id,
                "users_id": 3665,  # ID do usuário para atribuir o ticket
                "type": 1,  # 1 = Atribuído (responsável pelo ticket)
                "use_notification": True,
                '_users_id_assign': 2874,  # ID do usuário para atribuir o ticket
            }
        }
        return True
    logger.error(f"Failed to assign ticket {ticket_id} to user {user_id}. Status code: {response.status_code}")
    return False
def close_ticket(
    ticket_id,
    session_token,
    solution_content="Ticket resolvido via automação",
    group_id=62,  # ID do grupo técnico (negativo)
    user_id=3665      # ID do usuário responsável
):
    url = get_glpi_host()
    headers = {
        'Session-Token': session_token,
        'App-Token': get_api_token(),
        'Content-Type': 'application/json'
    }

    # 1. Criar uma tarefa associada ao ticket
    task_data = {
        "input": {    # Categoria técnica (ajuste conforme seu GLPI)
            "content": "Tarefa técnica para resolução do chamado",
            "groups_id_assign": int(group_id),  # Campo pode variar conforme versão GLPI
            "users_id_assign": int(user_id),
            "state": 1, # 1 = Em andamento
            "is_private": False
        }
    }
    
    task_response = requests.put(f'{url}/Ticket/{ticket_id}/TicketTask', headers=headers, json=task_data)
    if task_response.status_code != 200:
        logger.error(f"Falha ao criar tarefa para o ticket {ticket_id}. Status: {task_response.status_code}")
        return False
    
    logger.info(f"Tarefa criada com sucesso para o ticket {ticket_id}")

    # 2. Atribuir grupo técnico ao ticket (opcional, se já definido na tarefa)
    assign_data = {
        "input": {
            "id": ticket_id,
            "_groups_id_assign": group_id
        }
    }
    assign_response = requests.put(f'{url}/Ticket/{ticket_id}', headers=headers, json=assign_data)
    if assign_response.status_code != 200:
        logger.error(f"Falha ao atribuir grupo ao ticket {ticket_id}. Status: {assign_response.status_code}")
        return False

    # 3. Adicionar solução
    solution_data = {
        "input": {
            "itemtype": "Ticket",
            "items_id": ticket_id,
            "solutiontypes_id": 1,  # 1 = Solução permanente
            "content": solution_content,
            "status": 3             # 3 = Solução aceita
        }
    }
    solution_response = requests.post(f'{url}/ITILSolution/', headers=headers, json=solution_data)
    if solution_response.status_code != 201:
        logger.error(f"Falha ao adicionar solução ao ticket {ticket_id}. Status: {solution_response.status_code}")
        return False

    # 4. Fechar o ticket (status = 5)
    ticket_data = {
        "input": {
            "id": ticket_id,
            "status": 5,           # 5 = Resolvido
            "solution": solution_content
        }
    }
    close_response = requests.put(f'{url}/Ticket/{ticket_id}', headers=headers, json=ticket_data)
    
    if close_response.status_code == 200:
        logger.info(f"Ticket {ticket_id} fechado com sucesso.")
        return True
    
    logger.error(f"Falha ao fechar ticket {ticket_id}. Status: {close_response.status_code}")
    return False


def verify_duplicates(glpi_item_id, glpi_item_type, SESSION_TOKEN, status_alert, alert_name):
    item_problems = get_item_problems(SESSION_TOKEN)
    
    logger.info(f"Verifying duplicates for problems with item_id {glpi_item_id} and item_type {glpi_item_type}")
    logger.debug(f"Alert name: {alert_name}")
    logger.debug(f"Alert status: {status_alert}")
    # Filtra problemas relacionados ao item e tipo especificados
    problems_id = [
        problem['problems_id']
        for problem in item_problems
        if problem["items_id"] == int(glpi_item_id) and problem["itemtype"] == glpi_item_type
    ]
    # Busca os detalhes de cada problema identificado
    parsed_problems = [get_problem_by_id(_id, SESSION_TOKEN) for _id in problems_id]
    logger.debug("Matched problems.")
    # Verifica o status dos problemas
    for problem in parsed_problems:

        logger.debug(problem)
        if problem['name'] != alert_name:
            # ignore problems that don't have the same
            continue

        if problem.get('status') not in [5, 6]:  # Status diferentes de "fechado" ou "resolvido"
            logger.error(f'Problem {problem["id"]} already open for item {glpi_item_id} of type {glpi_item_type}')     

            if status_alert == 'resolved':
                headers = {
                    'Session-Token': SESSION_TOKEN,
                    'App-Token': get_api_token()
                }
                glpi_data = {
                    "input": {
                        "id": problem["id"],
                        "status": 5
                    }
                }
                response = requests.put(
                    os.path.join(get_glpi_host(), 'Problem'),
                    headers=headers,
                    json=glpi_data
                )
                if response.status_code == 200:
                    # Busca o ID do ticket vinculado ao problema
                    ticket_id = get_ticket_id_by_problem(problem["id"], SESSION_TOKEN)
                    if ticket_id:
                        if assign_ticket_to_user(ticket_id,SESSION_TOKEN,glpi_item_id,glpi_item_type):
                            if close_ticket(ticket_id, SESSION_TOKEN):
                                logger.info(f"Problem {problem['id']} closed, ticket {ticket_id} assigned to user 3665, updated to category 2800, and closed successfully.")
                                return True  # Retorna False após fechar o problema
                    return True  # Retorna True se houve falha ao fechar o problema
                return True  # Retorna True se houve falha ao fechar o problema
            return True  # Retorna True ao encontrar duplicata sem fechar o problema
    # Nenhuma duplicata encontrada
    return False







@m.memoize(
    expiration=60*60*3,
)
def get_item_equipments(entity_id, id_item, item_type, session_token, visited_entities=None):
    """Recursively search for an item in the given entity and all its sub-entities using DFS, handling pagination and avoiding revisiting entities."""
    if visited_entities is None:
        visited_entities = set()

    if entity_id in visited_entities:
        logger.debug(f"Entity {entity_id} has already been visited. Skipping...")
        return None
    

    item_type = translate_item_type_to_glpi_terminology(item_type)

    url = get_glpi_host()
    app_token = get_api_token()
    headers = {
        'Session-Token': session_token,
        'App-Token': app_token,
        'Content-Type': 'application/json'
    }
    request_url = os.path.join(url,item_type,str(id_item))
    response = requests.get(request_url, headers=headers)
    logger.debug(f"Status code: {response.status_code} for entity {entity_id}")

    if response.status_code in [200, 206]:
        data = response.json()
        return data
    else:
        logger.warning(f"Failed to retrieve items for entity {entity_id}. Status code: {response.status_code}")
        return

@m.memoize(
    expiration=60*60*24*3,
)
def get_problem_by_id(id_item,session_token):
    url = get_glpi_host()
    app_token = get_api_token()
    headers = {
        'Session-Token': session_token,
        'App-Token': app_token
    }
    response = requests.get(f'{url}/Problem/{id_item}',headers=headers)
    #logger.debug(f"Status code: {response.status_code}")
    if response.status_code != 404:    
        response_data = response.json()
        return response_data
    logger.error('Failed to parse response from GLPi when getting items Problems.')
    return []

@m.memoize(
    expiration=60*60*6,
    unique_on=['entity_id'],
)
def get_sub_entities(entity_id, session_token):
    """Get the sub-entities of a given entity in GLPI."""
    logger.debug(f"Getting sub-entities of entity {entity_id}...")
    url = get_glpi_host()
    app_token = get_api_token()
    headers = {
        'Session-Token': session_token,
        'App-Token': app_token
    }
    
    response = requests.get(f'{url}/Entity/{entity_id}', headers=headers)
    if response.status_code == 200:
        entity_info = response.json()
        sons_cache = entity_info.get('sons_cache', '{}')
        sub_entities = json.loads(sons_cache)
        return sub_entities
    else:
        logger.warning(f"Failed to get sub-entities for entity {entity_id}. Status code: {response.status_code}")
        return {}

# DynamoDB table name

# Query parameters
  # Replace with your partition key attribute name
#PARTITION_KEY_VALUE = "sf-gnd-rj-00001"  # Replace with the actual partition key value
def item_type_to_str(item_type):
    SESSION_TOKEN = get_auth_token('nope') # data["alerts"].get('labels', {}).get('glpi_entity_id'))
            
    session_token = SESSION_TOKEN
    headers = {
        'Session-Token': session_token,
        'App-Token': get_api_token()
    }
    response = requests.get(f'{get_glpi_host()}networkequipment/763', headers=headers)
    if response.status_code == 200:
        logger.debug(f'Item assigned to problem on GLPI: {response.json()}')
        return response.json()
    else:
        logger.debug(f'Failed to Item assigned to problem on GLPI: {response.json()}')


@m.memoize(
    expiration=60*60*24,
)
def get_glpi_info_by_sf_id(sf_id):
    logger.debug(f"Fetching glpi data for systemframe_id: {sf_id}")
    try:
        TABLE_NAME = "systemframe-configs"
        PARTITION_KEY_NAME = "systemframe_id"
        # Initialize the DynamoDB client
        dynamodb = boto3.resource('dynamodb',region_name='us-east-1')
        table = dynamodb.Table(TABLE_NAME)
        
        # Perform the query
        request_dynamodb_counter.add(1)
        response = table.query(
            KeyConditionExpression=f"{PARTITION_KEY_NAME} = :pkval",
            ExpressionAttributeValues={
                ":pkval": sf_id
            }
        )

        # Print the items retrieved
        items = response.get('Items', [])
        if items:
            item = items[0]  # Assuming we take the first item if multiple exist

            result = {
                "glpi_item_id": int(item.get("glpi_item_id")),
                "glpi_entity_id": int(item.get("glpi_entity_id")),
                "glpi_item_type": str(item.get("glpi_item_type"))
            }
            logger.debug(f"Data found: {result}")
            
            return result
        else:
            logger.warning("No data found.")

    except ClientError as e:
        logger.debug(f"Error querying the table: {e}")
    
def fetch_asset_data(alert: dict) -> Union[dict, None]:
    try:
        export_systemframe_id = alert.get('labels',{}).get('exported_systemframe_id')
        logger.debug(export_systemframe_id)
        if export_systemframe_id == "missing":
            logger.warning("exported_systemframe_id is missing, literally.")
            export_systemframe_id = None
        systemframe_id = alert.get('labels',{}).get('systemframe_id')
        entity_id = alert.get('labels', {}).get('glpi_entity_id')
        glpi_item_id = alert.get('labels', {}).get('glpi_item_id')
        glpi_item_type = alert.get('labels', {}).get('glpi_item_type')
        sf_id = export_systemframe_id or systemframe_id
        if sf_id:
            values_glpi = get_glpi_info_by_sf_id(sf_id)
            entity_id = values_glpi.get('glpi_entity_id')
            glpi_item_id = values_glpi.get('glpi_item_id')
            glpi_item_type = values_glpi.get('glpi_item_type')
            return {
                    "glpi_item_id": glpi_item_id,
                    "entity_id": entity_id,
                    "glpi_item_type": glpi_item_type
            }
        

        if glpi_item_id and glpi_item_type and entity_id:
                
            return {
                    "glpi_item_id": glpi_item_id,
                    "entity_id": entity_id,
                    "glpi_item_type": glpi_item_type
            }
            
        logger.warning(f"Could not find asset data for alert {alert.get('labels',{}).get('alertname','')}")
        
    except Exception as e:
        sf_id_lookup_failed_counter.add(1)
        logger.error(f"An error occurred while fetching asset data: {e}")
        return None
