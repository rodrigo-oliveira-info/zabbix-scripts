import requests
import json
import sys

def create_incident(name, status, body, impact_override, client_id, product_id, damage):
	URL_BASE = ""
	auth_key = ""
	NGINX_USER_NAME = ""
	NGINX_PASSWORD = ""

	user_id = 1
	headers = {'Content-Type' : 'application/json', 'Authorization' : f'Token {auth_key}'}

	# Atualizar Incident
	url_incident = URL_BASE + "/api/incidents/incidents/"
	components = []
	components.append(int(product_id))
	incident_data = {
		'status' : status,
		'title' : name,
		'impact': impact_override,
		'visibility' : True,
		'user' : user_id,
		'components' : components
	}
	incident_response = requests.post(url_incident, headers=headers, data=json.dumps(incident_data), auth=(NGINX_USER_NAME, NGINX_PASSWORD))
	incident_id = incident_response.json()['id']

	# Atualizar IncidentUpdate
	url_update = URL_BASE + "/api/incidents/incident-updates/"
	update_data = {
		'user' : user_id,
		'incident' : incident_id,
		'new_status': True,
		'text': body,
		'status': status
	}
	update_response = requests.post(url_update, headers=headers, data=json.dumps(update_data), auth=(NGINX_USER_NAME, NGINX_PASSWORD))

	# Atualizar Component
	url_component = URL_BASE + "/api/components/components/" + str(product_id) + "/"
	component_data = {
		'status': damage
	}
	component_response = requests.patch(url_component, headers=headers, data=json.dumps(component_data), auth=(NGINX_USER_NAME, NGINX_PASSWORD))

name_tag = sys.argv[1] if len(sys.argv) > 1 else None
status_tag = sys.argv[2] if len(sys.argv) > 2 else None
body_tag = sys.argv[3] if len(sys.argv) > 3 else None
impact_override_tag = sys.argv[4] if len(sys.argv) > 4 else None
client_id_tag = sys.argv[5] if len(sys.argv) > 5 else None
product_id_tag = sys.argv[6] if len(sys.argv) > 6 else None
damage_tag = sys.argv[7] if len(sys.argv) > 7 else None

if name_tag and status_tag and body_tag and impact_override_tag and product_id_tag:
    create_incident(name_tag, status_tag, body_tag, impact_override_tag, client_id_tag, product_id_tag, damage_tag)
else:
    print("Tags não fornecidas como argumentos.")
