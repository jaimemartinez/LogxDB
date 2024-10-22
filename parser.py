
# parser.py
import re
import sqlite3
import logging
from datetime import datetime
from multiprocessing import Pool, cpu_count
import chardet  # For encoding detection

logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    level=logging.INFO
)

class LogParserError(Exception):
    """Custom exception class for LogParser errors."""
    pass

class LogParser:
    def __init__(self, db_path):
        """Initialize the parser with a database path."""
        self.db_path = db_path

    def detect_encoding(self, file_path):
        """Detect the encoding of the given file."""
        with open(file_path, 'rb') as f:
            raw_data = f.read(1024)  # Read the first 1KB of the file
            result = chardet.detect(raw_data)
            encoding = result['encoding']
            logging.info(f"Detected encoding for {file_path}: {encoding}")
            return encoding

    def parse_line(self, line, regex):
        """Parses a single log line using the provided regex."""
        match = re.match(regex, line)
        return match.groupdict() if match else None

    def parse_file(self, file_path, regex):
        """Parses a log file line by line, handling multi-line entries."""
        results = []
        current_entry = None

        encoding = self.detect_encoding(file_path)  # Auto-detect encoding

        with open(file_path, encoding=encoding) as f:
            for line in f:
                parsed_line = self.parse_line(line, regex)

                if parsed_line:
                    if current_entry:
                        results.append(current_entry)
                    current_entry = parsed_line
                else:
                    if current_entry:
                        current_entry['message'] += "\n" + line.strip()

            if current_entry:
                results.append(current_entry)

        return results

    def create_table(self, conn, table_name, columns):
        """Creates a table if it doesn't exist."""
        columns_definition = ", ".join([f"{col} TEXT" for col in columns])
        query = f"CREATE TABLE IF NOT EXISTS {table_name} (id INTEGER PRIMARY KEY AUTOINCREMENT, {columns_definition});"
        conn.execute(query)

    def save_to_db(self, table_name, data, column_order):
        """Save parsed data to the SQLite database."""
        conn = sqlite3.connect(self.db_path)  # Create a new connection
        columns = column_order
        self.create_table(conn, table_name, columns)

        placeholders = ", ".join(["?"] * len(columns))
        query = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({placeholders})"

        for entry in data:
            values = [entry.get(col, None) for col in columns]
            conn.execute(query, values)

        conn.commit()
        conn.close()  # Close the connection after saving

    def process_file(self, config):
        """Process a single file with its configuration."""
        file_path, (table_name, regex, column_order) = config
        logging.info(f"Processing file: {file_path}")

        data = self.parse_file(file_path, regex)
        self.save_to_db(table_name, data, column_order)

    def parse_multiple_files(self, files_with_configs, enable_multiprocessing=False):
        """Parse multiple files and save each to its corresponding table."""
        if enable_multiprocessing:
            logging.info("Multiprocessing enabled.")
            with Pool(processes=cpu_count()) as pool:
                pool.map(self.process_file, files_with_configs.items())
        else:
            logging.info("Processing files sequentially.")
            for config in files_with_configs.items():
                self.process_file(config)
