
# LogxDB: Simple Log Parsing Library for Everyone  

**LogxDB** is a  log parsing library that extracts data from log files, stores it in an SQLite database, and provides tools to interact with that data. With support for multi-line entries, multiprocessing, and YAML/JSON configuration files.

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

## Features

### **Core Log Parsing (`parser.py`)**  
- **Encoding Detection**: Detects the encoding of log files automatically using the `chardet` library.  
- **Regex-Based Parsing**: Extracts fields from logs with regular expressions to capture essential data.  
- **Multi-Line Entry Handling**: Automatically appends unmatched lines to the previous entry, handling complex multi-line logs.  
- **SQLite Database Support**: Stores parsed data into an SQLite database, either in memory or as a persistent file.  
- **Table Creation**: Automatically creates database tables if they don’t already exist.  
- **Error Handling and Logging**: Provides detailed logs for debugging, with multiple levels like DEBUG, INFO, WARNING, ERROR, and CRITICAL.  

---

### **Configuration Support (YAML/JSON)**  
- **YAML/JSON Configs**: Use easy-to-read YAML or JSON configuration files to specify log files, regex patterns, and table mappings.  
- **Dynamic Table Creation**: Automatically maps regex captures to database columns based on the configuration.  

---

### **Command-Line Interface (`parser_cli.py`)**  
- **Regex REPL**: Test regular expressions interactively through a terminal-based Read-Eval-Print Loop (REPL).  
- **CLI Parsing**: Parse logs directly from the command line using YAML/JSON configs or individual file specifications.  
- **Multiprocessing**: Leverage all available CPU cores for faster log parsing.  
- **Custom Logging Levels**: Control verbosity via CLI arguments (DEBUG, INFO, etc.).  
- **Log File Output**: Save parser logs to files for easy review and debugging.  

---

### **Multiprocessing**  
- **CLI Toggle**: Enable or disable multiprocessing with a simple CLI flag.  
- **Automatic Core Usage**: Utilizes all available CPU cores for efficient log parsing.  

---

## How to Use: `parser.py`

### 1. Parse a Single Log File
```python
from parser import LogParser

# Initialize the parser with the SQLite database
parser = LogParser(db_path='logs.db', log_level='INFO')

# Parse the log file using a regex pattern
data = parser.parse_file(
    'web_server.log',
    r'(?P<ip>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}) - \[(?P<timestamp>.*?)\] - (?P<status>\d+)'
)

print(data)
```

**Expected Input (`web_server.log`):**
```
192.168.0.1 - [22/Oct/2024:10:15:32] - 200
```

**Expected Output:**
```python
[{'ip': '192.168.0.1', 'timestamp': '22/Oct/2024:10:15:32', 'status': '200'}]
```

---

### 2. Use YAML Configuration

Create a `config.yaml`:
```yaml
files:
  - file: web_server.log
    table: web_logs
    regex: (?P<ip>\d+\.\d+\.\d+\.\d+) - \[(?P<timestamp>.*?)\] - (?P<status>\d+)
    columns: [ip, timestamp, status]
```

**Python Code to Use YAML Config:**
```python
from parser import LogParser

parser = LogParser(db_path='logs.db', log_level='INFO')
parser.parse_with_config_file('config.yaml', enable_multiprocessing=False)
```

---

### 3. Use JSON Configuration

Create a `config.json`:
```json
{
  "files": [
    {
      "file": "web_server.log",
      "table": "web_logs",
      "regex": "(?P<ip>\\d+\\.\\d+\\.\\d+\\.\\d+) - \\[(?P<timestamp>.*?)\\] - (?P<status>\\d+)",
      "columns": ["ip", "timestamp", "status"]
    }
  ]
}
```

**Python Code to Use JSON Config:**
```python
from parser import LogParser

parser = LogParser(db_path='logs.db', log_level='INFO')
parser.parse_with_config_file('config.json', enable_multiprocessing=True)
```

---

## How to Use: `parser_cli.py`

### 1. Parse a Single Log File

```bash
python parser_cli.py --db-path logs.db --files web_server.log   --regexes "(?P<ip>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}) - \[(?P<timestamp>.*?)\] - (?P<status>\d+)"   --tables web_logs --columns ip,timestamp,status
```

---

### 2. Use YAML/JSON Config File

#### YAML Config (`config.yaml`):
```yaml
files:
  - file: web_server.log
    table: web_logs
    regex: (?P<ip>\d+\.\d+\.\d+\.\d+) - \[(?P<timestamp>.*?)\] - (?P<status>\d+)
    columns: [ip, timestamp, status]
```

#### Run with YAML Config:
```bash
python parser_cli.py --config config.yaml --multiprocessing
```

---

### 3. Test Regex with Interactive REPL

```bash
python parser_cli.py --repl
```

**Example REPL Session:**
```
Enter regex pattern: (?P<ip>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})
Enter test string: 192.168.0.1
Match found:
{
    "ip": "192.168.0.1"
}
```

---

## Installation

1. **Install Python Dependencies**:
   ```bash
   pip install chardet pyyaml
   ```

2. **Clone the Repository**:
   ```bash
   git clone <repository_url>
   cd logxdb
   ```

3. **Run Tests**:
   Use the `test/` folder for sample scripts and logs.

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
