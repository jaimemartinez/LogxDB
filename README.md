
# LogxDB: A Robust Log Parser with Multiprocessing and Encoding Detection

**LogxDB** is a high-performance log parser designed to handle multiple log files concurrently with **multiprocessing** and **auto-detect encoding** to ensure compatibility with diverse formats. It stores parsed data in **SQLite** databases with support for **custom regex patterns**, **table names**, and **column orders**.

---

## Project Structure

```
logxdb/
│
├── parser.py          # Main parser logic with multiprocessing and SQLite support
├── parser_cli.py      # Command-line interface for LogxDB with regex REPL and config support
├── test/              # Example scripts and log files for testing
│       ├── main.py    # Example script to use the parser
│       ├── example_log_500_lines.log  # Example log file with timestamped entries
│       ├── another_log.log            # Example log file with event-based entries
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
6. **YAML/JSON Configuration Support**: Manage log parsing rules in user-friendly YAML/JSON files.
7. **Interactive Regex Testing REPL**: Test regex patterns directly from the CLI.

---

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/your-username/logxdb.git
    cd logxdb
    ```

2. Install dependencies:

    ```bash
    pip install chardet pyyaml
    ```

---

## Documentation

### `parser.py`: Core Parser Logic

1. **Detecting Encoding of Log Files**:

   ```python
   encoding = parser.detect_encoding("test/example_log_500_lines.log")
   print(f"Detected encoding: {encoding}")
   ```

2. **Parsing a Single Log File**:

   ```python
   data = parser.parse_file("test/example_log_500_lines.log", regex_1)
   print(data)
   ```

3. **Storing Data in SQLite Database**:

   ```python
   data = [{"ip": "192.168.1.1", "timestamp": "22/Oct/2024:16:00:01", "status": "200"}]
   parser.save_to_db("logs", data, ["ip", "timestamp", "status"])
   ```

4. **Using YAML/JSON Configuration Files**:

   Example YAML configuration:
   ```yaml
   files:
     - file: web_server.log
       table: web_logs
       regex: (?P<ip>\d+\.\d+\.\d+\.\d+) - \[(?P<timestamp>.*)\] - (?P<status>.*)
       columns: [ip, timestamp, status]
   ```

---

### `parser_cli.py`: Command-Line Interface

1. **Using the CLI with YAML Configuration**:

   ```bash
   python parser_cli.py --config config.yaml --multiprocessing --log-level DEBUG --log-file parser.log
   ```

2. **Using Individual Parameters**:

   ```bash
   python parser_cli.py --db-path logs.db --files web_server.log app.log \
       --regexes "(?P<ip>\d+\.\d+\.\d+\.\d+) - \[(?P<timestamp>.*)\] - (?P<status>.*)" \
                 "(?P<timestamp>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) - (?P<level>\w+) - (?P<message>.*)" \
       --tables web_logs app_logs --columns ip,timestamp,status timestamp,level,message \
       --multiprocessing --log-level DEBUG --log-file parser_output.log
   ```

3. **Launching the Regex REPL**:

   ```bash
   python parser_cli.py --repl
   ```

---

## Example Logs and Expected Outputs

### Example Log Files

**`web_server.log`**:
```
192.168.1.1 - [22/Oct/2024:16:00:01] - 200
192.168.1.2 - [22/Oct/2024:16:01:12] - 404
192.168.1.3 - [22/Oct/2024:16:02:23] - 500
```

**`app.log`**:
```
2024-10-22 16:10:32 - INFO - Application started
2024-10-22 16:12:45 - ERROR - Application crashed
```

### Expected SQLite Output

**Table: web_logs**

| id | ip           | timestamp               | status |
|----|--------------|-------------------------|--------|
| 1  | 192.168.1.1  | 22/Oct/2024:16:00:01    | 200    |
| 2  | 192.168.1.2  | 22/Oct/2024:16:01:12    | 404    |
| 3  | 192.168.1.3  | 22/Oct/2024:16:02:23    | 500    |

**Table: app_logs**

| id | timestamp           | level | message               |
|----|---------------------|-------|-----------------------|
| 1  | 2024-10-22 16:10:32 | INFO  | Application started   |
| 2  | 2024-10-22 16:12:45 | ERROR | Application crashed   |

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

- **PyYAML**: Install using:

    ```bash
    pip install pyyaml
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
