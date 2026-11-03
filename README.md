# Grandpa's Drum

Grandpa's Drum is a philanthropic initiative of Fast Hands Drum Studio, beginning in New York's Hudson Valley. The project aims to collect, restore, and redistribute used percussion instruments to individuals, schools, and community organizations in need.

## Site architecture

- Flask renders the public homepage and five editorial pages.
- The shared layout lives in `templates/base.html`, page content in `templates/index.html` and `templates/page.html`, and styling in `static/site.css`.
- `GET /health` returns a JSON health check.
- Run tests with `python -m unittest discover -s tests -v`.
- Feature branches and pull requests are used for changes. Merges to `main` trigger the configured deployment workflow.

## Launch safety

**The donation page embeds a Fillout form** (ID `6ZDCbVfhi6us`) using the vendor's standard script and dynamic resizing. Submissions, uploads, notifications, spam protection, storage, and account access are managed in Fillout, not by Flask. The site has no native POST endpoint for donation submissions. Instrument requests and volunteer inquiries are not enabled yet.

Before merging this change or accepting real submissions: verify the form is published and accessible; review its fields and confirmation flow; restrict who may access Fillout submissions and uploaded files; configure notifications and spam protection; establish a dedicated privacy contact channel, a retention/deletion process, and confirm the published privacy notice accurately reflects actual Fillout settings. Also restrict direct access to the Gunicorn service port and review reverse-proxy and HTTPS settings. Test on desktop and mobile.

Do not create a duplicate Flask intake backend unless a later decision calls for custom data storage.

The site accurately identifies Grandpa's Drum as an initiative of Fast Hands Drum Studio. It does **not** claim 501(c)(3) status or tax-deductible donations.

## Design and photography

Heritage palette: aged paper `#F3E9D5`, walnut `#493426`, oxblood `#773C32`, antique brass `#B49259`, and charcoal `#292722`.

The homepage temporarily uses two externally hosted photos from [ASBA Drums on Unsplash](https://unsplash.com/@asbadrums), licensed under the Unsplash License. Replace these with original restoration photography when it is available. The site functions without the images but they are recommended for the complete design.
