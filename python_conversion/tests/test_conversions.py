from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from shellscripts_py.infra.tomcat_install import build_tomcat_install_plan
from shellscripts_py.infra.zookeeper_install import build_zookeeper_install_plan
from shellscripts_py.monitoring.log_monitoring import find_matches
from shellscripts_py.monitoring.process_status import process_running
from shellscripts_py.utilities.backup import backup_file
from shellscripts_py.utilities.character_count import count_character_in_file, count_character_in_text
from shellscripts_py.utilities.file_count import count_files
from shellscripts_py.utilities.largest_files import largest_files
from shellscripts_py.utilities.string_reverse import reverse_string


def test_backup_file_creates_timestamped_copy(tmp_path):
    source = tmp_path / "data.txt"
    source.write_text("hello world", encoding="utf-8")

    backup_path = backup_file(source, tmp_path / "backup")

    assert backup_path.exists()
    assert backup_path.parent == tmp_path / "backup"
    assert backup_path.read_text(encoding="utf-8") == "hello world"


def test_count_files_counts_only_top_level_files(tmp_path):
    (tmp_path / "a.txt").write_text("a")
    (tmp_path / "b.txt").write_text("b")
    (tmp_path / "nested").mkdir()

    assert count_files(tmp_path) == 2


def test_largest_files_returns_sorted_results(tmp_path):
    small = tmp_path / "small.txt"
    large = tmp_path / "large.txt"
    small.write_text("abc")
    large.write_text("abcdefghijk")

    results = largest_files(tmp_path, limit=2)

    assert results[0][0].endswith("large.txt")
    assert results[1][0].endswith("small.txt")


def test_string_reverse_reverses_value():
    assert reverse_string("shell") == "llehs"


def test_character_count_in_text_and_file(tmp_path):
    assert count_character_in_text("banana", "a") == 3

    file_path = tmp_path / "sample.txt"
    file_path.write_text("banana", encoding="utf-8")
    assert count_character_in_file(file_path, "a") == 3


def test_process_running_detects_active_python_process():
    proc = subprocess.Popen([sys.executable, "-c", "import time; time.sleep(30)"])
    try:
        assert process_running(Path(sys.executable).name)
    finally:
        proc.terminate()
        proc.wait(timeout=10)


def test_log_monitor_find_matches_uses_patterns():
    lines = ["INFO starting", "ERROR failed", "WARN retrying"]
    matches = find_matches(lines, ["ERROR", "WARN"])

    assert len(matches) == 2
    assert any("ERROR" in item for item in matches)
    assert any("WARN" in item for item in matches)


def test_install_plans_are_created_for_infra_tools():
    tomcat_plan = build_tomcat_install_plan(version="9.0.89")
    zookeeper_plan = build_zookeeper_install_plan(version="3.8.4")

    assert tomcat_plan.version == "9.0.89"
    assert zookeeper_plan.version == "3.8.4"
    assert tomcat_plan.commands
    assert zookeeper_plan.commands
