from . import api_globals
import uuid

# get_auth_code
auth_host = 'https://accounts.ea.com/connect/auth?client_id=sparta-backend-as-user-pc&response_type=code&release_type=none'

# get_access_token
access_host = 'https://accounts.ea.com/connect/auth?response_type=token&locale=en-US&client_id=ORIGIN_JS_SDK&redirect_uri=nucleus%3Arest'

# get_full_server_details_by_game_id, get_persona_by_id, get_servers_by_persona_id, get_session_id_by_authcode, kick_player, search_server_by_name
rpc_host = 'https://sparta-gw.battlelog.com/jsonrpc/pc/api'

# get_player_persona_by_name
identity_host = 'https://gateway.ea.com/proxy/identity/personas?namespaceName=cem_ea_id&displayName='

# get_players_by_game_id
gametools = 'https://api.gametools.network/bf1/players/'

def print_error_message(msg: str, content = None) -> None:
    print(msg)
    if content:
        print('API called returned: ' + str(content))

def rest_headers() -> dict[str, str]:
    return {'Cookie': f'remid={api_globals.remid};sid={api_globals.sid};'}

def rpc_headers() -> dict[str, str]:
    return {'X-GatewaySession': api_globals.session_id}

def rpc_request(method: str, params: object) -> dict[str, str | object]:
    return {
        'id': str(uuid.uuid4()),
        'jsonrpc': '2.0',
        'method': method,
        'params': params
    }