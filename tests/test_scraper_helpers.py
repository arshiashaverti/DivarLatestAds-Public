import unittest
from urllib.parse import urljoin, urlparse


class ScraperUrlTests(unittest.TestCase):
    def test_relative_listing_url(self):
        link = urljoin("https://divar.ir", "/v/example-id")
        self.assertEqual(link, "https://divar.ir/v/example-id")

    def test_listing_id_extraction(self):
        parsed = urlparse("https://divar.ir/v/example-id")
        self.assertEqual(parsed.path.rstrip("/").split("/")[-1], "example-id")


if __name__ == "__main__":
    unittest.main()