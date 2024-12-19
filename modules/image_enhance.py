import cv2 as cv
import numpy as np
import math

ally_color = (64,118,199)
enemy_color = (189,54,49)
squad_color = (74,155,44)

def get_color_interval_from_rgb(rgb: tuple[int, int, int], threshold = 80) -> tuple:
    r, g, b = rgb
    hsv = cv.cvtColor(np.uint8([[[r, g, b]]]), cv.COLOR_RGB2HSV)[0][0]
    min= np.array([np.clip(int(hsv[0]) - threshold, 0, 180), 110, 100], dtype=np.uint8)
    max = np.array([np.clip(int(hsv[0]) + threshold, 0, 180), 255, 255], dtype=np.uint8)
    return min, max

def create_masks_by_colors(image_hsv, *colors) -> tuple:
    masks = []
    for color in colors:
        lower, upper = get_color_interval_from_rgb(color)
        masks.append(cv.inRange(image_hsv, lower, upper))
    return tuple(masks)


def enhance_image(image_array, target_height = 100):

    height, width = image_array.shape[:2]
    ratio = target_height / height
    image_array = cv.resize(image_array, (math.trunc(ratio * width), math.trunc(ratio * height)), interpolation = cv.INTER_CUBIC)

    image_hsv = cv.cvtColor(image_array, cv.COLOR_BGR2HSV)

    masks = create_masks_by_colors(image_hsv, ally_color, enemy_color, squad_color)

    mask = cv.bitwise_not(cv.bitwise_or(*masks))
    white_background = np.full_like(image_hsv, 255)
    result = cv.bitwise_and(white_background, white_background, mask = mask)

    return result, mask