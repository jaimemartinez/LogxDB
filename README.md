
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

