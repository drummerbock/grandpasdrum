# Grandpa's Drum

Grandpa's Drum is a philanthropic initiative of Fast Hands Drum Studio, beginning in New York's Hudson Valley. The project aims to collect, restore, and redistribute used percussion instruments to individuals, schools, and community organizations in need.

## Site architecture

- Flask renders the public homepage and five editorial pages.
- The shared layout lives in `templates/base.html`, page content in `templates/index.html` and `templates/page.html`, and styling in `static/site.css`.
- `GET /health` returns a JSON health check.
- Run tests with `python -m unittest discover -s tests -v`.
- Feature branches and pull requests are used for changes. Merges to `main` trigger the configured deployment workflow.

## Launch safety

**Online instrument donation, recipient, and volunteer inquiries are intentionally not enabled yet.** The public pages describe the proposed process, but do not render forms, accept POST submissions, upload photos, or store personal data.

Before enabling intake: restrict direct access to the Gunicorn service port, review reverse-proxy and HTTPS settings, design a private database/storage and access controls, implement CSRF protection and rate limiting, establish spam controls, photo upload validation, privacy/retention practices, and notification handling. Add a secure administrator workflow before collecting submissions.

The site accurately identifies Grandpa's Drum as an initiative of Fast Hands Drum Studio. It does **not** claim 501(c)(3) status or tax-deductible donations.

## Design and photography

Heritage palette: aged paper `#F3E9D5`, walnut `#493426`, oxblood `#773C32`, antique brass `#B49259`, and charcoal `#292722`.

The homepage temporarily uses two externally hosted photos from [ASBA Drums on Unsplash](https://unsplash.com/@asbadrums), licensed under the Unsplash License. Replace these with original restoration photography when it is available. The site functions without the images but they are recommended for the complete design.
