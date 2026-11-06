from crypto_trading.strategies import get_strategy
from crypto_trading.data import generate_synthetic

def test_majors_signal():
    data = generate_synthetic("majors")
    data["regime"] = "trend"
    data["adx"] = 30
    data["mtf_consistency"] = 0.8
    sig = get_strategy("majors").generate_signal(data)
    assert sig["signal"] in ("BUY", "SELL", "HOLD")
    assert 0 <= sig["confidence"] <= 1
    assert "size_pct" in sig

def test_all_classes():
    for ac in ["majors", "large_alts", "defi", "stablecoins", "high_volatility"]:
        data = generate_synthetic(ac)
        sig = get_strategy(ac).generate_signal(data)
        assert sig["asset_class"] == ac
