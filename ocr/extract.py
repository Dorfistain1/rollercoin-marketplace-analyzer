# ocr/extract.py
import pytesseract
import cv2
import re
import numpy as np
from ocr.regions import crop_region

# Converts power string like "3.825 Th/s" to Gh/s float
def parse_power(power_str):
    match = re.search(r"([\d.,]+)\s*(Gh|Th|Ph)/s", power_str, re.IGNORECASE)
    if not match:
        return None

    value_str, unit = match.groups()

    value_str = value_str.replace(",", ".")

    try:
        value = float(value_str)
    except ValueError:
        return None

    unit = unit.lower()
    if unit == "gh":
        return value
    elif unit == "th":
        return value * 1_000
    elif unit == "ph":
        return value * 1_000_000
    return None


# Converts bonus string like "0%" to float percent
def parse_bonus(text: str) -> float:
    match = re.search(r"(\d+(?:\.\d+)?)\s*%", text)
    if match:
        return float(match.group(1)) / 100
    return 0.0

# Converts price string like "0.1234 RLT" to float
def parse_price(price_str):
    match = re.search(r"(\d+(\.\d+)?)(\s*RLT)?", price_str, re.IGNORECASE)
    return float(match.group(1)) if match else None

def extract_miner_data(miner_image):
    # Ensure image has valid dimensions
    if miner_image is None or not isinstance(miner_image, np.ndarray):
        raise ValueError("Invalid miner image input")

    name_img = crop_region(miner_image, "name")
    power_bonus_img = crop_region(miner_image, "power_bonus")
    price_img = crop_region(miner_image, "price")

    # Protect against empty crops
    if name_img.size == 0 or power_bonus_img.size == 0 or price_img.size == 0:
        raise ValueError("Cropped region is outside image bounds")

    name = pytesseract.image_to_string(name_img, config="--psm 7").strip()
    power_bonus_text = pytesseract.image_to_string(power_bonus_img, config="--psm 7").strip()
    price_text = pytesseract.image_to_string(price_img, config="--psm 7 -c tessedit_char_whitelist=0123456789.RLT").strip()

    # Expecting something like "3.825 Th/s | 0%"
    power_str, bonus_str = (part.strip() for part in power_bonus_text.split("|")[:2]) if "|" in power_bonus_text else (power_bonus_text.strip(), "0%")

    return {
        "name": name,
        "power_ghs": parse_power(power_str),
        "bonus_percent": parse_bonus(bonus_str),
        "price_rlt": parse_price(price_text)
    }
