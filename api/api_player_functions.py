import json
import requests
from .endpoints import print_error_message, rpc_headers, rpc_request
from . import endpoints

def search_server_by_name(server_name: str) -> tuple[bool, object]:
    json_body = rpc_request('GameServer.searchServers', {
        'filterJson': "{\"version\":6,\"name\":\"" + server_name + "\"}",
        'game': 'tunguska',
        'limit': '30',
        'protocolVersion': '3779779'
    })
    try:
        response = requests.post(endpoints.rpc_host, headers=rpc_headers(), json=json_body)
        if response.status_code == 200:
            return True, json.loads(response.content)
    except Exception as e:
        print_error_message('Failed to search for server ' + server_name, e)

    return False, json.loads(response.content)

def get_server_id_and_fullname(server_name: str) -> tuple[bool, str | None, str | None]:
    success, server_info_or_error = search_server_by_name(server_name)
    if not success:
        return False, None, None

    servers = server_info_or_error['result']['gameservers']
    if len(servers) > 0:
        return True, servers[0]['gameId'], servers[0]['name']
    else:
        print('No server found called ' + server_name)
        return False, None, None
    
def get_players_by_game_id(game_id: str) -> tuple[bool, dict]:
    params = {'gameID': game_id}
    teams = dict()
    try:
        response = requests.get(endpoints.gametools, params=params)
        if response.status_code == 200:
            parsed_content = json.loads(response.content)
            team1 = parsed_content['teams'][0]['players']
            team2 = parsed_content['teams'][1]['players']
            team1.extend(team2)
            for player in team1:
                # We also need to append the platoon tag because it shows up in killfeed
                if player['platoon']:
                    teams['[' + player['platoon'] + ']' + player['name']] = player['player_id']
                else:
                    teams[player['name']] =  player['player_id']

            # # Also remove anyone from the kick list no longer in the game
            # globals.kick_list.intersection_update(teams)

            return True, teams
    except Exception as e:
        print_error_message('Failed to get playerlist for game id ' + game_id, e)

    return False, dict()

def kick_player(game_id: str, persona_id: str, reason: str) -> tuple[bool, object]:
    json_body = rpc_request('RSP.kickPlayer', {
        'game': 'tunguska',
        'gameId': game_id,
        'personaId': persona_id,
        'reason': reason
    })
    try:
        response = requests.post(endpoints.rpc_host, headers=rpc_headers(), json=json_body)
        if response.status_code == 200:
            return True, json.loads(response.content)
    except Exception as e:
        print_error_message('Error kicking player with id ' + str(persona_id), e)

    return False, json.loads(response.content)