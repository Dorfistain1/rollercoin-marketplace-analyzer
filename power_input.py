# power_input.py

def ask_user_power():
    while True:
        try:
            value = float(input("Enter your total raw power (as a number, in Gh/s): "))
        except ValueError:
            print("Please enter a valid number.")
            continue

        # Pro kontrolu: zobraz číselnou hodnotu v "lidské" jednotce
        if value >= 1_000_000:
            label = "Ph/s"
            shown_value = value / 1_000_000
        elif value >= 1_000:
            label = "Th/s"
            shown_value = value / 1_000
        else:
            label = "Gh/s"
            shown_value = value

        confirm = input(f"Did you mean {shown_value} {label}? (Press Enter to confirm or type anything to re-enter): ")
        if confirm == "":
            return value  # always in Gh/s

def ask_user_pages():
    while True:
        try:
            value = int(input("Enter the maximum number of pages to scroll through: "))
            if value < 1:
                print("Please enter a valid number greater than 0.")
                continue
        except ValueError:
            print("Please enter a valid integer.")
            continue

        return value


def ask_user_max_price():
    while True:
        try:
            value = float(input("Enter the maximum price for a miner in RLT: "))
            if value < 0:
                print("Please enter a valid price greater than or equal to 0.")
                continue
        except ValueError:
            print("Please enter a valid number.")
            continue

        return value
