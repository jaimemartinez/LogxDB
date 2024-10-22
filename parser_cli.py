
# parser_cli.py
import argparse
import re
import sys
import json
import sqlite3
import logging
from parser import LogParser, LogParserError

logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    level=logging.INFO
)

def run_parser(db_path, files, regexes, tables, columns, multiprocessing_enabled):
    """Run the parser on specified files with given configurations."""
    try:
        parser = LogParser(db_path=db_path)

        files_with_configs = {
            file: (table, regex, column_order.split(','))
            for file, regex, table, column_order in zip(files, regexes, tables, columns)
        }

        parser.parse_multiple_files(files_with_configs, enable_multiprocessing=multiprocessing_enabled)
        print("Parsing completed successfully.")

    except LogParserError as e:
        print(f"Error occurred: {e}")

def regex_repl():
    """Interactive REPL to test regex patterns."""
    print("Welcome to the Regex Tester REPL! Type 'exit' to quit.")
    while True:
        pattern = input("Enter regex pattern: ")
        if pattern.lower() == 'exit':
            break
        test_string = input("Enter test string: ")
        match = re.match(pattern, test_string)
        if match:
            print("Match found:", json.dumps(match.groupdict(), indent=4))
        else:
            print("No match found.")

def main():
    """CLI entry point for the log parser."""
    parser = argparse.ArgumentParser(description="LogxDB: Log Parser with CLI and Regex REPL")

    parser.add_argument('--db-path', type=str, required=True, help='Path to the SQLite database')
    parser.add_argument('--files', nargs='+', required=True, help='List of log files to parse')
    parser.add_argument('--regexes', nargs='+', required=True, help='List of regex patterns for each file')
    parser.add_argument('--tables', nargs='+', required=True, help='Table names for each log file')
    parser.add_argument('--columns', nargs='+', required=True, help='Comma-separated column names for each table')
    parser.add_argument('--multiprocessing', action='store_true', help='Enable multiprocessing')
    parser.add_argument('--repl', action='store_true', help='Launch interactive regex testing REPL')

    args = parser.parse_args()

    if args.repl:
        regex_repl()
    else:
        if len(args.files) != len(args.regexes) or len(args.files) != len(args.tables) or len(args.files) != len(args.columns):
            print("Error: The number of files, regexes, tables, and columns must match.")
            sys.exit(1)

        run_parser(
            db_path=args.db_path,
            files=args.files,
            regexes=args.regexes,
            tables=args.tables,
            columns=args.columns,
            multiprocessing_enabled=args.multiprocessing
        )

if __name__ == "__main__":
    main()
