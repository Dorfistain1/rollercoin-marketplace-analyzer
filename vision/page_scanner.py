import cv2
import numpy as np
from config import rel_path

TEMPLATE_PATH = rel_path("ocr", "templates", "rom_rlt.png")
TEMPLATE_THRESHOLD = 0.85

# Offsets from RLT location
TOP_OFFSET = 68
BOTTOM_OFFSET = 122
LEFT_OFFSET = 595
RIGHT_OFFSET = 75

def find_miner_boxes(full_image: np.ndarray, template_path: str = TEMPLATE_PATH) -> list:
    """
    Finds miner boxes based on a fixed pixel offset from the "RLT" label
    """
    gray_full = cv2.cvtColor(full_image, cv2.COLOR_RGB2GRAY)
    template = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)

    result = cv2.matchTemplate(gray_full, template, cv2.TM_CCOEFF_NORMED)
    y_coords = []
    boxes = []

    for pt in zip(*np.where(result >= TEMPLATE_THRESHOLD)):
        y, x = pt
        # Avoid duplicate matches (same row)
        if any(abs(y - prev_y) < 10 for prev_y in y_coords):
            continue
        y_coords.append(y)

        # Use fixed offset from RLT location
        top = y - TOP_OFFSET
        bottom = y + BOTTOM_OFFSET
        left = x - LEFT_OFFSET
        right = x + RIGHT_OFFSET

        if top < 0 or left < 0:
            continue

        box = full_image[top:bottom, left:right]
        if box.shape[0] == (bottom - top) and box.shape[1] == (right - left):
            boxes.append(box)

    return boxes
