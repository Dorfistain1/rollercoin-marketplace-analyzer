import pyautogui
import time
import cv2
import numpy as np
from utils.mouse import human_move_offscreen

def take_screenshot():
    """Returns a screenshot as a NumPy RGB array"""
    return np.array(pyautogui.screenshot().convert("RGB"))

def is_hamster_visible(reference_image_paths, threshold=0.9):
    """
    Tries all reference images and returns True if any match exceeds the threshold.
    Also prints debug match values.
    """
    screen = take_screenshot()
    screen_gray = cv2.cvtColor(screen, cv2.COLOR_RGB2GRAY)

    best_match_val = 0

    for path in reference_image_paths:
        template = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
        result = cv2.matchTemplate(screen_gray, template, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, _ = cv2.minMaxLoc(result)
        best_match_val = max(best_match_val, max_val)

    return best_match_val >= threshold

def find_marketplace_window(reference_image_path):
    max_attempts = 10
    attempt = 0

    while attempt < max_attempts:
        pyautogui.keyDown("alt")
        for _ in range(attempt + 1):
            pyautogui.press("tab")
            time.sleep(0.1)
        pyautogui.keyUp("alt")
        time.sleep(1.2)

        if is_hamster_visible(reference_image_path):
            print("✅ Marketplace window found!")
            break

        attempt += 1
    else:
        print("❌ Failed to find marketplace window.")

    # Move cursor offscreen (just in case)
    human_move_offscreen()

