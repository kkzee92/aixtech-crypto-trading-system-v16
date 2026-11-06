# AIxTech Crypto Trading System v16

> Enhanced paper-only automated cryptocurrency trading information system with advanced multi-factor adaptive strategies per asset class, refined regime detection, multi-timeframe proxies, expanded zero-trust cyber and data security architecture, and AI-agent harness principles for safe development.

**Disclaimer:** Research and educational purposes only. No live order execution, no withdrawal permissions, no financial advice. Cryptocurrency trading involves substantial risk of loss. This is not investment advice.

## Overview
Builds on previous versions (v15 and earlier) and the AI coding-agent harness from [zeekiankok92/aixtech-agent-harness-demo](https://github.com/zeekiankok92/aixtech-agent-harness-demo). Features:

- Asset-class specific strategies: Majors (BTC/ETH), Large Alts, DeFi, Stablecoins, High-Volatility
- Regime-aware, multi-factor signals with volatility scaling, Bollinger Bands, ADX trend strength, on-chain proxies, adaptive filters, vol-adjusted sizing, multi-TF consistency checks
- Advanced risk gates: position limits, drawdown controls, correlation awareness, multi-layer anomaly, dynamic sizing
- Zero-trust security: encryption helpers (KMS/HSM recommended for prod), hash-chained audits with HMAC, expanded multi-layer anomaly detection, input validation, comprehensive secret redaction (including BIP39/seed phrases), rate limiting simulation
- Synthetic data mode by default for CI and safe agent development
- CI gates inspired by the harness (lint, tests, secret scan)

## Quick Start
```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python -m crypto_trading demo
```

## Architecture
See [docs/architecture.md](docs/architecture.md).

## Strategies
See [docs/trading-strategies.md](docs/trading-strategies.md).

## Security
See [SECURITY.md](SECURITY.md) and [docs/security-architecture.md](docs/security-architecture.md).

## Enhancements in v16
- Added ADX for trend strength confirmation in majors and alts
- Multi-timeframe proxy consistency filters
- Improved regime detection with more states
- Expanded anomaly detection layers and better redaction for crypto secrets
- Stronger audit chain with optional HMAC
- Updated risk module integration
- More comprehensive synthetic data features
- Updated docs for production security recommendations (IP whitelist, no withdrawals, KMS, key rotation)

## Licence
MIT
