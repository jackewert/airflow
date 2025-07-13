from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator

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
    'external_python_scripts',
    default_args=default_args,
    description='DAG for running external Python scripts',
    schedule_interval=timedelta(days=1),
    catchup=False,
    tags=['external', 'scripts'],
)

# Task to run an external Python script
run_external_script = BashOperator(
    task_id='run_external_script',
    bash_command='python /opt/airflow/scripts/sample_script.py',
    dag=dag,
)

# Task to run a script with parameters
run_script_with_params = BashOperator(
    task_id='run_script_with_params',
    bash_command='python /opt/airflow/scripts/parameterized_script.py --input data.csv --output results.json',
    dag=dag,
)

# Task to run a data processing script
run_data_processing = BashOperator(
    task_id='run_data_processing',
    bash_command='python /opt/airflow/scripts/data_processor.py',
    dag=dag,
)

# Task to run a reporting script
run_reporting = BashOperator(
    task_id='run_reporting',
    bash_command='python /opt/airflow/scripts/generate_report.py',
    dag=dag,
)

# Define task dependencies
run_external_script >> run_script_with_params >> run_data_processing >> run_reporting 