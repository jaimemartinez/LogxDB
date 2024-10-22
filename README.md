# LogxDB: A Robust Log Parser with Multiprocessing and Encoding Detection

**LogxDB** is a high-performance log parser designed to handle multiple log files concurrently with **multiprocessing** and **auto-detect encoding** to ensure compatibility with diverse formats. It stores parsed data in **SQLite** databases with support for **custom regex patterns**, **table names**, and **column orders**.

---

## Project Structure

```
logxdb/
│
├── parser.py          # Main parser logic with multiprocessing and SQLite support
├── test/
│       ├── main.py            # Example script to use the parser
│       ├── example_log_500_lines.log  # Example log file with timestamped entries
│       ├── another_log.log    # Example log file with event-based entries
├── LICENSE            # License file (MIT License)
└── README.md          # Documentation for the project
```

---

## Features

1. **Multiprocessing**: Efficiently process multiple log files in parallel.
2. **Encoding Detection**: Detects the encoding of each log file automatically.
3. **Custom Table Names and Column Orders**: Save logs to SQLite with custom table names and column configurations.
4. **Regex Parsing**: Use flexible regex patterns to extract log data.
5. **Multi-line Log Entry Support**: Handles logs that span multiple lines.

---

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/your-username/logxdb.git
    cd logxdb
    ```

2. Install dependencies:

    ```bash
    pip install chardet
    ```

---

## Usage Guide for Each Functionality

### 1. Detecting Encoding of Log Files

LogxDB uses `chardet` to detect the encoding of each file:

```python
encoding = parser.detect_encoding("test/example_log_500_lines.log")
print(f"Detected encoding: {encoding}")
```

---

### 2. Parsing a Single Log File

```python
data = parser.parse_file("test/example_log_500_lines.log", regex_1)
print(data)
```

---

### 3. Storing Data in SQLite Database

```python
parser.save_to_db("log_table", data, ["timestamp", "level", "message"])
```

---

### 4. Handling Multiple Files with Custom Configurations

```python
files_with_configs = {
    "test/example_log_500_lines.log": ("table_500_lines", regex_1, ["timestamp", "level", "message"]),
    "test/another_log.log": ("another_table", regex_2, ["date", "event", "details"])
}
```

---

### 5. Enabling Multiprocessing for Faster Processing

```python
parser.parse_multiple_files(files_with_configs, enable_multiprocessing=True)
```

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
## CLI Documentation

The `parser_cli.py` script provides a powerful command-line interface (CLI) for running the LogxDB parser and testing regex patterns interactively.

### Available Commands and Arguments

1. **Launching the Interactive Regex Testing REPL:**

   Use the `--repl` option to enter an interactive session where you can test regex patterns against input strings:

   ```bash
   python parser_cli.py --repl
   ```

   **Example Interaction:**

   ```
   Welcome to the Regex Tester REPL! Type 'exit' to quit.
   Enter regex pattern: (?P<timestamp>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) - (?P<level>\w+) - (?P<message>.*)
   Enter test string: 2024-10-22 16:19:43 - INFO - Parsing completed successfully.
   Match found:
   {
       "timestamp": "2024-10-22 16:19:43",
       "level": "INFO",
       "message": "Parsing completed successfully."
   }
   Enter regex pattern: exit
   ```

2. **Running the Log Parser with File Configurations:**

   The following options are required when running the parser:

   - **`--db-path`**: Path to the SQLite database file.
   - **`--files`**: One or more log files to parse.
   - **`--regexes`**: Regex patterns for each log file.
   - **`--tables`**: Table names corresponding to each log file.
   - **`--columns`**: Comma-separated column names for each table.
   - **`--multiprocessing`**: (Optional) Enable multiprocessing for faster parsing.

   **Example Command:**

   ```bash
   python parser_cli.py        --db-path logs.db        --files test/example_log_500_lines.log test/another_log.log        --regexes "(?P<timestamp>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) - (?P<level>\w+) - (?P<message>.*)"                  "(?P<date>\d{2}/\d{2}/\d{4}) \| (?P<event>\w+) \| (?P<details>.*)"        --tables table_500_lines another_table        --columns "timestamp,level,message" "date,event,details"        --multiprocessing
   ```

3. **Error Handling:**

   If any required arguments are missing, the script will raise an error. Use `--help` to view all available options:

   ```bash
   python parser_cli.py --help
   ```

   **Sample Output:**

   ```
   usage: parser_cli.py [-h] --db-path DB_PATH --files FILES [FILES ...] --regexes
                        REGEXES [REGEXES ...] --tables TABLES [TABLES ...] --columns
                        COLUMNS [COLUMNS ...] [--multiprocessing] [--repl]

   LogxDB: Log Parser with CLI and Regex REPL

   optional arguments:
     -h, --help            Show this help message and exit
     --db-path DB_PATH     Path to the SQLite database
     --files FILES [FILES ...]
                           List of log files to parse
     --regexes REGEXES [REGEXES ...]
                           List of regex patterns for each file
     --tables TABLES [TABLES ...]
                           Table names for each log file
     --columns COLUMNS [COLUMNS ...]
                           Comma-separated column names for each table
     --multiprocessing     Enable multiprocessing
     --repl                Launch interactive regex testing REPL
   ```

---

This CLI provides a flexible way to use the LogxDB parser and test regex patterns directly from the command line.

## Updated CLI with Logging Configuration

The CLI now supports setting the logging level and logging to a file.

### CLI Arguments for Logging

- **`--log-level`**: Set the logging level (default: `INFO`).
- **`--log-file`**: Specify a file to log messages (optional).

### Example CLI Command

```bash
python parser_cli.py     --db-path logs.db     --files test/example_log_500_lines.log test/another_log.log     --regexes "(?P<timestamp>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) - (?P<level>\w+) - (?P<message>.*)"               "(?P<date>\d{2}/\d{2}/\d{4}) \| (?P<event>\w+) \| (?P<details>.*)"     --tables table_500_lines another_table     --columns "timestamp,level,message" "date,event,details"     --multiprocessing     --log-level DEBUG     --log-file parser.log
```

---
## Running the Example

Navigate to the `test/` directory and run:

```bash
python main.py
```

---

## Troubleshooting

- **`sqlite3.Connection` cannot be pickled**: Ensure each process opens its own SQLite connection.

---

## Dependencies

- **Python 3.10+**
- **chardet**: Install using:
  
    ```bash
    pip install chardet
    ```

- **sqlite3**: Comes pre-installed with Python.

---

## License

This project is licensed under the MIT License. See the [LICENSE](./LICENSE) file for more details.

---

## Contributing

Contributions are welcome! Open an issue or submit a pull request for improvements.

---

## Contact

If you have any questions or suggestions, feel free to open an issue or contact the repository owner.

---

## New Features and Usage

This version of the Log Parser CLI introduces the following new features:

### 1. YAML and JSON Configuration Support
You can now use **YAML** or **JSON** configuration files to simplify log parsing setup.

Example YAML (`config.yaml`):
```yaml
files:
  - file: web_server.log
    table: web_logs
    regex: (?P<ip>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}) - \[(?P<timestamp>\d{2}\/[A-Za-z]{3}\/\d{4}:\d{2}:\d{2}:\d{2})\] - (?P<status>.*)
    columns:
      - ip
      - timestamp
      - status
  - file: app.log
    table: app_logs
    regex: (?P<timestamp>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) - (?P<level>\w+) - (?P<message>.*)
    columns:
      - timestamp
      - level
      - message
```

### 2. Command-line Usage with Config Files

You can specify the config file directly in the CLI:

```bash
python parser_cli.py --config config.yaml --multiprocessing --log-level DEBUG --log-file parser_output.log
```

### 3. Interactive Regex Tester (REPL)

Test your regex patterns interactively using the REPL mode:

```bash
python parser_cli.py --repl
```

Example:
```
Enter regex pattern: (?P<ip>\d+\.\d+\.\d+\.\d+) - \[(?P<timestamp>\d+\/\w+\/\d+:\d+:\d+:\d+)\] - (?P<status>.*)
Enter test string: 192.168.1.1 - [22/Oct/2024:16:00:01] - 200
Match found:
{
    "ip": "192.168.1.1",
    "timestamp": "22/Oct/2024:16:00:01",
    "status": "200"
}
```

### 4. Multiprocessing Support
Enable multiprocessing for faster log parsing with the `--multiprocessing` flag.

### 5. Example SQLite Database Output

**web_logs Table:**
| id | ip           | timestamp               | status |
|----|--------------|-------------------------|--------|
| 1  | 192.168.1.1  | 22/Oct/2024:16:00:01    | 200    |
| 2  | 192.168.1.2  | 22/Oct/2024:16:01:12    | 404    |
| 3  | 192.168.1.3  | 22/Oct/2024:16:02:23    | 500    |

**app_logs Table:**
| id | timestamp           | level | message               |
|----|---------------------|-------|-----------------------|
| 1  | 2024-10-22 16:10:32 | INFO  | Application started   |
| 2  | 2024-10-22 16:12:45 | ERROR | Application crashed   |

### 6. Complete CLI Command Example
```bash
python parser_cli.py     --db-path logs.db     --files web_server.log app.log     --regexes "(?P<ip>\d+\.\d+\.\d+\.\d+) - \[(?P<timestamp>\d+\/\w+\/\d+:\d+:\d+:\d+)\] - (?P<status>.*)"               "(?P<timestamp>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) - (?P<level>\w+) - (?P<message>.*)"     --tables web_logs app_logs     --columns ip,timestamp,status timestamp,level,message     --log-level DEBUG --log-file parser.log --multiprocessing
```

### 7. Error Handling and Logging
- Critical and unexpected errors are logged with `CRITICAL` severity.
- Errors in file parsing or configuration are logged and reported gracefully.

