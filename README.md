
# LogxDB: A Robust Log Parser with Multiprocessing and Encoding Detection

**LogxDB** is a high-performance log parser designed to handle multiple log files concurrently with **multiprocessing** and **auto-detect encoding** to ensure compatibility with diverse formats. It stores parsed data in **SQLite** databases with support for **custom regex patterns**, **table names**, and **column orders**.

---

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
encoding = parser.detect_encoding("example_log_500_lines.log")
print(f"Detected encoding: {encoding}")
```

This ensures that files with different encodings are processed correctly.

---

### 2. Parsing a Single Log File

You can parse a single log file with a specific regex pattern:

```python
data = parser.parse_file("example_log_500_lines.log", regex_1)
print(data)
```

This function reads the file, applies the regex pattern, and returns a list of parsed entries.

---

### 3. Storing Data in SQLite Database

The `save_to_db` function stores the parsed log data into a SQLite table with custom column orders:

```python
parser.save_to_db("log_table", data, ["timestamp", "level", "message"])
```

---

### 4. Handling Multiple Files with Custom Configurations

You can define multiple files with their own table names, regex patterns, and column orders:

```python
files_with_configs = {
    "example_log_500_lines.log": ("table_500_lines", regex_1, ["timestamp", "level", "message"]),
    "another_log.log": ("another_table", regex_2, ["date", "event", "details"])
}
```

---

### 5. Enabling Multiprocessing for Faster Processing

To speed up parsing, use the `parse_multiple_files` function with multiprocessing enabled:

```python
parser.parse_multiple_files(files_with_configs, enable_multiprocessing=True)
```

This processes files in parallel using all available CPU cores.

---

## Running the Project

1. Ensure all files are in the same directory.
2. Run the project using the following command:

    ```bash
    python main.py
    ```

---

## Troubleshooting

- **`sqlite3.Connection` cannot be pickled**: Ensure each process creates its own SQLite connection to avoid pickling errors.

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

## License

This project is licensed under the MIT License. See the [LICENSE](./LICENSE) file for more details.

---

## Contributing

Contributions are welcome! Open an issue or submit a pull request for improvements.

---

## Contact

If you have any questions or suggestions, feel free to open an issue or contact the repository owner.
