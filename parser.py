
import re
import sqlite3
import logging
import chardet
import yaml
import json
from multiprocessing import Pool, cpu_count

class LogParserError(Exception):
    pass

class LogParser:
    def __init__(self, db_path, log_level='INFO', log_file=None):
        self.db_path = db_path
        self.configure_logging(log_level, log_file)

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

    def detect_encoding(self, file_path):
        with open(file_path, 'rb') as f:
            raw_data = f.read(1024)
            return chardet.detect(raw_data)['encoding']

    def parse_file(self, file_path, regex):
        encoding = self.detect_encoding(file_path)
        results = []
        with open(file_path, encoding=encoding) as f:
            for line in f:
                match = re.match(regex, line)
                if match:
                    results.append(match.groupdict())
        return results

    def load_config(self, config_file):
        with open(config_file, 'r') as f:
            if config_file.endswith('.yaml'):
                return yaml.safe_load(f)
            elif config_file.endswith('.json'):
                return json.load(f)
            else:
                raise LogParserError("Unsupported config format")

    def run_with_config(self, config):
        for file_config in config['files']:
            data = self.parse_file(file_config['file'], file_config['regex'])
            self.save_to_db(file_config['table'], data, file_config['columns'])

    def save_to_db(self, table, data, columns):
        conn = sqlite3.connect(self.db_path)
        conn.execute(f"CREATE TABLE IF NOT EXISTS {table} (id INTEGER PRIMARY KEY, {', '.join(columns)})")
        conn.executemany(
            f"INSERT INTO {table} ({', '.join(columns)}) VALUES ({', '.join(['?'] * len(columns))})",
            [[entry.get(col) for col in columns] for entry in data]
        )
        conn.commit()
        conn.close()
