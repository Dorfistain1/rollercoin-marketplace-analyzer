import os

# Root folder of the project (where config.py is located)
ROOT_DIR = os.path.abspath(os.path.dirname(__file__))

def rel_path(*paths):
    return os.path.join(ROOT_DIR, *paths)

# Default values for max price in RLT (set to None to disable)
MAX_PRICE_RLT = None  # Example value, set to your desired limit

# Default values for max pages (set to None to disable)
MAX_PAGES = 3  # Set this to how many pages you want to scrape

# Default value for raw power in Gh/s
PRESET_RAW_POWER_GHS = 100_000_000  # Example, set to your desired value in Gh/s

