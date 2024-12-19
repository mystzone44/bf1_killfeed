from PIL import Image
from modules import ScreenshotManager, Model
import numpy as np

if __name__ == '__main__':
    screenshot_manager = ScreenshotManager()

    model = Model()

    image = Image.open('testimg.png')
    np_image = np.asarray(image)

    kick_players = model.predict(np_image)

    for player, weapon in kick_players.items():
        print('Player ' + player + ' using weapon ' + weapon)
