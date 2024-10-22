
# LogxDB: A Robust Log Parser with CLI and Interactive Regex Testing

**LogxDB** is a high-performance log parser designed to handle multiple log files concurrently with **multiprocessing** and **auto-detect encoding** to ensure compatibility with diverse formats. It stores parsed data in **SQLite** databases with support for **custom regex patterns**, **table names**, and **column orders**.

---

## Project Structure

```
logxdb/
│
├── parser.py          # Main parser logic with multiprocessing and SQLite support
├── parser_cli.py      # CLI for running the parser and interactive regex testing
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
4. **CLI Interface**: Use the parser directly from the command line.
5. **Interactive Regex Testing REPL**: Test regex patterns interactively.
6. **Multi-line Log Entry Support**: Handles logs that span multiple lines.

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

## CLI Usage Guide

### 1. Running the Parser from the CLI

```bash
python parser_cli.py     --db-path logs.db     --files test/example_log_500_lines.log test/another_log.log     --regexes "(?P<timestamp>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) - (?P<level>\w+) - (?P<message>.*)"               "(?P<date>\d{2}/\d{2}/\d{4}) \| (?P<event>\w+) \| (?P<details>.*)"     --tables table_500_lines another_table     --columns "timestamp,level,message" "date,event,details"     --multiprocessing
```

---

### 2. Launching the Interactive Regex Testing REPL

```bash
python parser_cli.py --repl
```

#### Example REPL Interaction:
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

---

## Example Usage: `main.py`

Navigate to the `test/` directory and run the example script:

```bash
python test/main.py
```

---

## Troubleshooting

- **sqlite3.Connection cannot be pickled**: Ensure each process opens its own SQLite connection to avoid pickling errors.

---

## Dependencies

- **Python 3.10+**
- **chardet**: Install using:

    ```bash
    pip install chardet
    ```

---

## License

This project is licensed under the MIT License. See the [LICENSE](./LICENSE) file for more details.

---

## Contributing

Contributions are welcome! Open an issue or submit a pull request for improvements.

---

## Contact

If you have any questions or suggestions, feel free to open an issue or contact the repository owner.
