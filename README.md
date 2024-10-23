
# LogxDB: Simple Log Parsing Library for Everyone  

**LogxDB** is a high-performance log parser designed to handle multiple log files concurrently with multiprocessing and auto-detect encoding to ensure compatibility with diverse formats. It stores parsed data in SQLite databases with support for custom regex patterns, table names, and column orders.

---

## Project Structure

```
logxdb/
│
├── parser.py              # Core logic: parsing logs, handling SQLite, multiprocessing
├── parser_cli.py          # Command-line tool with regex REPL and configuration support
├── test/
│   ├── main.py                   # Example script to test and use the parser
│   ├── example_log_500_lines.log # Example log file with timestamped entries
│   ├── another_log.log           # Example log file with event-based entries
├── LICENSE               # License file (MIT License)
└── README.md             # Documentation and usage guide for the project
```

---
### **Summary of Functionalities:**

1. [1. Logging Configuration] (#Logging Configuration): Logs operations with different verbosity levels.
2. **Encoding Detection**: Detects encoding using `chardet`.
3. **Regex Matching**: Identifies the appropriate regex for a log file.
4. **Log Preprocessing**: Handles unmatched lines by appending them to the previous valid entry.
5. **Multiple Match Handling**: Processes multiple regex matches within the same line.
6. **SQLite Database Creation**: Creates tables dynamically if they don't exist.
7. **Data Insertion**: Saves parsed data to the SQLite database.
8. **Single File Processing**: Handles the entire process for a single log file.
9. **Configuration File Loading**: Loads YAML/JSON configuration files.
10. **Config-Based Parsing**: Uses configuration files for batch processing.
11. **Multiprocessing**: Accelerates processing using multiple cores.

---

### **1. Logging Configuration**
- **Description**: Configures logging to print to console and/or log files at different levels (DEBUG, INFO, WARNING, etc.).

**Code Location**:
```python
def configure_logging(self, log_level, log_file):
    numeric_level = getattr(logging, log_level.upper(), logging.INFO)
    handlers = [logging.StreamHandler()]
    if log_file:
        handlers.append(logging.FileHandler(log_file))
    logging.basicConfig(
        level=numeric_level,
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        handlers=handlers
    )
```


#### **How to Use**:
```python
from parser import LogParser

# Initialize the parser with a log file and DEBUG level logging
parser = LogParser(db_path='logs.db', log_level='DEBUG', log_file='parser.log')

# This will configure logging to write to 'parser.log'
```


---

### **2. Detect File Encoding**
- **Description**: Detects the encoding of a given log file using **chardet** and provides a fallback if detection confidence is low.

**Code Location**:
```python
def detect_encoding(self, file_path):
    try:
        with open(file_path, 'rb') as f:
            raw_data = f.read(4096)
            result = chardet.detect(raw_data)
            encoding = result.get('encoding', 'utf-8')
            confidence = result.get('confidence', 0)
            logging.info(f"Detected encoding for {file_path}: {encoding} (Confidence: {confidence:.2f})")
            if confidence < 0.7:
                encoding = 'utf-8-sig'
                logging.warning(f"Low confidence in encoding detection. Defaulting to 'utf-8-sig'.")
            return encoding
    except Exception as e:
        logging.error(f"Failed to detect encoding for {file_path}: {e}")
        return 'utf-8'
```

#### **How to Use**:
```python
encoding = parser.detect_encoding('example.log')
print(f"Detected encoding: {encoding}")
```

#### **Expected Output**:
```
Detected encoding: utf-8-sig
```

---

### **3. Find Matching Regex for File**
- **Description**: Iterates through the provided regex patterns to find the first matching one for a log file.

**Code Location**:
```python
def find_matching_regex(self, file_path, regexes):
    encoding = self.detect_encoding(file_path)
    with open(file_path, encoding=encoding, errors='replace') as f:
        for line in f:
            for regex in regexes:
                if re.search(regex, line):
                    logging.info(f"Using regex: {regex} for file {file_path}")
                    return regex
    logging.error(f"No matching regex found for {file_path}.")
    raise LogParserError(f"No matching regex found for {file_path}.")
```



#### **How to Use**:
```python
regexes = [
    r"\d{2}\/\d{2}\/\d{4}",  # Example regex pattern
    r"\w+\s-\s\d+"           # Another example pattern
]

# Attempt to find a matching regex
matching_regex = parser.find_matching_regex('example.log', regexes)
print(f"Matching regex: {matching_regex}")
```

---

### **4. Preprocess Log Lines**
- **Description**: Prepares log lines by appending unmatched lines to the previous valid entry to maintain structure.

**Code Location**:
```python
def preprocess_log(self, file_path, regex):
    processed_lines = []
    encoding = self.detect_encoding(file_path)
    current_line = ""
    with open(file_path, encoding=encoding, errors='replace') as f:
        for line in f:
            cleaned_line = line.strip()
            if re.match(regex, cleaned_line):
                if current_line:
                    processed_lines.append(current_line)
                    logging.debug(f"Processed line: {current_line}")
                current_line = cleaned_line
            else:
                current_line += "[new-line]" + cleaned_line
                logging.debug(f"Appended unmatched line: {cleaned_line}")
        if current_line:
            processed_lines.append(current_line)
            logging.debug(f"Added final processed line: {current_line}")
    logging.info(f"Preprocessed {len(processed_lines)} lines from '{file_path}'.")
    return processed_lines
```


#### **How to Use**:
```python
preprocessed_lines = parser.preprocess_log('example.log', r"(\w+)\s-\s(\d+)")
print(preprocessed_lines)
```

#### **Expected Output**:
```
['Line 1 - 123', 'Continuation of Line 1[new-line]Line 2 - 456']
```


---

### **5. Parse Lines with Multiple Matches**
- **Description**: Uses `re.finditer()` to extract all non-overlapping matches in a line and parse them as separate entries.

**Code Location**:
```python
def parse_lines(self, lines, regex):
    parsed_entries = []
    for line in lines:
        logging.debug(f"Processing line: {line}")
        matches = list(re.finditer(regex, line))
        if matches:
            logging.debug(f"Found {len(matches)} matches in line.")
            for match in matches:
                entry = match.groupdict()
                entry = {k: v.replace("[new-line]", "\n") if isinstance(v, str) else v for k, v in entry.items()}
                logging.debug(f"Parsed entry: {entry}")
                parsed_entries.append(entry)
        else:
            logging.warning(f"No matches found for line: {line}")
    logging.info(f"Parsed {len(parsed_entries)} entries.")
    return parsed_entries
```

#### **How to Use**:
```python
lines = [
    "(P3308-T5876)Info ( 247): Event 1.[new-line](P3308-T5876)Debug( 259): Event 2"
]
regex = r"(?P<process>P\d+-T\d+)\s(?P<severity>\w+)\s\(\s*\d+\):\s(?P<log>.*?)(?=(\(P\d+-T\d+\)|$))"

parsed_entries = parser.parse_lines(lines, regex)
print(parsed_entries)
```

#### **Expected Output**:
```
[
    {'process': 'P3308-T5876', 'severity': 'Info', 'log': 'Event 1.'},
    {'process': 'P3308-T5876', 'severity': 'Debug', 'log': 'Event 2'}
]
```

---

### **6. Create SQLite Database Table**
- **Description**: Creates a table in the SQLite database if it does not already exist.

**Code Location**:
```python
def create_table(self, conn, table_name, columns):
    columns_definition = ", ".join([f"{col} TEXT" for col in columns])
    query = f"CREATE TABLE IF NOT EXISTS {table_name} (id INTEGER PRIMARY KEY AUTOINCREMENT, {columns_definition});"
    conn.execute(query)
    logging.debug(f"Created table '{table_name}' with columns {columns}")
```

#### **How to Use**:
```python
conn = sqlite3.connect('logs.db')
columns = ['process', 'severity', 'log']
parser.create_table(conn, 'log_table', columns)
```
#### **Expected Output**:

The **SQLite table structure** after calling the `create_table` function:

**Table Name:** `log_table`

| **Column**   | **Type** |
|--------------|-----------|
| id           | INTEGER (Primary Key) |
| process      | TEXT      |
| severity     | TEXT      |
| log          | TEXT      |



---

### **7. Save Parsed Data to Database**
- **Description**: Inserts parsed log entries into the SQLite database.

**Code Location**:
```python
def save_to_db(self, table_name, data, column_order):
    conn = sqlite3.connect(self.db_path)
    try:
        self.create_table(conn, table_name, column_order)
        placeholders = ", ".join(["?"] * len(column_order))
        query = f"INSERT INTO {table_name} ({', '.join(column_order)}) VALUES ({placeholders})"
        for entry in data:
            values = [entry.get(col) for col in column_order]
            conn.execute(query, values)
            logging.debug(f"Inserted entry into table '{table_name}': {entry}")
        conn.commit()
        logging.info(f"Saved {len(data)} entries to table '{table_name}'.")
    except sqlite3.Error as e:
        logging.error(f"SQLite error: {e}")
        raise
    finally:
        conn.close()
```

#### **How to Use**:
```python
data = [
    {'process': 'P3308-T5876', 'severity': 'Info', 'log': 'Event 1'},
    {'process': 'P3308-T5876', 'severity': 'Debug', 'log': 'Event 2'}
]

parser.save_to_db('log_table', data, ['process', 'severity', 'log'])
```
#### **Expected Output**:

The **SQLite table** after calling the `save_to_db` function:

| **ID** | **Process**    | **Severity** | **Log**                                            |
|--------|----------------|--------------|----------------------------------------------------|
| 1      | P3308-T5876    | Info         | Event 1                                            |
| 2      | P3308-T5876    | Debug        | Event 2                                            |
---

### **8. Process a Single File**
- **Description**: Processes one log file according to its configuration, including regex matching and database insertion.

**Code Location**:
```python
def process_file(self, config):
    try:
        file_path, (table_name, regexes, column_order, stop_on_first_match) = config
        if not os.path.isfile(file_path):
            logging.error(f"File not found: {file_path}")
            return
        regex = self.find_matching_regex(file_path, regexes)
        processed_lines = self.preprocess_log(file_path, regex)
        parsed_data = self.parse_lines(processed_lines, regex)
        self.save_to_db(table_name, parsed_data, column_order)
    except Exception as e:
        logging.error(f"Error processing file '{file_path}': {e}")
```
#### **How to Use**:
```python
config = ('example.log', ('log_table', [r"\w+\s-\s\d+"], ['process', 'severity', 'log'], True))
parser.process_file(config)
```

---

### **9. Load Configuration File**
- **Description**: Loads configuration settings from a YAML or JSON file.

**Code Location**:
```python
def load_config(self, config_file):
    config_path = Path(config_file)
    if not config_path.exists():
        raise LogParserError(f"Config file not found: {config_file}")
    with open(config_file, 'r') as f:
        if config_file.endswith(('.yaml', '.yml')):
            return yaml.safe_load(f)
        elif config_file.endswith('.json'):
            return json.load(f)
        else:
            raise LogParserError("Unsupported config format.")
```

#### **How to Use**:
```yaml
# config.yaml
files:
  - file: example.log
    table: log_table
    regexes:
      - "(P\\d+-T\\d+)\\s(\\w+)\\s\\(\\s*\\d+\\):\\s(.*)"
    columns:
      - process
      - severity
      - log
    stop_on_first_match: true
```

```python
config = parser.load_config('config.yaml')
print(config)
```

---

### **10. Parse Files Using Configuration File**
- **Description**: Uses the configuration file to parse multiple log files with optional multiprocessing support.

**Code Location**:
```python
def parse_with_config_file(self, config_file, enable_multiprocessing=False):
    config = self.load_config(config_file)
    files_with_configs = {
        entry['file']: (entry['table'], entry['regexes'], entry['columns'], entry.get('stop_on_first_match', True))
        for entry in config['files']
    }
    self.parse_multiple_files(files_with_configs, enable_multiprocessing)
```
#### **How to Use**:
```python
parser.parse_with_config_file('config.yaml')
```


---

### **11. Multiprocessing Support for Parsing Files**
- **Description**: Enables faster processing by using multiple CPU cores.

**Code Location**:
```python
def parse_multiple_files(self, files_with_configs, enable_multiprocessing=False):
    if enable_multiprocessing:
        with Pool(processes=cpu_count()) as pool:
            pool.map(self.process_file, files_with_configs.items())
    else:
        for config in files_with_configs.items():
            self.process_file(config)
```

#### **How to Use**:
```python
parser.parse_with_config_file('config.yaml', enable_multiprocessing=True)
```

---


### **Complete Example**

#### **config.yaml**:
```yaml
files:
  - file: example.log
    table: log_table
    regexes:
      - "(P\\d+-T\\d+)\\s(\\w+)\\s\\(\\s*\\d+\\):\\s(.*)"
    columns:
      - process
      - severity
      - log
    stop_on_first_match: true
```

#### **main.py**:
```python
from parser import LogParser

# Initialize the parser
parser = LogParser(db_path='logs.db', log_level='DEBUG')

# Use config file for parsing
parser.parse_with_config_file('config.yaml')
```

#### **Expected Output**:
1. Log messages printed in the console/log file.
2. Entries saved to the SQLite database.


---
## Documentation for `parser_cli.py`

`parser_cli.py` is the command-line interface (CLI) for `LogxDB`, a log file parsing utility. This script allows users to process multiple log files, apply custom regular expressions (regexes), store parsed data in a SQLite database, and configure the parsing process via command-line arguments or configuration files (YAML/JSON).

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
  - [1. Run Regex REPL](#1-run-regex-repl)
  - [2. Parse Logs with Config Files](#2-parse-logs-with-config-files)
  - [3. Parse Logs with CLI Arguments](#3-parse-logs-with-cli-arguments)
  - [4. Logging and Error Handling](#4-logging-and-error-handling)
  - [5. Multiprocessing Support](#5-multiprocessing-support)
- [Code Examples](#code-examples)
- [Commands Summary](#commands-summary)

---

## **Overview**

`parser_cli.py` provides a flexible interface for parsing log files through the command line. It supports reading custom regular expressions from YAML/JSON configuration files or directly via command-line arguments. Additionally, it offers features like multiprocessing for faster log processing, logging to files, and an interactive regex testing mode.

---

## **Features**

- **Interactive Regex REPL**: Test and evaluate regex patterns interactively.
- **Configuration File Support**: Use YAML or JSON files to define log files, regexes, and table structure.
- **Command-Line Parsing**: Pass log files, regex patterns, and database details directly via CLI.
- **Multiprocessing Support**: Enable or disable multiprocessing to process logs faster using multiple CPU cores.
- **Logging**: Customizable logging with multiple levels (DEBUG, INFO, WARNING, ERROR, CRITICAL) and file logging support.
- **Error Handling**: Handles unexpected errors, missing files, and invalid configurations with meaningful messages.

---

## **Installation**

Ensure you have Python 3.6+ installed on your machine. Install the required dependencies:

```bash
pip install -r requirements.txt
```

The required libraries include:
- `argparse` for command-line argument parsing
- `re` for regular expressions
- `yaml` for YAML file handling
- `json` for JSON file handling
- `sqlite3` for database interaction
- `logging` for error tracking and debugging

---

## **Usage**

`parser_cli.py` can be used in several ways depending on the requirements. Below are usage examples for common scenarios.

### **1. Run Regex REPL**

The Regex REPL allows you to interactively test regex patterns and evaluate their output on test strings.

#### **Command:**
```bash
python parser_cli.py --repl
```

#### **Example Interaction:**
```
Welcome to the Regex Tester REPL! Type 'exit' to quit.
Enter regex pattern: (\d{4}-\d{2}-\d{2})
Enter test string: 2024-10-23
Match found: {'0': '2024-10-23'}
```

---

### **2. Parse Logs with Config Files**

You can configure the parsing process using YAML or JSON files. These config files allow you to specify the log files, regexes, table names, and columns to be stored in the SQLite database.

#### **Command:**
```bash
python parser_cli.py --config config.yaml
```

#### **YAML Example:**
```yaml
files:
  - file: "example.log"
    table: "example"
    regexes: 
      - "(P\\d+-T\\d+).*?(Info|Debug).*"
    columns:
      - process
      - date
      - time
      - log
```

#### **JSON Example:**
```json
{
  "files": [
    {
      "file": "example.log",
      "table": "example",
      "regexes": ["(P\\d+-T\\d+).*?(Info|Debug).*"],
      "columns": ["process", "date", "time", "log"]
    }
  ]
}
```

---

### **3. Parse Logs with CLI Arguments**

Instead of using config files, you can specify the log files, regex patterns, and database columns directly via CLI.

#### **Command:**
```bash
python parser_cli.py --db-path logs.db \
  --files example.log \
  --regexes "(P\\d+-T\\d+).*?(Info|Debug).*" \
  --tables example \
  --columns "process,date,time,log" \
  --log-level DEBUG
```

This command parses the `example.log` file using the provided regex pattern, stores the parsed data in the SQLite database at `logs.db`, and logs debug information.

---

### **4. Logging and Error Handling**

`parser_cli.py` supports customizable logging levels and outputs logs to files.

#### **Command:**
```bash
python parser_cli.py --db-path logs.db \
  --files example.log \
  --regexes "(P\\d+-T\\d+).*?(Info|Debug).*" \
  --tables example \
  --columns "process,date,time,log" \
  --log-level INFO \
  --log-file parser.log
```

This example logs all information at `INFO` level and stores logs in `parser.log`. If an error occurs (e.g., missing files or incorrect regex), an appropriate error message will be logged and printed to the console.

---

### **5. Multiprocessing Support**

To speed up parsing for multiple files, enable multiprocessing by passing the `--multiprocessing` flag.

#### **Command:**
```bash
python parser_cli.py --config config.yaml --multiprocessing
```

This uses all available CPU cores to process multiple log files in parallel.

---

## **Code Examples**

### **Regex REPL Example**
```bash
python parser_cli.py --repl
```
Output:
```
Welcome to the Regex Tester REPL! Type 'exit' to quit.
Enter regex pattern: (\d{4}-\d{2}-\d{2})
Enter test string: 2024-10-23
Match found: {'0': '2024-10-23'}
```

### **Parse Logs Using Config File**
```bash
python parser_cli.py --config config.yaml
```
The `config.yaml` file specifies log files and regex patterns. Example:
```yaml
files:
  - file: "example.log"
    table: "example"
    regexes: 
      - "(P\\d+-T\\d+).*?(Info|Debug).*"
    columns:
      - process
      - date
      - time
      - log
```

### **Parse Logs Using Command-Line Arguments**
```bash
python parser_cli.py --db-path logs.db \
  --files example.log \
  --regexes "(P\\d+-T\\d+).*?(Info|Debug).*" \
  --tables example \
  --columns "process,date,time,log"
```

### **Multiprocessing Example**
```bash
python parser_cli.py --config config.yaml --multiprocessing
```

---

## **Commands Summary**

- `--repl`: Launch the interactive Regex Tester REPL.
- `--config <config_file>`: Specify a YAML or JSON configuration file.
- `--db-path <db_path>`: Specify the path to the SQLite database.
- `--files <file1> <file2>`: List the log files to parse.
- `--regexes <regex1> <regex2>`: List the regex patterns for each file.
- `--tables <table1> <table2>`: List the table names for storing parsed data.
- `--columns <cols1> <cols2>`: List the columns for each table.
- `--multiprocessing`: Enable multiprocessing for faster log parsing.
- `--log-level <level>`: Set the logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL).
- `--log-file <log_file>`: Specify a log file to store the logs.

---


## Contributing

1. **Fork the repository**.
2. **Create a new branch**:
   ```bash
   git checkout -b feature-branch
   ```
3. **Commit your changes**:
   ```bash
   git commit -am 'Add new feature'
   ```
4. **Push to the branch**:
   ```bash
   git push origin feature-branch
   ```
5. **Open a pull request**.


---

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.
