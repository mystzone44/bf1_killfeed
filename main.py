from PIL import Image
from modules import ScreenshotManager, Model
import numpy as np
import api

if __name__ == '__main__':
    screenshot_manager = ScreenshotManager()

    model = Model()

    image = Image.open('testimg.png')
    np_image = np.asarray(image)

    print('Fetching API details...', end = ' ')

    success, persona_name = api.init()
    if not success:
        raise Exception('Failed to init api')
    
    print('Success')

    print('Connected to API with', persona_name)

    print('Fetching server information...', end = ' ')

    success, game_id, full_server_name = api.get_server_id_and_fullname('![VG]Vanguard')

    if not success:
        raise Exception('Failed to get server')

    success, teams = api.get_players_by_game_id(game_id)

    if not success:
        raise Exception('Failed to get server teams')

    print('Success')

    print(f'Found server {full_server_name}')

    kick_players = model.predict(np_image)

    for player, weapon in kick_players.items():
        print('Player ' + player + ' using weapon ' + weapon)
