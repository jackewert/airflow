# Airflow Local Python Scripts Runner

This project sets up an Apache Airflow instance that can run Python scripts locally using Docker Compose.

## Prerequisites

- Docker and Docker Compose installed on your system
- At least 4GB of RAM available for Docker
- At least 10GB of disk space

## Quick Start

### 1. Set up the environment

First, set the AIRFLOW_UID environment variable (on Linux/Mac):

```bash
echo -e "AIRFLOW_UID=$(id -u)" > .env
```

On Windows, you can skip this step as the default value will be used.

### 2. Create necessary directories

```bash
mkdir -p ./dags ./logs ./plugins ./scripts ./config
```

### 3. Start Airflow

```bash
docker-compose up -d
```

This will start:
- PostgreSQL database
- Airflow webserver (accessible at http://localhost:8080)
- Airflow scheduler

### 4. Access Airflow Web UI

- Open your browser and go to: http://localhost:8080
- Login with:
  - Username: `admin`
  - Password: `admin`

## What's Included

### DAGs

1. **example_python_script_dag.py** - Demonstrates running Python functions directly in Airflow
   - `hello_world_task` - Simple hello world function
   - `data_processing_task` - Data processing with pandas
   - `file_operation_task` - File creation example

2. **external_script_dag.py** - Demonstrates running external Python scripts
   - `run_external_script` - Runs sample_script.py
   - `run_script_with_params` - Runs parameterized_script.py with arguments
   - `run_data_processing` - Runs data_processor.py
   - `run_reporting` - Runs generate_report.py

### Python Scripts

1. **scripts/sample_script.py** - Basic script with logging and file output
2. **scripts/parameterized_script.py** - Script that accepts command line arguments
3. **scripts/data_processor.py** - Data processing with pandas and numpy
4. **scripts/generate_report.py** - HTML report generation

## Running Your Own Scripts

### Method 1: Python Functions in DAGs

Create a new DAG file in the `dags/` directory:

```python
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

def my_function():
    # Your Python code here
    print("Hello from my function!")
    return "Success"

dag = DAG('my_dag', start_date=datetime(2024, 1, 1), schedule_interval='@daily')

task = PythonOperator(
    task_id='my_task',
    python_callable=my_function,
    dag=dag
)
```

### Method 2: External Scripts

1. Place your Python script in the `scripts/` directory
2. Create a DAG that uses `BashOperator` to run your script:

```python
from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

dag = DAG('my_script_dag', start_date=datetime(2024, 1, 1), schedule_interval='@daily')

task = BashOperator(
    task_id='run_my_script',
    bash_command='python /opt/airflow/scripts/my_script.py',
    dag=dag
)
```

## Useful Commands

### Check Airflow status
```bash
docker-compose ps
```

### View logs
```bash
# View all logs
docker-compose logs

# View specific service logs
docker-compose logs airflow-webserver
docker-compose logs airflow-scheduler
```

### Stop Airflow
```bash
docker-compose down
```

### Stop and remove volumes (will delete database)
```bash
docker-compose down -v
```

### Restart Airflow
```bash
docker-compose restart
```

## File Structure

```
airflow/
├── docker-compose.yml          # Docker Compose configuration
├── env_file                    # Environment variables
├── requirements.txt            # Python dependencies
├── README.md                  # This file
├── dags/                      # DAG definitions
│   ├── example_python_script_dag.py
│   └── external_script_dag.py
├── scripts/                   # Python scripts to run
│   ├── sample_script.py
│   ├── parameterized_script.py
│   ├── data_processor.py
│   └── generate_report.py
├── logs/                      # Airflow logs (created automatically)
├── plugins/                   # Airflow plugins (empty)
└── config/                    # Airflow configuration (empty)
```

## Troubleshooting

### Common Issues

1. **Port 8080 already in use**
   - Change the port in `docker-compose.yml`:
   ```yaml
   ports:
     - "8081:8080"  # Change 8081 to any available port
   ```

2. **Permission issues on Linux**
   - Make sure you've set the AIRFLOW_UID correctly
   - Run: `sudo chown -R 50000:0 ./dags ./logs ./plugins ./scripts`

3. **Scripts not found**
   - Ensure your scripts are in the `scripts/` directory
   - Check that the script paths in your DAGs are correct

4. **Dependencies missing**
   - Add required packages to `requirements.txt`
   - Restart the containers: `docker-compose restart`

### Checking Script Execution

1. Go to the Airflow web UI
2. Navigate to DAGs
3. Click on a DAG
4. Click on a task
5. View the logs to see script output

## Adding Custom Dependencies

To add new Python packages:

1. Edit `requirements.txt` and add your packages
2. Restart the containers:
   ```bash
   docker-compose down
   docker-compose up -d
   ```

## Security Notes

- Default admin credentials are `admin/admin` - change these in production
- The setup uses LocalExecutor for simplicity - use CeleryExecutor for production
- Consider adding authentication and SSL for production use

## Next Steps

1. Explore the example DAGs in the web UI
2. Try running the example DAGs manually
3. Create your own DAGs and scripts
4. Customize the configuration for your needs 