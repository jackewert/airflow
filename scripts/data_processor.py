#!/usr/bin/env python3
"""
Data processing script for Airflow execution
This script demonstrates data processing with pandas
"""

import sys
import logging
from datetime import datetime
import json
import pandas as pd
import numpy as np

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def generate_sample_data():
    """Generate sample data for processing"""
    logger.info("Generating sample data")
    
    # Create sample dataset
    np.random.seed(42)  # For reproducible results
    data = {
        'id': range(1, 1001),
        'value': np.random.randn(1000),
        'category': np.random.choice(['A', 'B', 'C', 'D'], 1000),
        'timestamp': pd.date_range('2024-01-01', periods=1000, freq='H')
    }
    
    df = pd.DataFrame(data)
    logger.info(f"Generated dataset with {len(df)} rows")
    
    return df

def process_data(df):
    """Process the data"""
    logger.info("Processing data")
    
    # Calculate statistics
    stats = {
        'total_records': len(df),
        'mean_value': df['value'].mean(),
        'std_value': df['value'].std(),
        'category_counts': df['category'].value_counts().to_dict(),
        'processing_timestamp': datetime.now().isoformat()
    }
    
    # Group by category and calculate statistics
    category_stats = df.groupby('category')['value'].agg(['mean', 'std', 'count']).to_dict()
    stats['category_statistics'] = category_stats
    
    logger.info(f"Data processing completed. Statistics: {json.dumps(stats, indent=2)}")
    
    return stats

def save_results(stats, df):
    """Save processing results"""
    logger.info("Saving results")
    
    # Save statistics
    stats_file = "/opt/airflow/logs/data_processing_stats.json"
    with open(stats_file, 'w') as f:
        json.dump(stats, f, indent=2)
    
    # Save processed data
    data_file = "/opt/airflow/logs/processed_data.csv"
    df.to_csv(data_file, index=False)
    
    logger.info(f"Results saved to {stats_file} and {data_file}")
    
    return stats_file, data_file

def main():
    """Main function for data processing"""
    logger.info("Starting data processing script")
    
    try:
        # Generate sample data
        df = generate_sample_data()
        
        # Process the data
        stats = process_data(df)
        
        # Save results
        stats_file, data_file = save_results(stats, df)
        
        logger.info("Data processing script completed successfully")
        logger.info(f"Output files: {stats_file}, {data_file}")
        
        return 0
        
    except Exception as e:
        logger.error(f"Data processing failed: {e}")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code) 