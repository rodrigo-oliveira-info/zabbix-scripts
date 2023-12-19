import requests
import sys
import json

URL_BASE = ""
AUTH_KEY = ""
NGINX_USER_NAME = ""
NGINX_PASSWORD = ""

headers = {'Content-Type' : 'application/json', 'Authorization' : f'{AUTH_KEY}', 'accept' : 'application/json'}

def find_incident_id(name):
	url_incident = URL_BASE + "/api/incidents/incidents/"
	response = requests.get(url_incident, headers=headers)
	print(response.text)

	if 200 <= response.status_code <= 299:
		data = response.json()

		more_to_search = True
		while (more_to_search):
			for incident in data["results"]:
				if incident["title"] == name and incident["status"] != "resolved":
					incident_id = incident["id"]
					return incident_id
			if response.json()["next"]:
				url_incident = response.json()["next"]
				response = requests.get(url_incident, headers=headers)
				print(response.text)
				data = response.json()
			else:
				more_to_search = False

		return None
	else:
		return None

def update_incident_status(incident_id, product_id):
	if incident_id:
		url_update = URL_BASE + "/api/incidents/incident-updates/"
		update_data = {
	        'user' : 1,
	        'incident' : incident_id,
	        'new_status': True,
	        'text': 'Resolvido',
	        'status': 'resolved',
		}
		update_response = requests.post(url_update, headers=headers, data=json.dumps(update_data))

		url_incident = URL_BASE + "/api/incidents/incidents/" + str(incident_id) + "/?=format=json"
		incident_data = {
			'status' : 'resolved',
		}
		incident_response = requests.patch(url_incident, headers=headers, data=json.dumps(incident_data))

		url_component = URL_BASE + "/api/components/components/" + str(product_id) + "/"
		component_data = {
			'status' : 'operational'
		}
		component_response = requests.patch(url_component, headers=headers, data=json.dumps(component_data))

name_tag = sys.argv[1] if len(sys.argv) > 1 else None

product_id_tag = sys.argv[2] if len(sys.argv) > 2 else None

incident_id = find_incident_id(name_tag)

if incident_id:
	print("Incidente encontrado: " + str(incident_id))
	update_incident_status(incident_id, product_id_tag)
else:
	print("Incidente não encontrado.")
