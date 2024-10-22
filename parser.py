import re
import sqlite3
import logging
import json
import yaml
from datetime import datetime
from multiprocessing import Pool, cpu_count
import chardet
from pathlib import Path

class LogParserError(Exception):
    """Custom exception class for LogParser errors."""
    pass

class LogParser:
    def __init__(self, db_path, log_level='INFO', log_file=None):
        """Initialize the parser with a database path and logging configuration."""
        self.db_path = db_path
        self.configure_logging(log_level, log_file)
        logging.debug("Initialized LogParser with db_path='%s', log_level='%s', log_file='%s'",
                      db_path, log_level, log_file)

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
        logging.info("Logging configured with level '%s'", log_level)

    def detect_encoding(self, file_path):
        """Detect the encoding of the given file."""
        try:
            with open(file_path, 'rb') as f:
                raw_data = f.read(1024)
                result = chardet.detect(raw_data)
                encoding = result['encoding']
                logging.info("Detected encoding for '%s': %s", file_path, encoding)
                return encoding
        except Exception as e:
            logging.error("Failed to detect encoding for '%s': %s", file_path, str(e))
            raise

    def parse_line(self, line, regex):
        """Parses a single log line using the provided regex."""
        try:
            match = re.match(regex, line)
            if match:
                logging.debug("Parsed line successfully: %s", line.strip())
                return match.groupdict()
            else:
                logging.warning("No match found for line: %s", line.strip())
                return None
        except re.error as e:
            logging.critical("Regex error: %s", str(e))
            raise

    def parse_file(self, file_path, regex):
        """Parses a log file line by line, treating unmatched lines as continuations."""
        results = []
        current_entry = None
        encoding = self.detect_encoding(file_path)
    
        try:
            with open(file_path, encoding=encoding) as f:
                for line in f:
                    parsed_line = self.parse_line(line, regex)
                    
                    if parsed_line:
                        # If there is an existing entry, add it to results
                        if current_entry:
                            results.append(current_entry)
                        current_entry = parsed_line  # Start a new entry
                        logging.debug("New entry started: %s", current_entry)
                    else:
                        # If no match, treat as a continuation of the previous message
                        if current_entry:
                            current_entry['message'] = current_entry.get('message', '') + "\n" + line.strip()
                            logging.debug("Continuation added to entry: %s", current_entry)
                        else:
                            logging.warning("Orphaned continuation line: %s", line.strip())
    
                # Add the last entry if it exists
                if current_entry:
                    results.append(current_entry)
    
            logging.info("Finished parsing '%s'. Parsed %d entries.", file_path, len(results))
        except Exception as e:
            logging.error("Error parsing file '%s': %s", file_path, str(e))
            raise
    
        return results


    def create_table(self, conn, table_name, columns):
        """Creates a table if it doesn't exist."""
        columns_definition = ", ".join([f"{col} TEXT" for col in columns])
        query = f"CREATE TABLE IF NOT EXISTS {table_name} (id INTEGER PRIMARY KEY AUTOINCREMENT, {columns_definition});"
        try:
            conn.execute(query)
            logging.debug("Created table '%s' with columns: %s", table_name, columns)
        except sqlite3.Error as e:
            logging.critical("SQLite error creating table '%s': %s", table_name, str(e))
            raise

    def save_to_db(self, table_name, data, column_order):
        """Saves parsed data to the SQLite database."""
        conn = sqlite3.connect(self.db_path)
        try:
            self.create_table(conn, table_name, column_order)
            placeholders = ", ".join(["?"] * len(column_order))
            query = f"INSERT INTO {table_name} ({', '.join(column_order)}) VALUES ({placeholders})"
            for entry in data:
                values = [entry.get(col) for col in column_order]
                conn.execute(query, values)
            conn.commit()
            logging.info("Saved %d entries to table '%s'.", len(data), table_name)
        except sqlite3.Error as e:
            logging.error("SQLite error saving to table '%s': %s", table_name, str(e))
            raise
        finally:
            conn.close()

    def process_file(self, config):
        """Process a single file with its configuration."""
        try:
            file_path, (table_name, regex, column_order) = config
            logging.info("Processing file: '%s'", file_path)
            data = self.parse_file(file_path, regex)
            self.save_to_db(table_name, data, column_order)
        except Exception as e:
            logging.error("Error processing file '%s': %s", config[0], str(e))
            raise

    def parse_multiple_files(self, files_with_configs, enable_multiprocessing=False):
        """Parse multiple files with multiprocessing support."""
        if enable_multiprocessing:
            logging.info("Multiprocessing enabled.")
            with Pool(processes=cpu_count()) as pool:
                pool.map(self.process_file, files_with_configs.items())
        else:
            logging.info("Processing files sequentially.")
            for config in files_with_configs.items():
                self.process_file(config)

    def load_config(self, config_file):
        """Load configuration from a YAML or JSON file."""
        config_path = Path(config_file)
        if not config_path.exists():
            logging.critical("Configuration file '%s' not found.", config_file)
            raise LogParserError(f"Configuration file '{config_file}' not found.")

        logging.info("Loading configuration from '%s'.", config_file)
        try:
            if config_file.endswith(('.yaml', '.yml')):
                with open(config_file, 'r') as f:
                    return yaml.safe_load(f)
            elif config_file.endswith('.json'):
                with open(config_file, 'r') as f:
                    return json.load(f)
            else:
                raise LogParserError("Unsupported configuration file format. Use YAML or JSON.")
        except Exception as e:
            logging.critical("Error loading configuration: %s", str(e))
            raise

    def parse_with_config_file(self, config_file, enable_multiprocessing=False):
        """Parse multiple files using a YAML or JSON configuration file."""
        config = self.load_config(config_file)
        files_with_configs = {
            entry['file']: (
                entry['table'],
                entry['regex'],
                entry['columns']
            ) for entry in config['files']
        }
        self.parse_multiple_files(files_with_configs, enable_multiprocessing)
