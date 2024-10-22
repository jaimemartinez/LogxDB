from parser import LogParser, LogParserError

# Define the regex patterns for each log format
regex_1 = r"(?P<timestamp>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) - (?P<level>\w+) - (?P<message>.*)"
regex_2 = r"(?P<date>\d{2}/\d{2}/\d{4}) \| (?P<event>\w+) \| (?P<details>.*)"

try:
    # Initialize the parser with the path to the SQLite database
    parser = LogParser(db_path="logs.db")

    # Define the files with their corresponding configurations
    files_with_configs = {
        "example_log_500_lines.log": ("table_500_lines", regex_1, ["timestamp", "level", "message"]),
        "another_log.log": ("another_table", regex_2, ["date", "event", "details"])
    }

    # Parse the files with multiprocessing enabled
    parser.parse_multiple_files(files_with_configs, enable_multiprocessing=True)

    print("All files processed successfully.")

except LogParserError as e:
    print(f"An error occurred: {e}")
