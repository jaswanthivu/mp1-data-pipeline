"""
Data Processing Pipeline - CLI Template

DS 3500 - MP1

Usage:
    python pipeline.py --input fixtures/sample_data.csv --output output/clean.csv --config config/config.yaml
    python pipeline.py --input fixtures/sample_data.csv --output output/clean.csv --config config/config.yaml --verbose
"""

import argparse
import logging
import sys

from src import (
    load_data,
    save_data,
    process_data,
    create_cleaning_report,
    validate_dataframe,
    setup_logging,
    validate_input
)


logger = logging.getLogger(__name__)


def parse_arguments():
    """Parse command-line arguments."""

    parser = argparse.ArgumentParser(
        description="Run the data processing pipeline"
    )

    parser.add_argument(
        "--input", "-i",
        required=True,
        help="Path to input file"
    )

    parser.add_argument(
        "--output", "-o",
        required=True,
        help="Path to output file"
    )

    parser.add_argument(
        "--config",
        required=True,
        help="Path to the YAML configuration file"
    )

    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Show the detailed DEBUG messages"
    )

    return parser.parse_args()


def main():
    """Main pipeline function."""
    args = parse_arguments()

    setup_logging(args.verbose)

    logger.debug(
        f"Arguments parsed: input={args.input}, "
        f"output={args.output}, config={args.config}"
    )

    if not validate_input(args.input):
        sys.exit(1)

    if not validate_input(args.config):
        sys.exit(1)

    try:
        data = load_data(args.input)
        config = load_data(args.config)
    except ValueError:
        sys.exit(1)

    validation = config["validation"]
    required_columns = validation["required_columns"]
    numeric_columns = validation["numeric_columns"]

    rows_before_validation = len(data)

    try:
        data = validate_dataframe(
            data,
            required_columns,
            numeric_columns
        )
    except ValueError:
        sys.exit(1)

    logger.info(
        f"Validation complete: {rows_before_validation} -> {len(data)} rows"
    )

    data_before = data.copy()

    try:
        data = process_data(data, config)
    except ValueError:
        sys.exit(1)

    report = create_cleaning_report(data_before, data)

    logger.info(
        f"Processing complete: {len(data_before)} -> {len(data)} rows"
    )

    output_path = save_data(data, args.output)
    logger.info(f"Saved cleaned data to {output_path}")

    print(report)


if __name__ == "__main__":
    main()