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

    def test_no_intake_or_personal_data_collection_yet(self):
        for path in ("/donate", "/request", "/get-involved"):
            response = self.client.get(path)
            self.assertIn(b"Online inquiries are not yet open", response.data)
            self.assertNotIn(b"<form", response.data)
            self.assertEqual(self.client.post(path, data={"email": "test@example.com"}).status_code, 405)

    def test_missing_page(self):
        self.assertEqual(self.client.get("/nonexistent-page").status_code, 404)

    def test_headings_and_stylesheet(self):
        response = self.client.get("/")
        self.assertIn(b'<main id="main-content">', response.data)
        self.assertIn(b'/static/site.css', response.data)
        self.assertIn(b'<nav', response.data)


if __name__ == "__main__":
    unittest.main()
