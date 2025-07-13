#!/usr/bin/env python3
"""
Sample Python script for Airflow execution
This script demonstrates basic Python functionality that can be run by Airflow
"""

import sys
import logging
from datetime import datetime
import json

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    """Main function for the sample script"""
    logger.info("Starting sample script execution")
    
    # Get current timestamp
    current_time = datetime.now()
    logger.info(f"Script started at: {current_time}")
    
    # Simulate some work
    logger.info("Processing data...")
    
    # Create some sample data
    data = {
        "timestamp": current_time.isoformat(),
        "script_name": "sample_script.py",
        "status": "completed",
        "message": "Hello from sample script!"
    }
    
    # Log the data
    logger.info(f"Generated data: {json.dumps(data, indent=2)}")
    
    # Write output to a file
    output_file = "/opt/airflow/logs/sample_script_output.json"
    with open(output_file, 'w') as f:
        json.dump(data, f, indent=2)
    
    logger.info(f"Output written to: {output_file}")
    logger.info("Sample script completed successfully")
    
    return 0

if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code)
    except Exception as e:
        logger.error(f"Script failed with error: {e}")
        sys.exit(1) 