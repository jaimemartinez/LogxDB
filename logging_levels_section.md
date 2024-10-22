
---

## Customizable Logging Levels

The LogxDB parser now supports **customizable logging levels**. You can set the logging level to one of the following:

- **DEBUG**: Detailed information for diagnosing problems.
- **INFO**: General information about the program’s execution.
- **WARNING**: Indicates a potential issue that does not stop the program.
- **ERROR**: A problem that causes part of the program to fail.
- **CRITICAL**: A serious issue causing the program to stop.

By default, the logging level is set to `INFO`. If needed, you can **log to a file** by specifying a log file path.

### Example Usage in Code

```python
from parser import LogParser

# Initialize the parser with a custom logging level and optional log file
parser = LogParser(
    db_path="logs.db",
    log_level="DEBUG",  # Available options: DEBUG, INFO, WARNING, ERROR, CRITICAL
    log_file="parser.log"  # Optional: Log messages will be saved to this file
)
```

### Example Log Output (DEBUG Level)

```text
2024-10-22 17:00:01 - DEBUG - Detected encoding for test/example_log_500_lines.log: utf-8
2024-10-22 17:00:01 - INFO - Processing file: test/example_log_500_lines.log
2024-10-22 17:00:02 - INFO - Finished parsing test/example_log_500_lines.log. Parsed 500 entries.
2024-10-22 17:00:02 - INFO - Saved 500 entries to table 'table_500_lines'.
```

---

## Updated CLI with Logging Configuration

The CLI now supports setting the logging level and logging to a file.

### CLI Arguments for Logging

- **`--log-level`**: Set the logging level (default: `INFO`).
- **`--log-file`**: Specify a file to log messages (optional).

### Example CLI Command

```bash
python parser_cli.py     --db-path logs.db     --files test/example_log_500_lines.log test/another_log.log     --regexes "(?P<timestamp>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) - (?P<level>\w+) - (?P<message>.*)"               "(?P<date>\d{2}/\d{2}/\d{4}) \| (?P<event>\w+) \| (?P<details>.*)"     --tables table_500_lines another_table     --columns "timestamp,level,message" "date,event,details"     --multiprocessing     --log-level DEBUG     --log-file parser.log
```
