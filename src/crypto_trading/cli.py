"""CLI for demo and paper signals (v16)."""
import argparse
from crypto_trading.data import generate_synthetic, validate_data
from crypto_trading.strategies import get_strategy
from crypto_trading.risk import check_risk_gates
from crypto_trading.security import redact_secrets, multi_layer_anomaly, AuditLog

def main():
    parser = argparse.ArgumentParser(description="AIxTech Crypto Trading System v16 (paper only)")
    parser.add_argument("command", choices=["demo", "signal"], help="Command to run")
    parser.add_argument("--asset-class", default="majors", choices=["majors", "large_alts", "defi", "stablecoins", "high_volatility"])
    args = parser.parse_args()

    if args.command == "demo":
        print("=== AIxTech Crypto Trading System v16 Demo (paper/research only) ===")
        for ac in ["majors", "large_alts", "defi", "stablecoins", "high_volatility"]:
            data = generate_synthetic(ac)
            if not validate_data(data):
                print(f"{ac}: invalid data")
                continue
            strat = get_strategy(ac)
            sig = strat.generate_signal(data)
            sig = check_risk_gates(sig, data=data)
            print(f"\n[{ac.upper()}] {sig['signal']} conf={sig['confidence']} size={sig['size_pct']}% | {sig['reason']}")
            # Anomaly demo
            anomalies = multi_layer_anomaly([0.01, -0.02, 0.015, 0.1], [1.0, 1.2, 1.1, 4.5], 3)
            print(f"  Anomalies: {anomalies}")
        print("\nSecurity note: all outputs redacted. No live execution.")
        print(redact_secrets("Demo key=abc123privatekeyseedphrase here"))

    elif args.command == "signal":
        data = generate_synthetic(args.asset_class)
        strat = get_strategy(args.asset_class)
        sig = check_risk_gates(strat.generate_signal(data), data=data)
        print(sig)

if __name__ == "__main__":
    main()
