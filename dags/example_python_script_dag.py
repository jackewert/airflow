from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
import logging

# Define default arguments
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Define the DAG
dag = DAG(
    'example_python_scripts',
    default_args=default_args,
    description='Example DAG for running Python scripts',
    schedule_interval=timedelta(days=1),
    catchup=False,
    tags=['example', 'python'],
)

# Example Python function that could be in a separate script
def hello_world():
    """Simple function to demonstrate Python script execution"""
    logging.info("Hello from Python script!")
    print("Hello World from Python script!")
    return "Hello World completed successfully"

def data_processing_example():
    """Example function simulating data processing"""
    import pandas as pd
    import numpy as np
    
    # Create sample data
    data = {
        'id': range(1, 101),
        'value': np.random.randn(100),
        'category': np.random.choice(['A', 'B', 'C'], 100)
    }
    
    df = pd.DataFrame(data)
    
    # Process data
    summary = df.groupby('category')['value'].agg(['mean', 'std', 'count'])
    
    logging.info(f"Data processing completed. Summary:\n{summary}")
    print(f"Data processing completed. Summary:\n{summary}")
    
    return "Data processing completed"

def file_operation_example():
    """Example function for file operations"""
    import os
    from datetime import datetime
    
    # Create a sample file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"/opt/airflow/logs/sample_output_{timestamp}.txt"
    
    with open(filename, 'w') as f:
        f.write(f"File created at {datetime.now()}\n")
        f.write("This is a sample output file created by Airflow DAG\n")
    
    logging.info(f"File created: {filename}")
    print(f"File created: {filename}")
    
    return filename

# Define tasks
task1 = PythonOperator(
    task_id='hello_world_task',
    python_callable=hello_world,
    dag=dag,
)

task2 = PythonOperator(
    task_id='data_processing_task',
    python_callable=data_processing_example,
    dag=dag,
)

task3 = PythonOperator(
    task_id='file_operation_task',
    python_callable=file_operation_example,
    dag=dag,
)

# Define task dependencies
task1 >> task2 >> task3 