
# LogxDB: A Robust Log Parser with Multiprocessing and Encoding Detection

**LogxDB** is a high-performance log parser designed to handle multiple log files concurrently with **multiprocessing** and **auto-detect encoding** to ensure compatibility with diverse formats. It stores parsed data in **SQLite** databases with support for **custom regex patterns**, **table names**, and **column orders**.

## Project Structure

```
logxdb/
│
├── parser.py          # Main parser logic with multiprocessing and SQLite support
├── main.py            # Example script to use the parser
├── example_log_500_lines.log  # Example log file with timestamped entries
├── another_log.log    # Example log file with event-based entries
├── LICENSE            # License file (MIT License)
└── README.md          # Documentation for the project
```

---

## Features

1. **Multiprocessing**: Efficiently processes multiple log files in parallel using Python’s `multiprocessing`.
2. **Encoding Detection**: Detects file encoding automatically using `chardet`.
3. **Custom Table Names and Orders**: Save parsed logs to SQLite with configurable table names and column orders.
4. **Regex Parsing**: Flexible regex patterns to extract log data.
5. **Multi-line Log Support**: Handles log entries that span multiple lines.

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

## Usage

### Example Log Files

- [example_log_500_lines.log](./example_log_500_lines.log)
- [another_log.log](./another_log.log)

---

### Main Functionality: `parser.py`

`parser.py` contains the core logic, which:
- Detects file encoding.
- Uses regex to parse logs.
- Stores parsed data into SQLite tables.
- Supports parallel processing via multiprocessing.

---

### Example Script: `main.py`

`main.py` demonstrates how to use the parser:

```python
from parser import LogParser, LogParserError

# Define the regex patterns for each log format
regex_1 = r"(?P<timestamp>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) - (?P<level>\w+) - (?P<message>.*)"
regex_2 = r"(?P<date>\d{2}/\d{2}/\d{4}) \| (?P<event>\w+) \| (?P<details>.*)"

try:
    # Initialize the parser with the path to the SQLite database
    parser = LogParser(db_path="logs.db")

    # Define the files with their configurations
    files_with_configs = {
        "example_log_500_lines.log": ("table_500_lines", regex_1, ["timestamp", "level", "message"]),
        "another_log.log": ("another_table", regex_2, ["date", "event", "details"])
    }

    # Parse files with multiprocessing enabled
    parser.parse_multiple_files(files_with_configs, enable_multiprocessing=True)

    print("All files processed successfully.")

except LogParserError as e:
    print(f"An error occurred: {e}")
```

---

### Running the Project

1. Ensure all log files and scripts are in the same directory.
2. Run the parser using:

    ```bash
    python main.py
    ```

---

## Dependencies

- **Python 3.10+**
- **chardet**: For encoding detection. Install using:
  
    ```bash
    pip install chardet
    ```

- **sqlite3**: Comes pre-installed with Python.
- **multiprocessing**: Standard Python library for parallel processing.

---

## How It Works

1. **Encoding Detection**: `parser.py` uses `chardet` to detect the encoding of each file.
2. **Parallel Processing**: Log files are processed in parallel using multiple CPU cores.
3. **SQLite Database**: Parsed data is stored in custom tables based on your configuration.
4. **Multi-line Support**: If a log line doesn’t match the regex, it’s appended to the previous entry.

---

## Troubleshooting

- **sqlite3.Connection cannot be pickled**: Ensure each process opens its own SQLite connection to avoid pickling errors.

---

## License

This project is licensed under the MIT License. See the [LICENSE](./LICENSE) file for more details.

---

## Contributing

Contributions are welcome! Open an issue or submit a pull request for improvements.

---

## Contact

If you have any questions or suggestions, feel free to open an issue or contact the repository owner.
