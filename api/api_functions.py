import json
import requests
from .endpoints import print_error_message, rest_headers, rpc_headers, rpc_request, access_host, rpc_host
from . import endpoints


def get_session_id_by_authcode(auth_code: str) -> tuple[bool, str | object, str | None]:
    json_body = rpc_request('Authentication.getEnvIdViaAuthCode', {
        'authCode': auth_code,
        'locale:': 'en-GB'
    })
    try:
        response = requests.post(rpc_host, json=json_body)
        if response.status_code == 200:
            json_content = json.loads(response.content)
            return True, json_content['result']['sessionId'], json_content['result']['personaId']
    except Exception as e:
        print_error_message('Error in getting session id from auth code', e)

    return False, json.loads(response.content), None

def get_access_token() -> tuple[bool, str | None]:
    try:
        response = requests.get(access_host, headers=rest_headers())
        content = json.loads(response.content)
        if response.status_code == 200:
            return True, content["access_token"]
    except Exception as e:
        print_error_message('Error in access token request', e)

    return False, None

class ResponseAuth:
    def __init__(self) -> None:
        self.success = False
        self.remid = ''
        self.sid = ''
        self.code = ''
        self.content = ''

def get_auth_code() -> ResponseAuth:
    resp_auth = ResponseAuth()
    try:
        response = requests.get(endpoints.auth_host, headers=rest_headers(), allow_redirects=False)
        if response.status_code == 302:
            location = str(response.headers['location'])
            if '127.0.0.1/success?code=' in location:
                if len(response.cookies) == 2:
                    resp_auth.remid = response.cookies.values()[0]
                    resp_auth.sid = response.cookies.values()[1]
                else:
                    resp_auth.sid = response.cookies.values()[0]

                resp_auth.success = True
                resp_auth.code = location.replace('http://127.0.0.1/success?code=', '')

            resp_auth.content = location
        else:
            resp_auth.content = response.content
    except Exception as e:
        print_error_message('Error in get auth code request', e)

    return resp_auth

def get_session_id_by_authcode(auth_code: str) -> tuple[bool, str | object, str | None]:
    json_body = rpc_request('Authentication.getEnvIdViaAuthCode', {
        'authCode': auth_code,
        'locale:': 'en-GB'
    })
    try:
        response = requests.post(endpoints.rpc_host, json=json_body)
        if response.status_code == 200:
            json_content = json.loads(response.content)
            return True, json_content['result']['sessionId'], json_content['result']['personaId']
    except Exception as e:
        print_error_message('Error in getting session id from auth code', e)

    return False, json.loads(response.content), None

def get_persona_by_id(persona_id: str) -> tuple[bool, str | object]:
    content = ''
    json_body = rpc_request('RSP.getPersonasByIds', {
        'game': 'tunguska',
        'personaIds': [persona_id]
    })
    try:
        response = requests.post(endpoints.rpc_host, headers=rpc_headers(), json=json_body)
        content = json.loads(response.content)
        if response.status_code == 200:
            return True, content['result'][persona_id]['displayName']
    except Exception as e:
        print_error_message('Error getting persona by id', e)

    return False, content