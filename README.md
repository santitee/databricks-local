# Databricks Local Development Setup

This project is configured for Databricks local development using Docker containers.

## Prerequisites

1. Docker Desktop installed and running
2. Python 3.8+ installed
3. Databricks CLI installed

## Setup Instructions

### 1. Environment Setup
```bash
# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate  # On macOS/Linux
# or
.venv\Scripts\activate     # On Windows

# Install dependencies
pip install -e ".[dev]"
```

### 2. Docker Setup
Make sure Docker Desktop is running:
```bash
docker ps
```

### 3. Local Development

#### Running PySpark Locally
```bash
# Set environment variables for local Spark
export SPARK_LOCAL_IP=127.0.0.1
export PYSPARK_PYTHON=python

# Run Python scripts with local Spark
python src/example_spark_job.py
```

#### Running with Databricks Connect (Local Mode)
```bash
# Configure Databricks Connect for local mode
databricks connect configure --profile local

# Test the connection
python -c "from pyspark.sql import SparkSession; spark = SparkSession.builder.appName('test').getOrCreate(); print(spark.range(10).count())"
```

## Project Structure

```
databricks-local/
├── databricks.yml          # Databricks bundle configuration
├── pyproject.toml          # Python project configuration
├── src/                    # Source code
│   ├── __init__.py
│   └── example_spark_job.py
├── notebooks/              # Jupyter notebooks
│   └── example_notebook.ipynb
├── tests/                  # Unit tests
│   └── test_example.py
├── data/                   # Sample data files
└── README.md              # This file
```

## Running Tests

```bash
# Run all tests
pytest tests/

# Run with coverage
pytest --cov=src tests/
```

## Common Commands

```bash
# Validate bundle configuration
databricks bundle validate

# Deploy to local target
databricks bundle deploy --target local

# Run a job locally
databricks bundle run sample_job --target local
```

## Troubleshooting

1. **Docker not running**: Start Docker Desktop
2. **Permission errors**: Check Docker permissions
3. **Port conflicts**: Ensure ports 4040-4044 are available for Spark UI
4. **Memory issues**: Increase Docker memory allocation

## Environment Variables

Create a `.env` file for local configuration:
```
SPARK_LOCAL_IP=127.0.0.1
SPARK_DRIVER_MEMORY=2g
SPARK_EXECUTOR_MEMORY=2g
```# databricks-local
