import os
import re
import sqlite3
import logging
import json
import yaml
from datetime import datetime
from multiprocessing import Pool, cpu_count
import chardet
from pathlib import Path
import codecs

class LogParserError(Exception):
    """Custom exception class for LogParser errors."""
    pass

class LogParser:
    def __init__(self, db_path, log_level='DEBUG', log_file=None):
        """Initialize the parser with a database path and logging configuration."""
        self.db_path = db_path
        self.configure_logging(log_level, log_file)
        logging.debug(f"Initialized LogParser with db_path='{db_path}', log_level='{log_level}', log_file='{log_file}'")

    def configure_logging(self, log_level, log_file):
        """Configures logging settings."""
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
        logging.info(f"Logging configured with level '{log_level}'")

    def detect_encoding(self, file_path):
        """Detect the encoding of the given file."""
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

    def find_matching_regex(self, file_path, regexes):
        """Find the first regex that matches any line in the file."""
        encoding = self.detect_encoding(file_path)
        with open(file_path, encoding=encoding, errors='replace') as f:
            for line in f:
                for regex in regexes:
                    if re.search(regex, line):
                        logging.info(f"Using regex: {regex} for file {file_path}")
                        return regex
        logging.error(f"No matching regex found for {file_path}.")
        raise LogParserError(f"No matching regex found for {file_path}.")

    def preprocess_log(self, file_path, regex):
        """Preprocess the log by keeping unmatched lines as part of the previous one."""
        processed_lines = []
        encoding = self.detect_encoding(file_path)
        current_line = ""

        try:
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
        except Exception as e:
            logging.error(f"Error preprocessing file '{file_path}': {e}")
            raise

        return processed_lines

    def parse_lines(self, lines, regex):
        """Parse each line and handle multiple matches within the same line."""
        parsed_entries = []

        for line in lines:
            logging.debug(f"Processing line: {line}")

            # Use re.finditer to capture all non-overlapping matches
            matches = list(re.finditer(regex, line))

            if matches:
                logging.debug(f"Found {len(matches)} matches in line.")

                for match in matches:
                    entry = match.groupdict()

                    # Replace '[new-line]' with '\n' for readability
                    entry = {k: v.replace("[new-line]", "\n") if isinstance(v, str) else v for k, v in entry.items()}

                    # Log the parsed entry
                    logging.debug(f"Parsed entry: {entry}")

                    # Add the parsed entry to the results
                    parsed_entries.append(entry)
            else:
                logging.warning(f"No matches found for line: {line}")

        logging.info(f"Parsed {len(parsed_entries)} entries.")
        return parsed_entries


    def create_table(self, conn, table_name, columns):
        """Create a table if it doesn't exist."""
        columns_definition = ", ".join([f"{col} TEXT" for col in columns])
        query = f"CREATE TABLE IF NOT EXISTS {table_name} (id INTEGER PRIMARY KEY AUTOINCREMENT, {columns_definition});"
        conn.execute(query)
        logging.debug(f"Created table '{table_name}' with columns {columns}")

    def save_to_db(self, table_name, data, column_order):
        """Save parsed data to the SQLite database."""
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

    def process_file(self, config):
        """Process a single file with its configuration."""
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

    def load_config(self, config_file):
        """Load configuration from a YAML or JSON file."""
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

    def parse_with_config_file(self, config_file, enable_multiprocessing=False):
        """Parse multiple files using a configuration file."""
        config = self.load_config(config_file)
        files_with_configs = {
            entry['file']: (entry['table'], entry['regexes'], entry['columns'], entry.get('stop_on_first_match', True))
            for entry in config['files']
        }
        self.parse_multiple_files(files_with_configs, enable_multiprocessing)

    def parse_multiple_files(self, files_with_configs, enable_multiprocessing=False):
        """Parse multiple files with multiprocessing support."""
        if enable_multiprocessing:
            with Pool(processes=cpu_count()) as pool:
                pool.map(self.process_file, files_with_configs.items())
        else:
            for config in files_with_configs.items():
                self.process_file(config)
