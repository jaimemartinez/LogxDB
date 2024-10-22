
# LogxDB: A Powerful Log Parser with Multiprocessing and Encoding Detection

**LogxDB** is a robust log parser that can handle multiple log files in parallel using **multiprocessing**. It also supports **auto-detection of file encoding** to ensure compatibility with various log formats. Parsed data is saved to an **SQLite database** with custom table names and column orders for each log file.

## Features

- **Multiprocessing** for parallel log file processing.
- **Auto-detection of encoding** using `chardet`.
- **Custom regex patterns, table names, and column orders** for each log file.
- **Support for multi-line log entries**.
- **SQLite database integration** for storing parsed data.

---

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/your-username/logxdb.git
    cd logxdb
    ```

2. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

---

## Usage

### Example Log Files

You can download example log files here:
- [example_log_500_lines.log](./example_log_500_lines.log)
- [another_log.log](./another_log.log)

Place these files in the project directory or modify the paths accordingly in `main.py`.

---

### Running the Parser

1. Create a Python script `main.py` with the following content:

    ```python
    from parser import LogParser, LogParserError

    # Define the regex patterns for each log format
    regex_1 = r"(?P<timestamp>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) - (?P<level>\w+) - (?P<message>.*)"
    regex_2 = r"(?P<date>\d{2}/\d{2}/\d{4}) \| (?P<event>\w+) \| (?P<details>.*)"

    try:
        # Initialize the parser with the path to the SQLite database
        parser = LogParser(db_path="logs.db")

        # Define the files with their corresponding configurations
        files_with_configs = {
            "example_log_500_lines.log": ("table_500_lines", regex_1, ["timestamp", "level", "message"]),
            "another_log.log": ("another_table", regex_2, ["date", "event", "details"])
        }

        # Parse the files with multiprocessing enabled
        parser.parse_multiple_files(files_with_configs, enable_multiprocessing=True)

        print("All files processed successfully.")

    except LogParserError as e:
        print(f"An error occurred: {e}")
    ```

2. Run the parser:

    ```bash
    python main.py
    ```

---

## Dependencies

- Python 3.10+
- `chardet` (for encoding detection)
- `sqlite3` (comes pre-installed with Python)
- `multiprocessing` (standard Python library)

Install dependencies using:

```bash
pip install chardet
```

---

## Project Structure

```
logxdb/
│
├── parser.py          # Main parser logic with multiprocessing and SQLite support
├── main.py            # Example script to use the parser
├── example_log_500_lines.log  # Example log file with timestamped entries
├── another_log.log    # Example log file with event-based entries
├── requirements.txt   # List of Python dependencies
└── README.md          # Documentation for the project
```

---

## How It Works

1. **Encoding Detection**: Each file's encoding is detected using `chardet`.
2. **Parallel Processing**: Files are processed in parallel using Python's `multiprocessing`.
3. **Custom Table Structures**: Each file is stored in a unique SQLite table with a configurable column order.
4. **Multi-line Support**: Continuation lines are appended to the previous entry if they don't match the regex.

---

## Troubleshooting

- **Error: `sqlite3.Connection` cannot be pickled**  
  Ensure that each process creates its **own SQLite connection**. This issue is resolved by using separate connections for each process.

---

## License

This project is licensed under the MIT License.

---

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bugs you find.

---

## Contact

If you have any questions or issues, feel free to open an issue in this repository or contact me directly.
