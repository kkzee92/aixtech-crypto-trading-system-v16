"""Synthetic data generator and secure ingestion helpers (v16 enhanced)."""
import random
from typing import Dict, Any

def generate_synthetic(asset_class: str = "majors") -> Dict[str, Any]:
    price = 65000 if asset_class == "majors" else (2500 if asset_class == "large_alts" else 100)
    base = {
        "price": price,
        "ema_50": price * random.uniform(0.96, 1.04),
        "ema_200": price * random.uniform(0.88, 1.12),
        "rsi": random.uniform(20, 80),
        "volume_ratio": random.uniform(0.6, 3.0),
        "funding_rate": random.uniform(-0.02, 0.03),
        "atr_pct": random.uniform(1.5, 12),
        "bb_upper": price * random.uniform(1.015, 1.06),
        "bb_lower": price * random.uniform(0.94, 0.985),
        "adx": random.uniform(15, 45),
        "regime": random.choice(["strong_trend", "trend", "range", "neutral", "stress", "high_vol"]),
        "mtf_consistency": random.uniform(0.4, 0.95),  # multi-TF agreement proxy
    }
    if asset_class == "large_alts":
        base.update({
            "btc_relative_strength": random.uniform(0.80, 1.25),
            "macd_histogram": random.uniform(-3, 3),
            "adx": random.uniform(20, 50),
        })
    elif asset_class == "defi":
        base.update({
            "tvl_change_7d": random.uniform(-0.20, 0.25),
            "fee_revenue_change": random.uniform(-0.20, 0.30),
            "active_addresses_change": random.uniform(-0.15, 0.20),
            "tvl_usd": random.uniform(1e8, 5e9),
        })
    elif asset_class == "stablecoins":
        base.update({
            "premium_to_peg": random.uniform(-0.02, 0.02),
            "yield_diff_bps": random.uniform(0, 200),
            "peg_deviation_hours": random.uniform(0, 48),
        })
    elif asset_class == "high_volatility":
        base.update({
            "atr_pct": random.uniform(6, 20),
            "volume_ratio": random.uniform(2.0, 8.0),
            "rsi": random.uniform(15, 85),
        })
    return base

def validate_data(data: Dict[str, Any]) -> bool:
    """Basic input validation."""
    required = ["price"]
    return all(k in data and isinstance(data[k], (int, float)) and data[k] > 0 for k in required)
