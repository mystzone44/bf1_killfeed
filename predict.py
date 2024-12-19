import cv2
from ultralytics import YOLO
import pytesseract

pytesseract.pytesseract.tesseract_cmd = 'tesseract/tesseract.exe'
common_symbols = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'

available_nickname_symbols = f'{common_symbols}-_[]'

def recognize_text(image) -> str:
    text: str = pytesseract.image_to_string(image, lang = 'bf1', config = f'--psm 7 --oem 3 -c tessedit_char_whitelist={available_nickname_symbols}')
    words = text.strip() # string cleanup
    return words or None

weapon_classes = {
    0: 'heavy bomber',
    1: 'smg08',
    2: 'artillery truck',
    3: 'rifle grenade',
    4: 'mortar'
}

model = YOLO("best.pt")

img_name = "testimg.png"

image = cv2.imread(img_name)

results = model(img_name)


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

        start_point = (left_x - 150, top_y)
        end_point = (left_x, bottom_y)
        # colour = (0, 255, 0)
        # thickness = 2

        name_image = image[top_y:bottom_y, left_x - 150:left_x]

        print(recognize_text(name_image) + ' using ' + weapon_classes[box.cls[0]])

        #image = cv2.rectangle(image, start_point, end_point, colour, thickness)
        # cv2.imshow('Result', name_image)

cv2.waitKey(0)