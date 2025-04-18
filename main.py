import json
import cv2
import pyautogui

from miner_analyzer import analyze_miner
from config import rel_path, PRESET_RAW_POWER_GHS, MAX_PAGES, MAX_PRICE_RLT
from vision.screen_grabber import find_marketplace_window, take_screenshot
from vision.page_scanner import find_miner_boxes
from ocr.extract import extract_miner_data
from vision.scroller import scroll_until_footer
from vision.navigator import navigate_to_next_page
from screen_profiles import Profile1080p, Profile4K

def detect_and_activate_profile():
    width, height = pyautogui.size()
    if width >= 3840:
        profile = Profile4K()
    else:
        profile = Profile1080p()
    profile.activate()
    return profile

def format_power(ghs: float) -> str:
    if ghs >= 1_000_000:
        return f"{ghs / 1_000_000:.2f} Ph/s"
    elif ghs >= 1_000:
        return f"{ghs / 1_000:.2f} Th/s"
    else:
        return f"{ghs:.2f} Gh/s"

def ocr_miner_names():
    image = take_screenshot()
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    boxes = find_miner_boxes(image)
    names = []
    for box in boxes:
        data = extract_miner_data(box)
        if data.get("name"):
            names.append(data["name"])
    return names

def analyze_visible_miners(raw_power_ghs: float, seen_names: set, max_price: float = None):
    image = take_screenshot()
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    miner_images = find_miner_boxes(image)
    analyzed = []

    print(f"\n🧠 Found {len(miner_images)} miner box(es)")

    for i, img in enumerate(miner_images):
        print(f"\n🔍 Extracting miner #{i + 1}...")
        data = extract_miner_data(img)
        print("   Raw OCR:", data)

        name = data.get("name")
        if name in seen_names:
            print(f"   ⚠️ Skipping duplicate miner '{name}'.")
            continue

        if name:
            seen_names.add(name)

        if all(value is not None for value in data.values()):
            print("   ✅ Data complete, analyzing miner.")
            if max_price is None or data['price_rlt'] <= max_price:
                analyzed.append(analyze_miner(data, raw_power_ghs))
            else:
                print(f"   ⚠️ Skipping miner with price higher than {max_price} RLT.")
        else:
            print("   ⚠️ Skipping incomplete miner.")

    return analyzed


def main():
    print("=== RollerCoin Miner Efficiency Analyzer ===")

    # 🧠 Detect and activate screen profile (resolves REGIONS, templates etc.)
    profile = detect_and_activate_profile()
    print(f"🧩 Active profile: {profile.name}")

    # 🪟 Auto-switch to RollerCoin Marketplace window
    print("🪟 Switching to RollerCoin window...")
    find_marketplace_window([profile.hamster_template_path])

    raw_power_ghs = PRESET_RAW_POWER_GHS
    print(f"⚡ Using preset raw power: {format_power(raw_power_ghs)}")

    max_pages = MAX_PAGES
    max_price_rlt = MAX_PRICE_RLT

    analyzed = []
    current_page = 1

    if max_pages is None and max_price_rlt is not None:
        print("📜 Scanning until price exceeds MAX_PRICE_RLT or no more pages...")
        while True:
            print(f"🔄 Scanning page {current_page}...")
            scroll_until_footer(ocr_miner_names, scroll_px_range=(300, 380))

            seen_names = set()
            all_miners = analyze_visible_miners(raw_power_ghs, seen_names, max_price=None)

            for miner in all_miners:
                if miner['price_rlt'] <= max_price_rlt:
                    analyzed.append(miner)

            if any(miner['price_rlt'] > max_price_rlt for miner in all_miners):
                break

            current_page += 1
            navigate_to_next_page(str(current_page))

    elif max_pages is not None and max_price_rlt is None:
        print(f"📜 Scanning {max_pages} pages...")
        while current_page <= max_pages:
            print(f"🔄 Scanning page {current_page}...")
            scroll_until_footer(ocr_miner_names, scroll_px_range=(300, 380))

            seen_names = set()
            miners_on_page = analyze_visible_miners(raw_power_ghs, seen_names)
            analyzed.extend(miners_on_page)

            current_page += 1
            navigate_to_next_page(str(current_page))

    elif max_pages is not None and max_price_rlt is not None:
        print(f"📜 Scanning {max_pages} pages with price filter {max_price_rlt} RLT...")
        while current_page <= max_pages:
            print(f"🔄 Scanning page {current_page}...")
            scroll_until_footer(ocr_miner_names, scroll_px_range=(300, 380))

            seen_names = set()
            miners_on_page = analyze_visible_miners(raw_power_ghs, seen_names, max_price_rlt)
            analyzed.extend(miners_on_page)

            current_page += 1
            navigate_to_next_page(str(current_page))

    else:
        print("⚠️ Configuration error: You must set either MAX_PAGES or MAX_PRICE_RLT or both.")
        return

    if analyzed:
        analyzed.sort(key=lambda m: m["efficiency_score"], reverse=True)
        print("\nTop miners (sorted by effective power per 1 RLT):")
        print("--------------------------------------------------")
        for i, m in enumerate(analyzed[:5], start=1):
            readable_power = format_power(m["effective_power_ghs"])
            readable_score = format_power(m["efficiency_score"])
            print(f"{i}. {m['name']} → Score: {readable_score} per RLT | Price: {m['price_rlt']} RLT")

        with open(rel_path("data", "results.json"), "w", encoding="utf-8") as f:
            json.dump(analyzed, f, indent=2)
            print("\n📁 Results saved to data/results.json")

if __name__ == "__main__":
    main()
