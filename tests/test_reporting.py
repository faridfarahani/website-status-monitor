from __future__ import annotations

import csv
import tempfile
import unittest
from pathlib import Path

from website_status_monitor.checker import CheckResult
from website_status_monitor.reporting import write_csv_report


class CsvReportTests(unittest.TestCase):
    def test_writes_csv_report(self) -> None:
        results = [
            CheckResult(
                url="https://example.com",
                is_up=True,
                status_code=200,
                response_ms=123,
                error=None,
            )
        ]

        with tempfile.TemporaryDirectory() as temp_dir:
            output_path = Path(temp_dir) / "status.csv"
            written_path = write_csv_report(results, output_path)

            with written_path.open(
                "r",
                encoding="utf-8-sig",
                newline="",
            ) as handle:
                rows = list(csv.DictReader(handle))

            self.assertEqual(len(rows), 1)
            self.assertEqual(rows[0]["url"], "https://example.com")
            self.assertEqual(rows[0]["is_up"], "True")
            self.assertEqual(rows[0]["status_code"], "200")
            self.assertEqual(rows[0]["response_ms"], "123")
            self.assertEqual(rows[0]["error"], "")


if __name__ == "__main__":
    unittest.main()
