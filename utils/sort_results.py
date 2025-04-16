import json
import os

def format_power(ghs: float) -> str:
    if ghs >= 1_000_000:
        return f"{ghs / 1_000_000:.2f} Ph/s"
    elif ghs >= 1_000:
        return f"{ghs / 1_000:.2f} Th/s"
    else:
        return f"{ghs:.2f} Gh/s"

def main():
    # Resolve results.json relative to the script's parent directory
    base_dir = os.path.dirname(os.path.abspath(__file__))
    results_path = os.path.join(base_dir, "..", "data", "results.json")

    try:
        with open(results_path, "r", encoding="utf-8") as f:
            analyzed = json.load(f)
    except FileNotFoundError:
        print("❌ results.json not found.")
        return

    if not analyzed:
        print("⚠️ No miners found in results.")
        return

    analyzed.sort(key=lambda m: m["efficiency_score"], reverse=True)

    print("\n📊 Top miners (sorted by effective power per 1 RLT):")
    print("--------------------------------------------------------")
    for i, m in enumerate(analyzed[:5], start=1):
        readable_power = format_power(m["effective_power_ghs"])
        readable_score = format_power(m["efficiency_score"])
        print(f"{i}. {m['name']} → Score: {readable_score} per RLT | Price: {m['price_rlt']} RLT")

if __name__ == "__main__":
    main()
