import os
import unittest
from unittest.mock import patch

from divar_monitor.config import (
    DEFAULT_URL,
    get_telegram_credentials,
    load_settings,
)


class ConfigTests(unittest.TestCase):
    def test_default_settings(self):
        with patch.dict(os.environ, {}, clear=True):
            settings = load_settings()
            self.assertEqual(settings.url, DEFAULT_URL)
            self.assertEqual(settings.max_ads, 10)

    def test_telegram_credentials_required(self):
        with patch.dict(os.environ, {}, clear=True):
            with self.assertRaises(RuntimeError):
                get_telegram_credentials()

    def test_telegram_credentials_loaded(self):
        values = {
            "TELEGRAM_BOT_TOKEN": "test-token",
            "TELEGRAM_CHAT_ID": "test-chat",
        }
        with patch.dict(os.environ, values, clear=True):
            self.assertEqual(
                get_telegram_credentials(),
                ("test-token", "test-chat"),
            )


if __name__ == "__main__":
    unittest.main()