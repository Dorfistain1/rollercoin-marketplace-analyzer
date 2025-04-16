import time
import random
import cv2
import numpy as np
from PIL import ImageGrab
from config import rel_path
from utils.mouse import human_scroll

# Path to the footer reference image (e.g. 'ABOUT US | INFORMATION | COMMUNITY')
SCROLL_STOP_TEMPLATE = rel_path("ocr", "templates", "footer_about_us.png")

def is_footer_visible(template_path: str, threshold: float = 0.9) -> bool:
    """
    Checks if the footer element is visible on the current screen using template matching.
    """
    screen = np.array(ImageGrab.grab())
    screen_gray = cv2.cvtColor(screen, cv2.COLOR_RGB2GRAY)
    template = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)

    result = cv2.matchTemplate(screen_gray, template, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, _ = cv2.minMaxLoc(result)

    return max_val >= threshold

def scroll_until_footer(get_current_names, max_scrolls: int = 30, scroll_px_range=(250, 350)):
    """
    Scrolls the page while analyzing miner names until the footer is visible.

    :param get_current_names: Callable returning list of currently visible miner names.
    :param max_scrolls: Max number of scrolls to attempt.
    :param scroll_px_range: Tuple (min, max) defining scroll step in pixels.
    """
    seen = set(get_current_names())
    print(f"👀 Initially found {len(seen)} miners.")

    for i in range(max_scrolls):
        print(f"\n--- Scroll attempt #{i + 1} ---")
        time.sleep(random.uniform(0.3, 0.6))

        scroll_amount = -random.randint(*scroll_px_range)
        human_scroll(scroll_amount)
        print(f"🌀 Scrolled by {scroll_amount}px")

        time.sleep(random.uniform(0.4, 0.7))  # Wait for page to settle

        current = set(get_current_names())
        new = current - seen
        if new:
            print(f"✅ {len(new)} new miners added.")
        else:
            print("⚠️ No new miners found.")

        seen.update(new)

        if is_footer_visible(SCROLL_STOP_TEMPLATE):
            print("🛑 Footer detected, stopping scroll.")
            break
    else:
        print("⚠️ Reached max scrolls without finding footer.")
