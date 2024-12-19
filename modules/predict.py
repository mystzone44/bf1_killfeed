from ultralytics import YOLO
import numpy as np
from .player_name import recognize_player
from .image_enhance import enhance_image
import cv2

weapon_classes = {
    0: 'heavy bomber',
    1: 'smg08',
    2: 'artillery truck',
    3: 'rifle grenade',
    4: 'mortar'
}

class Model:
    def __init__(self):
        self.model = YOLO("best.pt")

    def predict(self, image: np.ndarray):
        results = self.model(image)

        kick_players = dict()

        for result in results:
            np_result = result.numpy()

            for box in np_result.boxes:

                if box.conf < 0.7:
                    print('Confidence is ' + str(box.conf) + ', skipping')
                    continue
                
                x, y, width, height = box.xywh[0]

                left_x = int(x - width * 0.5)
                top_y = int(y - height * 0.5)

                bottom_y = int(y + height * 0.5)

                name_image = image[top_y:bottom_y, left_x - 150:left_x]

                name_image_enhanced, _ = enhance_image(name_image)

                player_name = recognize_player(name_image_enhanced) 
                weapon = weapon_classes[box.cls[0]]
                kick_players[player_name] = weapon

                # colour = (0, 255, 0)
                # thickness = 2
                # name_image_enhanced = cv2.rectangle(name_image_enhanced, start_point, end_point, colour, thickness)
                # cv2.imshow('Result', name_image_enhanced)
                # cv2.waitKey()

        return kick_players