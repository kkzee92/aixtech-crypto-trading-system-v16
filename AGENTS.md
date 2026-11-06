# AGENTS.md - rules for AI coding agents in this repo

These rules apply to any AI coding assistant working in this repository.

## 1. Scope and autonomy
- Work only on the task in the current brief. If ambiguous, stop and ask.
- Keep changes small: one task = one branch = one PR.
- Never push to main, merge own PR, or edit CI gates to make them pass without approval.

## 2. Data and privacy / Security
- Use only synthetic fixtures or public data. Never paste real API keys, private keys, seeds, mnemonics, or personal data.
- All secrets from environment. gitleaks and redaction helpers must pass.
- Paper/research only. No live trading code paths.

## 3. Secrets
- No API keys, tokens, passwords, private keys in code, fixtures, docs or commits.
- Read from env (e.g. EXCHANGE_API_KEY). Never commit.

## 4. Engineering rules
- Python >= 3.10. Prefer stdlib; cryptography for encryption demos only.
- Tests for every behavior. No network in tests.
- Run local checks before review.

## 5. Disclosure
- Commits carry AI-Assisted: yes (<tool>) and Human-Review: pending|<name, date>.
- Document in PRs what was AI-generated.

## 6. Definition of Done
CI green + human review recorded.
