#!/usr/bin/env python3
"""
Parameterized Python script for Airflow execution
This script demonstrates how to handle command line arguments
"""

import sys
import argparse
import logging
from datetime import datetime
import json
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description='Parameterized script for Airflow')
    parser.add_argument('--input', type=str, help='Input file path')
    parser.add_argument('--output', type=str, help='Output file path')
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')
    
    return parser.parse_args()

def process_data(input_file=None, output_file=None):
    """Process data based on input parameters"""
    logger.info("Processing data with parameters")
    
    # Simulate data processing
    data = {
        "timestamp": datetime.now().isoformat(),
        "script_name": "parameterized_script.py",
        "input_file": input_file,
        "output_file": output_file,
        "status": "completed",
        "processed_records": 100
    }
    
    # If input file is specified, simulate reading it
    if input_file and os.path.exists(input_file):
        logger.info(f"Reading input file: {input_file}")
        data["input_file_exists"] = True
    else:
        logger.info("No input file specified or file doesn't exist")
        data["input_file_exists"] = False
    
    # Write output
    if output_file:
        with open(output_file, 'w') as f:
            json.dump(data, f, indent=2)
        logger.info(f"Output written to: {output_file}")
    else:
        # Write to default location
        default_output = "/opt/airflow/logs/parameterized_script_output.json"
        with open(default_output, 'w') as f:
            json.dump(data, f, indent=2)
        logger.info(f"Output written to: {default_output}")
    
    return data

def main():
    """Main function for the parameterized script"""
    logger.info("Starting parameterized script execution")
    
    # Parse arguments
    args = parse_arguments()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
        logger.debug("Verbose mode enabled")
    
    logger.info(f"Arguments: input={args.input}, output={args.output}")
    
    # Process data
    result = process_data(args.input, args.output)
    
    logger.info("Parameterized script completed successfully")
    logger.info(f"Result: {json.dumps(result, indent=2)}")
    
    return 0

if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code)
    except Exception as e:
        logger.error(f"Script failed with error: {e}")
        sys.exit(1) 