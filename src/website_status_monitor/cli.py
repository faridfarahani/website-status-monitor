from __future__ import annotations

import argparse

from website_status_monitor.checker import check_urls_concurrently, load_urls
from website_status_monitor.reporting import write_json_report


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Check website availability and response time."
    )
    parser.add_argument(
        "file",
        help="Text file containing one URL per line.",
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=5.0,
        help="Request timeout in seconds. Default: 5",
    )
    parser.add_argument(
        "--workers",
        type=int,
        default=5,
        help="Number of concurrent workers. Default: 5",
    )
    parser.add_argument(
        "--json-output",
        help="Optional path for saving results as JSON.",
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()
    urls = load_urls(args.file)

    results = check_urls_concurrently(
        urls,
        timeout=args.timeout,
        workers=args.workers,
    )

    up_count = 0

    for result in results:

        if result.is_up:
            up_count += 1
            print(
                f"[UP]   {result.url:<35} "
                f"{result.status_code:<4} "
                f"{result.response_ms} ms"
            )
        else:
            detail = result.error or "unknown error"
            status = result.status_code if result.status_code is not None else "-"
            print(f"[DOWN] {result.url:<35} {status:<4} {detail}")

    print()
    print(f"Checked: {len(urls)} | Up: {up_count} | Down: {len(urls) - up_count}")

    if args.json_output:
        report_path = write_json_report(results, args.json_output)
        print(f"JSON report: {report_path}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
