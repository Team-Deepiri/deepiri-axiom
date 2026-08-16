---
name: axiom-secrets-hygiene
description: Prevent secrets from landing in Deepiri repos, logs, or client bundles.
---

# Axiom Secrets Hygiene

Use when adding new credentials, API keys, or tokens anywhere in the stack.

## Rules
- Secrets live in `deepiri-wooven`-managed storage or environment injection — never hardcoded, never in `.env` files committed to git.
- Check `VITE_*` / client-bundled env vars specifically — anything prefixed for frontend build tools ships to the browser.
- Rotate immediately, don't just delete, if a secret is found in git history — `git rm` alone leaves it in history.

Grep the diff for common patterns (`api_key`, `secret`, `token =`, base64-looking strings) before approving, not just trusting `.gitignore`.
