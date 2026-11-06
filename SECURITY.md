# Security Policy

## Supported Versions
v16 is the current research version.

## Reporting a Vulnerability
Please open a private issue or contact the maintainer. Do not disclose secrets publicly.

## Key Principles (Zero-Trust)
- Least privilege: API keys with trade-only scope, no withdrawals, IP allowlist.
- Secrets in env / KMS / HSM. Never in repo.
- Encryption for sensitive data at rest (Fernet demo; use proper KMS in prod).
- Hash-chained audit logs with HMAC integrity.
- Multi-layer anomaly detection on price, volume, signal frequency.
- Input validation and secret redaction on all logs/outputs.
- Rate limiting and circuit breakers recommended.
- Synthetic data only in CI/dev.

See docs/security-architecture.md for details.
