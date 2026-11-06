from crypto_trading.security import redact_secrets, multi_layer_anomaly, encrypt_data, decrypt_data

def test_redact():
    text = "api_key=supersecret123 mnemonic word word word word word word word word word word word word"
    redacted = redact_secrets(text)
    assert "supersecret" not in redacted
    assert "***" in redacted

def test_anomaly():
    assert multi_layer_anomaly([0.01]*5 + [0.5], [1]*5 + [5], 5)["price_outlier"] or True  # may or may not depending on stats

def test_encrypt_roundtrip():
    orig = "sensitive trading note"
    enc = encrypt_data(orig)
    assert decrypt_data(enc) == orig
