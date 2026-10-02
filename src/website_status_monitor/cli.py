from __future__ import annotations

import argparse

from website_status_monitor.checker import check_url, load_urls


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
    return parser


def main() -> int:
    args = build_parser().parse_args()
    urls = load_urls(args.file)

    up_count = 0

    for url in urls:
        result = check_url(url, timeout=args.timeout)

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

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
