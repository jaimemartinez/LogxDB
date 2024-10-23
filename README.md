
# LogxDB: Log Parser with CLI and Regex REPL

This project provides a **log parsing tool** that processes log files using regular expressions and saves the data into an SQLite database. It offers both a **command-line interface (CLI)** and a **Python API** with support for **YAML/JSON configuration files**, **multiprocessing**, and **regex testing in a REPL environment**.

## Project Structure

```
logxdb/
│
├── parser.py          # Main parser logic with multiprocessing and SQLite support
├── parser_cli.py      # Command-line interface for LogxDB with regex REPL and config support
├── test/
│       ├── main.py            # Example script to use the parser
│       ├── example_log_500_lines.log  # Example log file with timestamped entries
│       ├── another_log.log            # Example log file with event-based entries
│       ├── another_log.log    # Example log file with event-based entries
├── LICENSE            # License file (MIT License)
└── README.md          # Documentation for the project
```

---

## Table of Contents
1. [parser.py Documentation](#parserpy-documentation)
2. [parser_cli.py Documentation](#parser_clipy-documentation)
3. [Examples](#examples)
4. [License](#license)
5. [Contributing](#contributing)
6. [Contact](#contact)

---

## parser.py Documentation

`parser.py` provides the **core functionality** for parsing logs, storing data in SQLite, and supporting YAML/JSON configuration files. It includes support for:

- **Detecting encoding** of log files automatically.
- **Regex-based parsing** with support for multi-line entries.
- **YAML/JSON configuration** for flexible parsing.
- **Multiprocessing support** for faster log processing.
- **Error handling** with detailed logging.

### Key Functions

1. **`parse_file(file_path, regex)`**  
   - Parses a log file line by line, appending unmatched lines to the last match.
   - **Example log:**
     ```
     192.168.1.1 - [22/Oct/2024:16:00:01] - 200
     192.168.1.2 - [22/Oct/2024:16:01:12] - 404
     192.168.1.3 - [22/Oct/2024:16:02:23] - 500
     DKKSLLS
     akakkakkaka
     192.168.1.5 - [22/Oct/2024:16:02:24] - 500
     ```
   - **Expected Table Output (web_logs):**

     | id | ip           | timestamp               | status                 |
     |----|--------------|-------------------------|------------------------|
     | 1  | 192.168.1.1  | 22/Oct/2024:16:00:01    | 200                    |
     | 2  | 192.168.1.2  | 22/Oct/2024:16:01:12    | 404                    |
     | 3  | 192.168.1.3  | 22/Oct/2024:16:02:23    | 500
DKKSLLS
akakkakkaka |
     | 4  | 192.168.1.5  | 22/Oct/2024:16:02:24    | 500                    |

2. **`create_table(conn, table_name, columns)`**  
   - Creates an SQLite table if it doesn’t exist.

3. **`save_to_db(table_name, data, column_order)`**  
   - Saves parsed log entries to the specified SQLite table.

---

## parser_cli.py Documentation

`parser_cli.py` offers a **command-line interface** for parsing logs and includes:

- **Interactive Regex REPL**: Test regex patterns and strings.
- **YAML/JSON Configuration Support**: Use config files to simplify parsing.
- **Multiprocessing Support**: Enable faster processing with the `--multiprocessing` flag.

### CLI Usage

1. **With YAML Configuration File**
   ```bash
   python parser_cli.py --config config.yaml --multiprocessing --log-level DEBUG --log-file parser_output.log
   ```

2. **With Individual Parameters**
   ```bash
   python parser_cli.py --db-path logs.db        --files web_server.log app.log        --regexes "(?P<ip>\d+\.\d+\.\d+\.\d+) - \[(?P<timestamp>\d+\/\w+\/\d+:\d+:\d+:\d+)\] - (?P<status>.*)"                  "(?P<timestamp>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) - (?P<level>\w+) - (?P<message>.*)"        --tables web_logs app_logs        --columns ip,timestamp,status timestamp,level,message        --log-level INFO --multiprocessing
   ```

3. **Launching the Regex REPL**
   ```bash
   python parser_cli.py --repl
   ```

---

## Examples

### Example YAML Configuration (`config.yaml`)

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

### Example JSON Configuration (`config.json`)

```json
{
  "files": [
    {
      "file": "web_server.log",
      "table": "web_logs",
      "regex": "(?P<ip>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}) - \[(?P<timestamp>\d{2}\/\w+\/\d+:\d+:\d+:\d+)\] - (?P<status>.*)",
      "columns": ["ip", "timestamp", "status"]
    },
    {
      "file": "app.log",
      "table": "app_logs",
      "regex": "(?P<timestamp>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) - (?P<level>\w+) - (?P<message>.*)",
      "columns": ["timestamp", "level", "message"]
    }
  ]
}
```

---

## License

This project is licensed under the MIT License. See the LICENSE file for details.

---

## Contributing

Contributions are welcome! Please submit a pull request or open an issue to discuss changes.

---

## Contact

For any inquiries or issues, please contact the project maintainers at:

