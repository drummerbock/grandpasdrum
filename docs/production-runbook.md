# Grandpa's Drum — Production Operations

This runbook documents checks and procedures; it does **not** configure backups, uptime monitoring, email, or Google Search Console automatically. Never commit passwords, SSH keys, recovery codes, or personal inquiry data.

## Deployment verification

1. Merge a reviewed PR after GitHub's **Test** job passes.
2. Confirm the **Deploy to DreamHost VPS** workflow succeeds. It now runs tests before transfer, runs tests on the VPS, restarts the user service, checks the loopback health endpoint, and checks the public HTTPS health, robots and sitemap endpoints.
3. Manually check the homepage, /donate, /request, /privacy, mobile navigation, and external images.
4. Check https://grandpasdrum.com/health, /robots.txt, and /sitemap.xml. Confirm HTTP redirects to HTTPS and the canonical non-www hostname.
5. On failure, review the GitHub Actions logs and the service's journal on the VPS. Do not publish sensitive logs.

## Recovery and rollback

- Identify the last known-good commit on main. Do **not** assume GitHub workflow cancellation rolls back a partial deployment.
- The current deployment extracts over the working directory and restarts the service; it is **not atomic** and does not automatically roll back.
- To revert a bad change, use a reviewed GitHub revert PR and let the normal workflow redeploy, if the pipeline is functioning.
- If the site is unavailable, an authorized operator can inspect the VPS user service and its journal, then restore a known-good release. Avoid destructive commands without verifying the deployment directory.
- Test restoration of a backup before relying on it. Keep at least one off-server copy.

## Backup policy — configure outside this PR

- Verify DreamHost snapshot/backup coverage and actual restore options for this VPS. Do not assume the hosting provider retains a usable application backup.
- Back up application configuration and any persistent content or future inquiry data securely. GitHub already versions source code, but does not protect server secrets, uploaded files, or future form-provider records.
- Set a schedule, retention period, encrypted off-server destination, responsible owner, and periodic restore test. Record them privately.

## Monitoring — configure outside this PR

- Set up an independent HTTPS uptime check for https://grandpasdrum.com/health with alerts to an operator-controlled address.
- Monitor TLS expiry, HTTP failures, VPS disk capacity, service restarts and deployment failures.
- Keep alert destinations and credentials out of the repository.

## Google Search Console — manual setup

1. Open https://search.google.com/search-console and add a **Domain property** for grandpasdrum.com.
2. Verify ownership using the DNS TXT record provided by Google in DreamHost DNS. Do not invent or commit the verification token.
3. Submit https://grandpasdrum.com/sitemap.xml under Sitemaps.
4. Inspect the homepage and donation/request pages; monitor indexing and search performance over time. Submission does not guarantee indexing.

## Branded email — manual setup

- Decide on an operator-managed address such as hello@grandpasdrum.com, then provision the mailbox or alias with the chosen provider.
- Configure provider-specified MX, SPF, DKIM and DMARC records in DNS, testing delivery and replies before publishing the address.
- Do not add a placeholder address to public pages until it works.

## Forms go-live gate

Before enabling Fillout or another provider, update /privacy to name the provider, fields collected, retention/access/deletion process, and third-party processing. Verify consent, spam protection, recipient notifications and access permissions. The website currently does not accept inquiries; do not claim otherwise.

## Launch checklist

- [ ] CI tests and deployment checks pass
- [ ] Public pages and mobile menu manually verified
- [ ] DNS and HTTPS canonical behavior verified
- [ ] Google Search Console verified and sitemap submitted
- [ ] Independent uptime alert configured and tested
- [ ] Backup and restore tested
- [ ] Branded email provisioned and tested
- [ ] Form privacy review completed before intake launch
