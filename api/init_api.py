from dotenv import load_dotenv
from . import api_globals
from .api_functions import print_error_message, get_access_token, get_auth_code, get_session_id_by_authcode, get_persona_by_id
import requests
import json
import os

load_dotenv()

def init() -> tuple[bool, str]:
    api_globals.sid = os.getenv('SID')
    api_globals.remid = os.getenv('REMID')

    success, api_globals.access_token = get_access_token()
    if not success:
        print_error_message('Failed to get access token')
        return False, None

    resp_auth = get_auth_code()
    if not resp_auth.success:
        print_error_message('Failed to get auth code')
        return False, None

    api_globals.remid = resp_auth.remid
    api_globals.sid = resp_auth.sid

    success, session_id_or_error, persona_id = get_session_id_by_authcode(resp_auth.code)
    if not success:
        print_error_message('Failed to get session id', session_id_or_error)
        return False, None

    api_globals.session_id = session_id_or_error
    api_globals.my_persona_id = persona_id

    success, name_or_error = get_persona_by_id(api_globals.my_persona_id)
    if not success:
        print_error_message('Failed to get persona for id', name_or_error)
        return False, None

    return True, name_or_error