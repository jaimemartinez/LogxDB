import argparse
import logging
import json
import re
import yaml
from parser import LogParser, LogParserError

def run_parser(db_path, files, regexes, tables, columns, multiprocessing_enabled, log_level, log_file):
    """Run the parser with given configurations."""
    try:
        parser = LogParser(db_path=db_path, log_level=log_level, log_file=log_file)

        files_with_configs = {
            file: (table, regex_list.split(','), column_order.split(','))
            for file, regex_list, table, column_order in zip(files, regexes, tables, columns)
        }

        parser.parse_multiple_files(files_with_configs, enable_multiprocessing=multiprocessing_enabled)
        print("Parsing completed successfully.")
    except LogParserError as e:
        print(f"Error occurred: {e}")
    except Exception as e:
        logging.critical(f"Unexpected error: {e}")
        print(f"Critical error occurred: {e}")

def regex_repl():
    """Interactive REPL for testing regex patterns."""
    print("Welcome to the Regex Tester REPL! Type 'exit' to quit.")
    while True:
        try:
            pattern = input("Enter regex pattern: ")
            if pattern.lower() == 'exit':
                break
            test_string = input("Enter test string: ")
            matches = list(re.finditer(pattern, test_string))
            if matches:
                for i, match in enumerate(matches, start=1):
                    print(f"Match {i}:", json.dumps(match.groupdict(), indent=4))
            else:
                print("No match found.")
        except re.error as e:
            print(f"Invalid regex: {e}")

def run_with_config_file(config_file, multiprocessing_enabled):
    """Run the parser using a YAML or JSON configuration file."""
    try:
        parser = LogParser(db_path='logs.db', log_level='INFO')
        parser.parse_with_config_file(config_file, enable_multiprocessing=multiprocessing_enabled)
        print(f"Parsing completed successfully using config file: {config_file}")
    except LogParserError as e:
        print(f"Error occurred: {e}")
    except Exception as e:
        logging.critical(f"Unexpected error: {e}")
        print(f"Critical error occurred: {e}")

def validate_files_exist(files):
    """Validate if all files exist."""
    missing_files = [file for file in files if not os.path.isfile(file)]
    if missing_files:
        raise LogParserError(f"File(s) not found: {', '.join(missing_files)}")

def main():
    """CLI entry point for LogxDB."""
    parser = argparse.ArgumentParser(description="LogxDB: Log Parser with CLI and Regex REPL")

    # Optional REPL for regex testing
    parser.add_argument('--repl', action='store_true', help='Launch interactive regex testing REPL')

    # Optional configuration file for parsing
    parser.add_argument('--config', type=str, help='Path to a YAML or JSON configuration file')

    # Required arguments for file parsing (if not using config file)
    parser.add_argument('--db-path', type=str, help='Path to the SQLite database')
    parser.add_argument('--files', nargs='+', help='List of log files to parse')
    parser.add_argument('--regexes', nargs='+', help='Comma-separated regex patterns for each file')
    parser.add_argument('--tables', nargs='+', help='Table names for each log file')
    parser.add_argument('--columns', nargs='+', help='Comma-separated column names for each table')
    parser.add_argument('--multiprocessing', action='store_true', help='Enable multiprocessing')

    # Logging configuration
    parser.add_argument('--log-level', type=str, default='INFO', 
                        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'], 
                        help='Set the logging level (default: INFO)')
    parser.add_argument('--log-file', type=str, help='Path to a log file (optional)')

    args = parser.parse_args()

    # Launch REPL if requested
    if args.repl:
        regex_repl()
        return

    # Run the parser with a configuration file if provided
    if args.config:
        run_with_config_file(args.config, args.multiprocessing)
        return

    # Ensure all required arguments are provided for file parsing if no config is used
    if not (args.db_path and args.files and args.regexes and args.tables and args.columns):
        parser.error("The following arguments are required: --db-path, --files, --regexes, --tables, --columns")

    try:
        # Validate file existence
        validate_files_exist(args.files)

        # Run the parser with the provided configurations
        run_parser(
            db_path=args.db_path,
            files=args.files,
            regexes=args.regexes,
            tables=args.tables,
            columns=args.columns,
            multiprocessing_enabled=args.multiprocessing,
            log_level=args.log_level,
            log_file=args.log_file
        )
    except LogParserError as e:
        print(f"Error: {e}")
    except Exception as e:
        logging.critical(f"Unexpected error: {e}")
        print(f"Critical error: {e}")

if __name__ == "__main__":
    main()
