# Cyber / Data Security Architecture (v16)

Zero-trust design for automated crypto trading information systems.

## Core Principles
1. **Least Privilege**: Exchange API keys scoped to trade-only, no withdrawal, IP allowlist, short-lived where possible.
2. **Secrets Management**: Environment variables, cloud KMS/HSM, automatic rotation. Never in code, logs, or git.
3. **Encryption**: Data at rest (Fernet demo; production uses AES-GCM via KMS). TLS in transit.
4. **Integrity & Audit**: Hash-chained logs with HMAC. Immutable where possible. All actions logged with redaction.
5. **Anomaly Detection**: Multi-layer (price outliers, volume spikes, ATR spikes, signal frequency) to detect manipulation or bugs.
6. **Input Validation & Redaction**: Sanitize all inputs; redact keys, addresses, mnemonics, long tokens from outputs/logs.
7. **Rate Limiting & Circuit Breakers**: Prevent abuse or cascading failures.
8. **Isolation**: Paper/synthetic mode by default. Separate environments for research vs any future live.
9. **Supply Chain**: Pinned dependencies, licence allow-list, secret scanning (gitleaks).

## Production Recommendations
- Use dedicated cloud KMS with key rotation.
- Enable exchange IP whitelist and 2FA/hardware key.
- No withdrawal permission on trading keys.
- Monitor for anomalous API usage.
- Regular security reviews and penetration testing.
- Compliance with relevant regulations (e.g., data protection).

This is a research architecture demonstration. Adapt rigorously for any real deployment.
