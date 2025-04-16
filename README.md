# Rollercoin Marketplace Analyzer

This tool automatically scans the RollerCoin Marketplace and helps you identify the most cost-efficient miners based on your current raw power. It uses OCR and human-like mouse movement to simulate browsing through marketplace pages and analyzing each miner box.

## Features

- Automatically switches to the RollerCoin window (based on hamster icon).
- Scrolls through the visible marketplace page.
- Detects all miner boxes and extracts:
  - Name
  - Hashrate (Gh/s, Th/s, or Ph/s)
  - Bonus power
  - Price (RLT)
- Calculates effective power including your current bonus multiplier.
- Calculates efficiency: *Effective Power per 1 RLT*.
- Sorts results by efficiency and outputs top suggestions.
- Supports multiple pages (navigation via numbered buttons).
- Allows limiting scan by:
  - `MAX_PAGES`: how many pages to analyze
  - `MAX_PRICE_RLT`: ignore miners more expensive than this

## Installation

Make sure you have Python 3.8+ installed.

Install the required packages:

```
pip install -r requirements.txt
```


Also make sure `tesseract` is installed and added to your system's PATH.

- Windows: https://github.com/tesseract-ocr/tesseract/wiki
- Linux: `sudo apt install tesseract-ocr`

## Configuration

Edit `config.py` to customize behavior:

- `PRESET_RAW_POWER_GHS`: your current raw power (in Gh/s)
- `MAX_PAGES`: max number of pages to scan (set to `None` to disable)
- `MAX_PRICE_RLT`: ignore miners above this price (set to `None` to disable)

You can use only one or both filters together.

## How it works

1. Switches to the RollerCoin Marketplace tab (Alt+Tab).
2. Detects the hamster icon to verify correct window.
3. Scrolls the current page to load all miners.
4. Extracts each visible miner and analyzes their efficiency.
5. Navigates through pages using number buttons (2–6+).
6. Stops based on config limits or when expensive miners appear.
7. Outputs top suggestions and saves them to `data/results.json`.

## Folder structure

- `ocr/` – OCR logic and templates
- `utils/` – Human-like mouse control
- `vision/` – Screen scanning, scrolling, and navigation

## Output

- Console output of best miners
- Results saved to: `data/results.json`

## Usage

1. **Open the RollerCoin Marketplace** in your browser and make sure it's visible on screen.
2. **Configure settings** in `config.py`, such as:
   - `PRESET_RAW_POWER_GHS`: Your current raw power (in Gh/s).
   - `MAX_PAGES`: How many pages to scan.
   - `MAX_PRICE_RLT`: Optional price filter – skip miners above this value.
3. **Run the script** using:

   ```
   python main.py
   ```

4. The bot will:
   - Automatically locate the RollerCoin window.
   - Scroll through the Marketplace and analyze miner stats using OCR.
   - Output the top miners directly in the console.
   - Save all scanned miner data to `data/results.json`.

5. **Optional**: You can re-analyze or sort results without re-running the bot by executing:

   ```
   python utils/sort_results.py
   ```

   This will read from `data/results.json` and print the top-performing miners again.


## Notes

This is a hobby automation tool and not affiliated with RollerCoin. Use responsibly.

---

**Created by Dorfistain**
