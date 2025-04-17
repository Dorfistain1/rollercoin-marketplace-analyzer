import cv2
import numpy as np
from config import rel_path
from screen_profiles import detect_and_activate_profile

# Activate and load the current profile
profile = detect_and_activate_profile()
TOP_OFFSET, BOTTOM_OFFSET, LEFT_OFFSET, RIGHT_OFFSET = profile.rlt_offsets
TEMPLATE_PATH = profile.rom_rlt_template_path

BOX_WIDTH = LEFT_OFFSET + RIGHT_OFFSET
BOX_HEIGHT = TOP_OFFSET + BOTTOM_OFFSET
TEMPLATE_THRESHOLD = 0.85

def find_miner_boxes(full_image: np.ndarray, template_path: str = TEMPLATE_PATH) -> list:
    """
    Finds all miner boxes by locating the "rom RLT" reference template.
    Returns a list of cropped miner boxes from the full image.
    """
    gray_full = cv2.cvtColor(full_image, cv2.COLOR_RGB2GRAY)
    template = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)

    if template.shape[0] > gray_full.shape[0] or template.shape[1] > gray_full.shape[1]:
        raise ValueError(
            f"Template size {template.shape} is larger than input image size {gray_full.shape}. "
            "Check your screen resolution or selected profile."
        )

    result = cv2.matchTemplate(gray_full, template, cv2.TM_CCOEFF_NORMED)
    boxes = []

    for pt in zip(*np.where(result >= TEMPLATE_THRESHOLD)):
        y, x = pt

        # Calculate box boundaries from template position and profile offsets
        top = y - TOP_OFFSET
        left = x - LEFT_OFFSET
        if top < 0 or left < 0:
            continue

        box = full_image[top:top + BOX_HEIGHT, left:left + BOX_WIDTH]
        if box.shape[0] == BOX_HEIGHT and box.shape[1] == BOX_WIDTH:
            boxes.append(box)


    return boxes
