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
        self.assertIn(b"A second life for every beat", response.data)
        self.assertIn(b"not presently a registered nonprofit", response.data)
        self.assertIn(b"Donation intake is coming soon", response.data)


if __name__ == "__main__":
    unittest.main()
