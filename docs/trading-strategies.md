# Enhanced Trading Strategies by Asset Class (v16)

All strategies are multi-factor, regime-aware, volatility-adjusted, ADX/MTF filtered, and return structured signals with confidence and size_pct. Risk gates applied post-strategy.

## Majors (BTC, ETH)
Hybrid trend (EMA 50/200 + volume + Bollinger Bands + ADX trend strength + multi-TF consistency) + mean reversion (RSI). Funding rate adjustment and volatility scaling. Regime filter suppresses in stress/high-vol. Size reduced in high ATR.

## Large Alts
Relative strength vs BTC + MACD histogram + volume + ADX + MTF. Adaptive to BTC regime. Vol-adjusted sizing.

## DeFi
Protocol metrics (TVL change, fee revenue, active addresses) + price/RSI. Exit on fundamental deterioration. Avoid in stress.

## Stablecoins
Peg premium arbitrage and yield differential signals. Low directional risk. Higher confidence on clear arb.

## High Volatility
Strict filters: extreme volume spike + moderate ATR + neutral RSI + not stress. Tiny position sizes only. Strong vol adjustment.

See `src/crypto_trading/strategies.py` for implementation details. All research/paper only. No live execution. Past performance of synthetic data is not indicative of future results.
