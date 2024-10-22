# parser_cli.py
import argparse
import logging
from parser import LogParser, LogParserError

def run_parser(db_path, files, regexes, tables, columns, multiprocessing_enabled, log_level, log_file):
    """Run the parser with given configurations."""
    try:
        parser = LogParser(db_path=db_path, log_level=log_level, log_file=log_file)

        files_with_configs = {
            file: (table, regex, column_order.split(','))
            for file, regex, table, column_order in zip(files, regexes, tables, columns)
        }

        parser.parse_multiple_files(files_with_configs, enable_multiprocessing=multiprocessing_enabled)
        print("Parsing completed successfully.")
    except LogParserError as e:
        print(f"Error occurred: {e}")

def regex_repl():
    """Interactive REPL for testing regex patterns."""
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
    """CLI entry point for LogxDB."""
    parser = argparse.ArgumentParser(description="LogxDB: Log Parser with CLI and Regex REPL")

    # Optional REPL for regex testing
    parser.add_argument('--repl', action='store_true', help='Launch interactive regex testing REPL')

    # Required arguments for file parsing
    parser.add_argument('--db-path', type=str, help='Path to the SQLite database')
    parser.add_argument('--files', nargs='+', help='List of log files to parse')
    parser.add_argument('--regexes', nargs='+', help='List of regex patterns for each file')
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

    # Ensure all required arguments are provided for file parsing
    if not (args.db_path and args.files and args.regexes and args.tables and args.columns):
        parser.error("The following arguments are required: --db-path, --files, --regexes, --tables, --columns")

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

if __name__ == "__main__":
    main()
