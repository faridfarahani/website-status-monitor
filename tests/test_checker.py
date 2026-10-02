from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from website_status_monitor.checker import load_urls, normalize_url


class NormalizeUrlTests(unittest.TestCase):
    def test_adds_https_when_scheme_is_missing(self) -> None:
        self.assertEqual(
            normalize_url("example.com"),
            "https://example.com",
        )

    def test_keeps_existing_https_scheme(self) -> None:
        self.assertEqual(
            normalize_url("https://example.com"),
            "https://example.com",
        )

    def test_rejects_empty_url(self) -> None:
        with self.assertRaises(ValueError):
            normalize_url("   ")


class LoadUrlsTests(unittest.TestCase):
    def test_loads_urls_and_skips_comments(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "urls.txt"
            path.write_text(
                "# demo\nexample.com\nhttps://python.org\n",
                encoding="utf-8",
            )

            urls = load_urls(str(path))

            self.assertEqual(
                urls,
                ["example.com", "https://python.org"],
            )


if __name__ == "__main__":
    unittest.main()
