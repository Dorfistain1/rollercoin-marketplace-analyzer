import time
import random
import pyautogui
import cv2
import numpy as np
from PIL import Image
from utils.mouse import human_click, human_move_offscreen
from vision.screen_grabber import take_screenshot
from config import rel_path

# Define template paths for page numbers (2–6)
TEMPLATES = {
    "2": rel_path("ocr", "templates", "page_2.png"),
    "3": rel_path("ocr", "templates", "page_3.png"),
    "4": rel_path("ocr", "templates", "page_4.png"),
    "5": rel_path("ocr", "templates", "page_5.png"),
    "6": rel_path("ocr", "templates", "page_6.png")
}

# Global variable to store fixed coordinates from page 6 onward
fixed_page_coords = None

def find_page_number(template_path: str, threshold: float = 0.9):
    screen = take_screenshot()
    if isinstance(screen, np.ndarray):
        screen = Image.fromarray(screen)

    screen_rgb = screen.convert("RGB")
    screen_gray = cv2.cvtColor(np.array(screen_rgb), cv2.COLOR_RGB2GRAY)
    template = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)

    result = cv2.matchTemplate(screen_gray, template, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(result)

    if max_val >= threshold:
        return max_loc
    return None

def click_page_number(page_number: str, offset_x=0, offset_y=0):
    global fixed_page_coords

    if page_number in TEMPLATES:
        # Pages 2–6 use template matching
        page_coords = find_page_number(TEMPLATES[page_number])
        if not page_coords:
            return
        x, y = page_coords

        # If it's page 6, save coordinates for later use
        if page_number == "6" and fixed_page_coords is None:
            fixed_page_coords = (x, y)

        # Slightly larger random offset for click targeting
        x += 20 + random.randint(-7, 7)
        y += 20 + random.randint(-7, 7)

    elif page_number.isdigit() and int(page_number) > 6:
        # Use saved coordinates for 7+ (fixed layout)
        if fixed_page_coords is None:
            print("⚠️ Cannot click pages >6 before detecting page 6!")
            return
        x, y = fixed_page_coords
        x += 20 + random.randint(-7, 7)
        y += 20 + random.randint(-7, 7)

    else:
        print(f"⚠️ No template or coords found for page {page_number}")
        return

    human_click(x + offset_x, y + offset_y)
    time.sleep(random.uniform(0.5, 1.5))
    human_move_offscreen()

def navigate_to_next_page(page_number: str):
    click_page_number(page_number)
