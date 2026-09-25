"""
Data Processing Pipeline - CLI Template

DS 3500 - MP1

Usage:
    python pipeline.py --input data.csv --output clean.csv
    python pipeline.py --input data.csv --output results.json --format json --verbose
"""

import argparse
import logging
import sys
from pathlib import Path


logger = logging.getLogger(__name__)


def setup_logging(verbose=False):
    """Configure logging for the pipeline."""

    level = logging.INFO

    if verbose:
        level = logging.DEBUG

    logging.basicConfig(
        level=level,
        format="%(asctime)s %(levelname)-8s %(message)s",
        datefmt="%H:%M:%S"
    )


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
        "--format",
        choices=["csv", "json"],
        default="csv",
        help="Output format"
    )

    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Show the detailed DEBUG messages"
    )

    return parser.parse_args()


def validate_input(filepath):
    """Check whether the input path exists and is a file."""
    pass  # TODO: implement


def main():
    """Main pipeline function."""
    pass  # TODO: implement


if __name__ == "__main__":
    main()