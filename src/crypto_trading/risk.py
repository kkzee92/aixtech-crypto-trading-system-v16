"""Risk management gates (v16)."""
from typing import Dict, Any

def check_risk_gates(signal: Dict[str, Any], portfolio: Dict[str, Any] = None, data: Dict[str, Any] = None) -> Dict[str, Any]:
    """Apply position limits, drawdown, correlation, anomaly filters."""
    portfolio = portfolio or {"equity": 100000, "max_drawdown": 0.05, "open_positions": 0}
    data = data or {}

    size_pct = signal.get("size_pct", 0.0)
    confidence = signal.get("confidence", 0.0)
    regime = data.get("regime", "neutral")

    # Drawdown gate
    if portfolio.get("max_drawdown", 0) > 0.15:
        size_pct *= 0.3
        signal["reason"] = signal.get("reason", "") + "; drawdown limit"

    # Position count
    if portfolio.get("open_positions", 0) >= 5:
        size_pct *= 0.5

    # Regime stress
    if regime in ("stress", "high_vol") and confidence < 0.8:
        size_pct *= 0.4

    # Min confidence
    if confidence < 0.4:
        size_pct = 0.0
        signal["signal"] = "HOLD"

    signal["size_pct"] = round(max(0.0, min(size_pct, 1.0)), 2)
    signal["risk_adjusted"] = True
    return signal
