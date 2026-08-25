# ShellScripts Python Conversion

This project converts the bash utilities in the original ShellScripts repository into Python equivalents with a clearer CLI, safer argument handling, and reusable helper functions.

## Project structure

- `src/shellscripts_py/utilities/` – file and text utilities
- `src/shellscripts_py/monitoring/` – real-time monitoring utilities
- `src/shellscripts_py/infra/` – deployment automation helpers
- `src/shellscripts_py/__main__.py` – shared command entry point
- `tests/` – focused validation coverage for converted behavior

## Included conversions

- backup.sh → `shellscripts_py.utilities.backup`
- filecount.sh → `shellscripts_py.utilities.file_count`
- largestfiles.sh → `shellscripts_py.utilities.largest_files`
- diskuage.sh → `shellscripts_py.utilities.dir_usage`
- choice.sh → `shellscripts_py.utilities.choice`
- looping.sh → `shellscripts_py.utilities.looping`
- string_reverse.sh → `shellscripts_py.utilities.string_reverse`
- number_of_occurance_of_char.sh → `shellscripts_py.utilities.character_count`
- process_status.sh → `shellscripts_py.monitoring.process_status`
- log_monitoring.sh → `shellscripts_py.monitoring.log_monitoring`
- real-time.sh → `shellscripts_py.monitoring.real_time`
- tomcat_install.sh → `shellscripts_py.infra.tomcat_install`
- zookeeper.sh → `shellscripts_py.infra.zookeeper_install`

## Usage

Install the project in editable mode:

```bash
cd python_conversion
python -m pip install -e .
```

Run a command:

```bash
shellscripts backup /path/to/file
shellscripts file-count /path/to/directory
shellscripts largest-files /path/to/directory --limit 5
shellscripts string-reverse "hello"
shellscripts char-count --text "abcab" --char "a"
shellscripts process-status nginx
shellscripts log-monitor /var/log/syslog --pattern ERROR --pattern WARN
```

## Notes

- Installer scripts are designed around a plan/execution model so they can run in dry-run mode safely.
- Some bash scripts in the original repo had syntax issues; the Python versions preserve the intended behavior rather than copying broken shell logic verbatim.
- Monitoring features are best used on Unix-like systems where `pgrep` and standard process APIs are available.
