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

# Global variable to store coordinates of page 6
page_6_coords = None

def find_page_number(template_path: str, threshold: float = 0.9):
    """Find a specific page number on the screen using OCR."""
    screen = take_screenshot()
    if isinstance(screen, np.ndarray):
        screen = Image.fromarray(screen)  # Convert NumPy array to Pillow Image

    screen_rgb = screen.convert("RGB")  # Now we can use .convert("RGB")
    screen_gray = cv2.cvtColor(np.array(screen_rgb), cv2.COLOR_RGB2GRAY)
    template = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)

    result = cv2.matchTemplate(screen_gray, template, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(result)

    if max_val >= threshold:
        return max_loc  # Coordinates of the top-left corner of the template
    return None



def click_page_number(page_number: str, offset_x=0, offset_y=0):
    """Click on the page number with optional offset and move the mouse away afterward."""
    global page_6_coords  # Declare page_6_coords as global

    page_coords = find_page_number(TEMPLATES[page_number])

    if page_coords:
        x, y = page_coords

        # Apply offset for page 6, which needs special handling
        if page_number == "6" and page_6_coords is None:
            page_6_coords = (x, y)

        # If this is page 6, use the saved coordinates with a small random offset
        if page_number == "6" and page_6_coords:
            x, y = page_6_coords
            x += random.randint(-7, 7)
            y += random.randint(-7, 7)
        else:
            # Apply small random offset for pages 2–5
            x += 20 + random.randint(-3, 3)
            y += 20 + random.randint(-3, 3)

        human_click(x + offset_x, y + offset_y)
        time.sleep(random.uniform(0.5, 1.5))

        # Move mouse out of the way after click (left or right edge)
        screen_width, screen_height = pyautogui.size()
        side = random.choice(["left", "right"])
        target_x = 20 if side == "left" else screen_width - 20
        target_y = screen_height // 2 + random.randint(-100, 100)
        human_move_offscreen()

    else:
        print(f"Page {page_number} not found!")


def navigate_to_next_page(page_number: str):
    """Navigate to the next page, clicking on the appropriate page number."""
    if page_number == "6":
        print(f"Page 6 detected, using saved coordinates for clicking.")
        if page_6_coords is None:
            print("⚠️ Page 6 coordinates not saved yet!")
        else:
            click_page_number("6")
    elif page_number in ["2", "3", "4", "5"]:
        click_page_number(page_number)
