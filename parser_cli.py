
import argparse
from parser import LogParser, LogParserError

def main():
    parser = argparse.ArgumentParser(description="LogxDB Parser CLI")
    parser.add_argument('--config', type=str, required=True, help='Path to YAML or JSON config file')
    parser.add_argument('--log-level', type=str, default='INFO', 
                        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'], help='Logging level')
    parser.add_argument('--log-file', type=str, help='Optional log file')

    args = parser.parse_args()
    try:
        log_parser = LogParser(log_level=args.log_level, log_file=args.log_file)
        config = log_parser.load_config(args.config)
        log_parser.run_with_config(config)
        print("Parsing completed successfully.")
    except LogParserError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
