# Deployment plan

The deployment workflow is **manual-only** until VPS runtime inspection, verified SSH host key, and web process configuration are complete.

## GitHub Actions secrets

- `VPS_HOST` — server SSH hostname
- `VPS_USER` — SSH account username
- `VPS_SSH_KEY` — private key for authorized deployment account (never commit)
- `VPS_KNOWN_HOSTS` — server host public key entry verified against DreamHost's host fingerprint

## Next steps

1. Determine Python version, available processes, and hosting directory.
2. Verify SSH host fingerprint and add `VPS_KNOWN_HOSTS`.
3. Confirm deployment key authentication independently.
4. Configure a Python virtual environment, persistent storage outside deployed code, Gunicorn, and web proxy/domain.
5. Test a manual deployment and health check.
6. Enable automatic deployment on protected `main` after successful verification.

Do not put API keys, private SSH keys, .env files, donor data, or uploads into Git.
