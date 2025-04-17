import json
import cv2
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from config import rel_path, PRESET_RAW_POWER_GHS
from miner_analyzer import analyze_miner
from screen_profiles import DebugProfile
from vision.page_scanner import find_miner_boxes
from ocr.extract import extract_miner_data
from ocr import regions

def format_power(ghs: float) -> str:
    if ghs >= 1_000_000:
        return f"{ghs / 1_000_000:.2f} Ph/s"
    elif ghs >= 1_000:
        return f"{ghs / 1_000:.2f} Th/s"
    else:
        return f"{ghs:.2f} Gh/s"

def save_debug_crop(img, region_key):
    x, y, w, h = regions.REGIONS[region_key]
    cropped = img[y:y+h, x:x+w]
    path = rel_path("debug", f"debug_01_{region_key}.png")
    cv2.imwrite(path, cropped)

def save_debug_full_box(img):
    path = rel_path("debug", "debug_01_full.png")
    cv2.imwrite(path, cv2.cvtColor(img, cv2.COLOR_RGB2BGR))

def main():
    print("=== DEBUG: RollerCoin Miner Analyzer ===")

    profile = DebugProfile()
    profile.activate()
    print(f"🧩 Debug profile activated: {profile.name}")

    raw_power_ghs = PRESET_RAW_POWER_GHS
    print(f"⚡ Using preset raw power: {format_power(raw_power_ghs)}")

    image_path = profile.get_debug_image_path()
    print(f"📷 Reading image: {image_path}")
    image = cv2.imread(image_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    miner_images = find_miner_boxes(image)
    print(f"\n🧠 Found {len(miner_images)} miner box(es)")

    analyzed = []

    for i, img in enumerate(miner_images):
        print(f"\n🔍 Extracting miner #{i + 1}...")

        # Only save debug crops for the first miner
        if i == 0:
            save_debug_full_box(img)
            for region_key in regions.REGIONS:
                save_debug_crop(img, region_key)


        data = extract_miner_data(img)
        print("   Raw OCR:", data)

        if all(value is not None for value in data.values()):
            print("   ✅ Data complete, analyzing miner.")
            analyzed.append(analyze_miner(data, raw_power_ghs))
        else:
            print("   ⚠️ Skipping incomplete miner.")

    if analyzed:
        analyzed.sort(key=lambda m: m["efficiency_score"], reverse=True)
        print("\nTop miners (sorted by effective power per 1 RLT):")
        print("--------------------------------------------------")
        for i, m in enumerate(analyzed[:5], start=1):
            readable_power = format_power(m["effective_power_ghs"])
            readable_score = format_power(m["efficiency_score"])
            print(f"{i}. {m['name']} → Score: {readable_score} per RLT | Price: {m['price_rlt']} RLT")

        output_path = rel_path("data", "results.json")
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(analyzed, f, indent=2)
            print(f"\n📁 Results saved to {output_path}")

if __name__ == "__main__":
    main()
