from __future__ import annotations

import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


@dataclass(frozen=True)
class CheckResult:
    url: str
    is_up: bool
    status_code: int | None
    response_ms: int | None
    error: str | None = None


def normalize_url(url: str) -> str:
    value = url.strip()

    if not value:
        raise ValueError("URL cannot be empty.")

    if not value.startswith(("http://", "https://")):
        value = "https://" + value

    return value


def check_url(url: str, timeout: float = 5.0) -> CheckResult:
    normalized = normalize_url(url)
    request = Request(
        normalized,
        headers={"User-Agent": "WebsiteStatusMonitor/0.1"},
    )

    started = time.perf_counter()

    try:
        with urlopen(request, timeout=timeout) as response:
            elapsed_ms = int((time.perf_counter() - started) * 1000)
            status_code = getattr(response, "status", 200)

            return CheckResult(
                url=normalized,
                is_up=200 <= status_code < 400,
                status_code=status_code,
                response_ms=elapsed_ms,
            )

    except HTTPError as exc:
        elapsed_ms = int((time.perf_counter() - started) * 1000)

        return CheckResult(
            url=normalized,
            is_up=False,
            status_code=exc.code,
            response_ms=elapsed_ms,
            error=f"HTTP {exc.code}",
        )

    except URLError as exc:
        reason = getattr(exc, "reason", exc)

        return CheckResult(
            url=normalized,
            is_up=False,
            status_code=None,
            response_ms=None,
            error=str(reason),
        )

    except TimeoutError:
        return CheckResult(
            url=normalized,
            is_up=False,
            status_code=None,
            response_ms=None,
            error="timeout",
        )


def load_urls(path: str) -> list[str]:
    with open(path, "r", encoding="utf-8") as handle:
        urls = [
            line.strip()
            for line in handle
            if line.strip() and not line.lstrip().startswith("#")
        ]

    if not urls:
        raise ValueError("No URLs found in input file.")

    return urls

def check_urls_concurrently(urls: list[str], timeout: float = 5.0, workers: int = 5) -> list[CheckResult]:
    if workers < 1:
        raise ValueError("workers must be at least 1")

    results: list[CheckResult | None] = [None] * len(urls)

    with ThreadPoolExecutor(max_workers=workers) as executor:
        future_map = {executor.submit(check_url, url, timeout): index for index, url in enumerate(urls)}

        for future in as_completed(future_map):
            index = future_map[future]
            results[index] = future.result()

    return [result for result in results if result is not None]
