from __future__ import annotations

import subprocess
from datetime import datetime
from pathlib import Path
from typing import Iterable, Sequence


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def normalize_path(path: str | Path) -> Path:
    return Path(path).expanduser().resolve()


def timestamped_backup_path(file_path: str | Path, backup_dir: str | Path = "backup") -> Path:
    path = normalize_path(file_path)
    backup_root = normalize_path(backup_dir)
    backup_root.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%y%m%d_%H%M%S")
    return backup_root / f"{path.name}_{timestamp}"


def run_command(command: Sequence[str], *, check: bool = True) -> subprocess.CompletedProcess[str]:
    completed = subprocess.run(command, capture_output=True, text=True, check=False)
    if check and completed.returncode != 0:
        raise RuntimeError(completed.stderr.strip() or completed.stdout.strip() or f"Command failed: {' '.join(command)}")
    return completed


def iter_lines(file_path: str | Path) -> Iterable[str]:
    with Path(file_path).open("r", encoding="utf-8", errors="replace") as file_obj:
        yield from file_obj
