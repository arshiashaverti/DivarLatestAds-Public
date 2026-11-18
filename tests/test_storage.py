import tempfile
import unittest
from pathlib import Path

from divar_monitor.storage import find_new_ads, load_ids, save_ids


class StorageTests(unittest.TestCase):
    def test_save_and_load_ids(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "state.json"
            expected = {"listing-1", "listing-2"}

            save_ids(path, expected)

            self.assertEqual(load_ids(path), expected)

    def test_missing_file_returns_empty_set(self):
        with tempfile.TemporaryDirectory() as directory:
            self.assertEqual(
                load_ids(Path(directory) / "missing.json"),
                set(),
            )

    def test_find_new_ads(self):
        ads = [
            {"id": "one", "title": "A", "url": "https://divar.ir/v/one"},
            {"id": "two", "title": "B", "url": "https://divar.ir/v/two"},
        ]

        self.assertEqual(
            [ad["id"] for ad in find_new_ads(ads, {"one"})],
            ["two"],
        )


if __name__ == "__main__":
    unittest.main()