import unittest

from app import app


class ApplicationTests(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_health(self):
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["status"], "ok")

    def test_home(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Every Drum Has a Story", response.data)
        self.assertIn(b"Another Chapter", response.data)
        self.assertIn(b"Donate an Instrument", response.data)
        self.assertIn(b"Request an Instrument", response.data)
        self.assertIn(b"Fast Hands Drum Studio", response.data)

    def test_public_pages(self):
        for path, heading in (
            ("/our-story", b"A Tradition Worth"),
            ("/donate", b"Give an Old Drum"),
            ("/request", b"Music Should Be"),
            ("/impact", b"From Forgotten to"),
            ("/get-involved", b"A Little Work Can Make"),
        ):
            with self.subTest(path=path):
                response = self.client.get(path)
                self.assertEqual(response.status_code, 200)
                self.assertIn(heading, response.data)
                self.assertIn(b"Hudson Valley", response.data)

    def test_donation_form_embed(self):
        response = self.client.get("/donate")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'data-fillout-id="6ZDCbVfhi6us"', response.data)
        self.assertIn(b'data-fillout-embed-type="standard"', response.data)
        self.assertIn(b'data-fillout-dynamic-resize', response.data)
        self.assertIn(b'https://server.fillout.com/embed/v1/', response.data)
        self.assertIn(b'href="/privacy"', response.data)
        self.assertNotIn(b"Online inquiries are not yet open", response.data)
        self.assertNotIn(b"<form", response.data)
        self.assertEqual(self.client.post("/donate", data={"email": "test@example.com"}).status_code, 405)

    def test_first_stage_applicant_information_embed(self):
        response = self.client.get("/request")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'data-fillout-id="gexJNppcEzus"', response.data)
        self.assertIn(b'data-fillout-embed-type="standard"', response.data)
        self.assertIn(b'data-fillout-dynamic-resize', response.data)
        self.assertIn(b'https://server.fillout.com/embed/v1/', response.data)
        self.assertIn(b"first stage", response.data.lower())
        self.assertIn(b'href="/privacy"', response.data)
        self.assertNotIn(b"Online inquiries are not yet open", response.data)
        self.assertNotIn(b"<form", response.data)
        self.assertEqual(self.client.post("/request", data={"email": "test@example.com"}).status_code, 405)

    def test_contact_form_embed(self):
        response = self.client.get("/contact")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'data-fillout-id="sjiuKo9q7Vus"', response.data)
        self.assertIn(b'data-fillout-embed-type="standard"', response.data)
        self.assertIn(b'data-fillout-dynamic-resize', response.data)
        self.assertIn(b'https://server.fillout.com/embed/v1/', response.data)
        self.assertIn(b'href="/privacy"', response.data)
        self.assertNotIn(b"<form", response.data)
        self.assertEqual(self.client.post("/contact", data={"email": "test@example.com"}).status_code, 405)
        home = self.client.get("/")
        self.assertIn(b'href="/contact"', home.data)

    def test_volunteer_inquiries_not_yet_open(self):
        response = self.client.get("/get-involved")
        self.assertIn(b"Online inquiries are not yet open", response.data)
        self.assertNotIn(b'data-fillout-id=', response.data)
        self.assertNotIn(b"<form", response.data)
        self.assertEqual(self.client.post("/get-involved", data={"email": "test@example.com"}).status_code, 405)

    def test_privacy_notice_and_disclosures(self):
        response = self.client.get("/privacy")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Privacy", response.data)
        self.assertIn(b"Fast Hands Drum Studio", response.data)
        self.assertIn(b"Google Fonts", response.data)
        self.assertIn(b"Unsplash", response.data)
        self.assertIn(b"Fillout", response.data)
        self.assertIn(b"Instrument request applicant information", response.data)
        self.assertIn(b"General contact messages", response.data)
        self.assertIn(b"501(c)(3)", response.data)
        self.assertNotIn(b"<form", response.data)
        home = self.client.get("/")
        self.assertIn(b'href="/privacy"', home.data)
        self.assertIn(b"not a separately incorporated nonprofit", home.data)

    def test_performance_and_accessibility_hints(self):
        home = self.client.get("/")
        self.assertIn(b'fetchpriority="high"', home.data)
        self.assertIn(b'loading="lazy"', home.data)
        self.assertIn(b'decoding="async"', home.data)
        self.assertIn(b'sizes="(max-width: 860px) 100vw, 45vw"', home.data)
        self.assertIn(b'aria-label="Toggle navigation menu"', home.data)
        self.assertIn(b'<a href="/">Home</a>', home.data)
        self.assertIn(b'href="#main-content"', home.data)
        stylesheet = self.client.get("/static/site.css")
        self.assertEqual(stylesheet.status_code, 200)
        self.assertIn(b"prefers-reduced-motion:reduce", stylesheet.data)
        self.assertIn(b"focus-visible", stylesheet.data)

    def test_seo_metadata(self):
        for path in ("/", "/our-story", "/donate", "/request", "/impact", "/get-involved", "/contact", "/privacy"):
            with self.subTest(path=path):
                response = self.client.get(path)
                self.assertEqual(response.status_code, 200)
                self.assertIn(('href="https://grandpasdrum.com' + path + '"').encode(), response.data)
                self.assertIn(b'name="description"', response.data)
                self.assertIn(b'property="og:url"', response.data)
        self.assertIn(b'application/ld+json', self.client.get("/").data)
        self.assertIn(b'parentOrganization', self.client.get("/").data)
        self.assertIn(b'noindex, follow', self.client.get("/missing").data)

    def test_sitemap_and_robots(self):
        sitemap = self.client.get("/sitemap.xml")
        self.assertEqual(sitemap.status_code, 200)
        self.assertIn(b"application/xml", sitemap.content_type.encode())
        for path in ("/", "/our-story", "/donate", "/request", "/impact", "/get-involved", "/contact", "/privacy"):
            self.assertIn(("https://grandpasdrum.com" + path + "</").encode(), sitemap.data)
        self.assertNotIn(b"/health", sitemap.data)
        robots = self.client.get("/robots.txt")
        self.assertEqual(robots.status_code, 200)
        self.assertEqual(robots.data, b"User-agent: *\\nAllow: /\\nSitemap: https://grandpasdrum.com/sitemap.xml\\n")

    def test_missing_page(self):
        self.assertEqual(self.client.get("/nonexistent-page").status_code, 404)

    def test_headings_and_stylesheet(self):
        response = self.client.get("/")
        self.assertIn(b'<main id="main-content">', response.data)
        self.assertIn(b'/static/site.css', response.data)
        self.assertIn(b'<nav', response.data)


if __name__ == "__main__":
    unittest.main()
