def analyze_miner(miner: dict, raw_power_ghs: float) -> dict:
    """
    Calculates the effective power and efficiency score of a miner.

    :param miner: Dictionary with keys: name, power_ghs, bonus_percent, price_rlt
    :param raw_power_ghs: User's current raw power in Gh/s
    :return: Augmented dictionary with effective_power_ghs and efficiency_score
    """
    base_power = miner["power_ghs"]           # Gh/s
    bonus_percent = miner.get("bonus_percent", 0.0)
    price = miner["price_rlt"]

    # New total power if the miner is bought
    new_total_power = raw_power_ghs + base_power  # Gh/s

    # Bonus is calculated from the new total power
    effective_bonus = new_total_power * bonus_percent  # Gh/s

    # Effective power includes the miner's own power + bonus
    effective_power = base_power + effective_bonus  # Gh/s

    # Efficiency is power per RLT (still in Gh/s)
    efficiency = effective_power / price if price > 0 else 0

    return {
        **miner,
        "effective_power_ghs": effective_power,
        "efficiency_score": efficiency
    }
