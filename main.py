import os
import json
import base64
import requests

# Read the configuration
with open('config.json', 'r') as config_file:
    config_data = config_file.read()
config = json.loads(config_data)

def log_visit(event, context):
    # Decode the JSON event data
    event_string = base64.b64decode(event['data']).decode('utf-8')
    event_data = json.loads(event_string)
    print(event_string)

    # Build the Matomo request
    url = config['MATOMO_URL']
    params = {
        'idsite':config['SITE_ID'],
        'rec':1,
        'apiv':1,
        'send_image':0,
        'url':'http://{}{}'.format(
            event_data['protoPayload']['host'],
            event_data['protoPayload']['resource']),
        'ua': event_data['protoPayload'].get('userAgent',''),
        'cip':event_data['protoPayload']['ip'],
    }

    # Send the Matomo API request
    response = requests.post(url, params=params)
    print(response.status_code)
    print(response.content)
