import os
import json
import base64
import re
import requests

# Read the configuration
with open('config.json', 'r') as config_file:
    config_data = config_file.read()
config = json.loads(config_data)

def matomo_log_visit(event, context):
    # Decode the JSON event data
    event_string = base64.b64decode(event['data']).decode('utf-8')
    event_data = json.loads(event_string)

    # Check for excluded user agents
    if any(re.match(user_agent,event_data['protoPayload'].get('userAgent','')) for user_agent in config['EXCLUDED_USER_AGENTS']):
        print('excluded user agent: {}'.format(event_data['protoPayload'].get('userAgent','')))
        return

    # Check for excluded paths
    if any(re.match(path,event_data['protoPayload']['resource']) for path in config['EXCLUDED_PATHS']):
        print('excluded path: {}'.format(event_data['protoPayload']['resource']))
        return

    # Check for static extensions
    if any(re.match(r'.*\.{}(\?.*)?$'.format(extension),event_data['protoPayload']['resource']) for extension in config['STATIC_EXTENSIONS']):
        print('excluded extension: {}'.format(event_data['protoPayload']['resource']))
        return

    # Build the Matomo request
    url = config['MATOMO_URL']
    params = {
        'token_auth':config['AUTH_TOKEN'],
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

    # Check for download extensions
    if any(re.match(r'\.{}$'.format(extension),event_data['protoPayload']['resource']) for extension in config['DOWNLOAD_EXTENSIONS']):
        params['download'] = params['url']

    # Send the Matomo API request
    response = requests.post(url, params=params)
    if response.status_code == 204:
        print('logged: {}'.format(event_data['protoPayload']['resource']))
    else:
        print('error: response code {}'.format(response.status_code))
