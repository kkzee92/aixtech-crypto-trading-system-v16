"""Enhanced multi-factor adaptive strategies per asset class (v16)."""
from abc import ABC, abstractmethod
from typing import Dict, Any

class BaseStrategy(ABC):
    name: str = "base"
    asset_class: str = "general"

    @abstractmethod
    def generate_signal(self, data: Dict[str, Any]) -> Dict[str, Any]:
        pass

    def _safe_get(self, data: Dict[str, Any], key: str, default: float = 0.0) -> float:
        try:
            return float(data.get(key, default))
        except (TypeError, ValueError):
            return default

    def _vol_adjust(self, base_size: float, atr_pct: float) -> float:
        if atr_pct > 12:
            return base_size * 0.25
        elif atr_pct > 7:
            return base_size * 0.5
        elif atr_pct > 4:
            return base_size * 0.75
        return base_size

    def _trend_strength_ok(self, adx: float, min_adx: float = 20.0) -> bool:
        return adx >= min_adx

class MajorsStrategy(BaseStrategy):
    name = "majors_hybrid_v16"
    asset_class = "majors"

    def generate_signal(self, data: Dict[str, Any]) -> Dict[str, Any]:
        price = self._safe_get(data, "price")
        ema_50 = self._safe_get(data, "ema_50", price)
        ema_200 = self._safe_get(data, "ema_200", price)
        rsi = self._safe_get(data, "rsi", 50.0)
        volume_ratio = self._safe_get(data, "volume_ratio", 1.0)
        funding_rate = self._safe_get(data, "funding_rate", 0.0)
        atr_pct = self._safe_get(data, "atr_pct", 3.0)
        regime = data.get("regime", "neutral")
        bb_upper = self._safe_get(data, "bb_upper", price * 1.02)
        bb_lower = self._safe_get(data, "bb_lower", price * 0.98)
        adx = self._safe_get(data, "adx", 25.0)
        mtf = self._safe_get(data, "mtf_consistency", 0.7)

        signal = "HOLD"
        confidence = 0.3
        reason = "Neutral"
        size_pct = 0.4

        if regime in ("stress", "high_vol"):
            return {"signal": "HOLD", "confidence": 0.1, "reason": "Stress/high-vol regime - stand aside", "size_pct": 0.0, "asset_class": self.asset_class}

        trend_ok = self._trend_strength_ok(adx, 22)
        mtf_ok = mtf > 0.65

        if price > ema_50 > ema_200 and volume_ratio > 1.15 and price < bb_upper and trend_ok and mtf_ok:
            signal, confidence, reason, size_pct = "BUY", 0.85, "Bullish trend + ADX + MTF + volume + within BB", 1.0
        elif price < ema_50 < ema_200 and volume_ratio > 1.05 and price > bb_lower and trend_ok:
            signal, confidence, reason, size_pct = "SELL", 0.78, "Bearish trend + ADX", 0.85
        elif rsi < 28 and price < ema_50 * 0.96 and price < bb_lower and mtf_ok:
            signal, confidence, reason, size_pct = "BUY", 0.72, "Oversold reversion + BB + MTF", 0.55
        elif rsi > 72 and price > ema_50 * 1.04 and price > bb_upper:
            signal, confidence, reason, size_pct = "SELL", 0.68, "Overbought reversion", 0.45

        if funding_rate > 0.012 and signal == "BUY":
            confidence *= 0.82
            reason += "; high funding"
        size_pct = self._vol_adjust(size_pct, atr_pct)

        return {"signal": signal, "confidence": round(confidence, 2), "reason": reason, "size_pct": round(size_pct, 2), "asset_class": self.asset_class}

class LargeAltsStrategy(BaseStrategy):
    name = "large_alts_momentum_v16"
    asset_class = "large_alts"

    def generate_signal(self, data: Dict[str, Any]) -> Dict[str, Any]:
        btc_relative = self._safe_get(data, "btc_relative_strength", 1.0)
        volume_ratio = self._safe_get(data, "volume_ratio", 1.0)
        macd_hist = self._safe_get(data, "macd_histogram", 0.0)
        atr_pct = self._safe_get(data, "atr_pct", 4.0)
        regime = data.get("regime", "neutral")
        adx = self._safe_get(data, "adx", 25.0)
        mtf = self._safe_get(data, "mtf_consistency", 0.7)

        signal, confidence, reason, size_pct = "HOLD", 0.35, "Awaiting confirmation", 0.35

        if regime in ("stress", "high_vol"):
            return {"signal": "HOLD", "confidence": 0.12, "reason": "Stress - reduced exposure", "size_pct": 0.05, "asset_class": self.asset_class}

        if btc_relative > 1.06 and macd_hist > 0.2 and volume_ratio > 1.4 and self._trend_strength_ok(adx, 25) and mtf > 0.6:
            signal, confidence, reason, size_pct = "BUY", 0.88, "RS + MACD + volume + ADX + MTF", 0.95
        elif btc_relative < 0.94 and macd_hist < -0.2:
            signal, confidence, reason, size_pct = "SELL", 0.78, "Underperforming BTC", 0.75

        size_pct = self._vol_adjust(size_pct, atr_pct)
        return {"signal": signal, "confidence": round(confidence, 2), "reason": reason, "size_pct": round(size_pct, 2), "asset_class": self.asset_class}

class DeFiStrategy(BaseStrategy):
    name = "defi_protocol_aware_v16"
    asset_class = "defi"

    def generate_signal(self, data: Dict[str, Any]) -> Dict[str, Any]:
        tvl_change = self._safe_get(data, "tvl_change_7d", 0.0)
        fee_change = self._safe_get(data, "fee_revenue_change", 0.0)
        rsi = self._safe_get(data, "rsi", 50.0)
        onchain_active = self._safe_get(data, "active_addresses_change", 0.0)
        regime = data.get("regime", "neutral")

        signal, confidence, reason, size_pct = "HOLD", 0.32, "Monitoring protocol", 0.25

        if regime == "stress":
            return {"signal": "HOLD", "confidence": 0.1, "reason": "Stress - avoid DeFi", "size_pct": 0.0, "asset_class": self.asset_class}

        if tvl_change > 0.06 and fee_change > 0.12 and rsi < 58 and onchain_active > 0.03:
            signal, confidence, reason, size_pct = "BUY", 0.80, "Growing TVL/fees + activity", 0.65
        elif tvl_change < -0.12 or fee_change < -0.18 or onchain_active < -0.06:
            signal, confidence, reason, size_pct = "SELL", 0.73, "Declining metrics", 0.55

        return {"signal": signal, "confidence": round(confidence, 2), "reason": reason, "size_pct": size_pct, "asset_class": self.asset_class}

class StablecoinStrategy(BaseStrategy):
    name = "stable_arb_yield_v16"
    asset_class = "stablecoins"

    def generate_signal(self, data: Dict[str, Any]) -> Dict[str, Any]:
        premium = self._safe_get(data, "premium_to_peg", 0.0)
        yield_diff = self._safe_get(data, "yield_diff_bps", 0.0)

        signal, confidence, reason, size_pct = "HOLD", 0.55, "Peg stable", 0.15

        if abs(premium) > 0.006:
            signal = "BUY" if premium < 0 else "SELL"
            confidence, reason, size_pct = 0.92, f"Arb: premium {premium:.4f}", 1.0
        elif yield_diff > 60:
            signal, confidence, reason, size_pct = "BUY", 0.70, "Yield opportunity", 0.45

        return {"signal": signal, "confidence": round(confidence, 2), "reason": reason, "size_pct": size_pct, "asset_class": self.asset_class}

class HighVolStrategy(BaseStrategy):
    name = "high_vol_controlled_v16"
    asset_class = "high_volatility"

    def generate_signal(self, data: Dict[str, Any]) -> Dict[str, Any]:
        atr_pct = self._safe_get(data, "atr_pct", 5.0)
        volume_spike = self._safe_get(data, "volume_ratio", 1.0)
        rsi = self._safe_get(data, "rsi", 50.0)
        regime = data.get("regime", "neutral")

        signal, confidence, reason, size_pct = "HOLD", 0.15, "High vol - waiting", 0.05

        if regime not in ("stress",) and volume_spike > 3.5 and atr_pct < 9.0 and 35 < rsi < 65:
            signal, confidence, reason, size_pct = "BUY", 0.55, "Controlled volume spike + neutral RSI", 0.12

        size_pct = self._vol_adjust(size_pct, atr_pct)
        return {"signal": signal, "confidence": round(confidence, 2), "reason": reason, "size_pct": round(size_pct, 2), "asset_class": self.asset_class}

STRATEGIES: Dict[str, BaseStrategy] = {
    "majors": MajorsStrategy(),
    "large_alts": LargeAltsStrategy(),
    "defi": DeFiStrategy(),
    "stablecoins": StablecoinStrategy(),
    "high_volatility": HighVolStrategy(),
}

def get_strategy(asset_class: str) -> BaseStrategy:
    return STRATEGIES.get(asset_class, MajorsStrategy())
