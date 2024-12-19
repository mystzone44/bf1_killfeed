import pytesseract
import globals
from difflib import SequenceMatcher
import api
import config

pytesseract.pytesseract.tesseract_cmd = 'tesseract/tesseract.exe'
common_symbols = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'

available_nickname_symbols = f'{common_symbols}-_[]'

def get_string_similarity(str1: str, str2: str) -> float:
    return SequenceMatcher(None, str1, str2).ratio()

def search_for_player(attempted_player_name):

    if attempted_player_name in globals.teams.keys():
        return attempted_player_name

    highest_probability = 0
    most_likely_name = ''
    for actual_name in globals.teams.keys():
        probability = get_string_similarity(attempted_player_name, actual_name)
        if probability > highest_probability:
            highest_probability = probability
            most_likely_name = actual_name

    if highest_probability > config.data.player_name_similarity_probability:
        return most_likely_name
    
    return None

def recognize_player(image) -> str:
    text: str = pytesseract.image_to_string(image, lang = 'bf1', config = f'--psm 7 --oem 3 -c tessedit_char_whitelist={available_nickname_symbols}')
    read_player_name = text.strip() # string cleanup

    if read_player_name is None:
        return None
    
    return read_player_name

    with globals.teams_lock:
        
        # Initial search
        player = search_for_player(read_player_name)
        if player:
            return player

        # Get player list again and search
        success, globals.teams = api.get_players_by_game_id(globals.game_id)
        if not success:
            print('Failed to get teams')
            return False
        
        # Search again
        player = search_for_player(read_player_name)
        if player:
            return player

    return None