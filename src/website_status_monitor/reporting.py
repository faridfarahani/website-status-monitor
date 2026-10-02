from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path
from typing import Iterable

from website_status_monitor.checker import CheckResult


def write_json_report(results: Iterable[CheckResult], output_path: str | Path) -> Path:
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    data = [asdict(result) for result in results]

    output_path.write_text(
        json.dumps(data, indent=2, ensure_ascii=False),
        encoding='utf-8',
    )

    return output_path
