"""
Utility functions for Databricks local development
"""

import os
from typing import Optional
from pyspark.sql import SparkSession


def get_spark_session(
    app_name: str = "DatabricksLocalApp",
    master: str = "local[*]",
    config: Optional[dict] = None
) -> SparkSession:
    """
    Get or create a Spark session with local configuration
    
    Args:
        app_name: Name of the Spark application
        master: Spark master URL (default: local[*])
        config: Additional Spark configuration dictionary
    
    Returns:
        SparkSession: Configured Spark session
    """
    builder = SparkSession.builder.appName(app_name).master(master)
    
    # Default configuration for local development
    default_config = {
        "spark.sql.adaptive.enabled": "true",
        "spark.sql.adaptive.coalescePartitions.enabled": "true",
        "spark.serializer": "org.apache.spark.serializer.KryoSerializer",
        "spark.sql.execution.arrow.pyspark.enabled": "true",
        "spark.driver.memory": "2g",
        "spark.executor.memory": "2g",
    }
    
    # Merge with user-provided config
    if config:
        default_config.update(config)
    
    # Apply configuration
    for key, value in default_config.items():
        builder = builder.config(key, value)
    
    spark = builder.getOrCreate()
    spark.sparkContext.setLogLevel("WARN")
    
    return spark


def load_env_vars():
    """
    Load environment variables from .env file if it exists
    """
    env_file = ".env"
    if os.path.exists(env_file):
        with open(env_file, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    os.environ[key.strip()] = value.strip()


def setup_local_environment():
    """
    Setup local environment for Databricks development
    """
    # Load environment variables
    load_env_vars()
    
    # Set default Spark environment variables if not already set
    spark_env_vars = {
        "SPARK_LOCAL_IP": "127.0.0.1",
        "SPARK_DRIVER_HOST": "localhost",
        "PYSPARK_PYTHON": "python",
    }
    
    for key, value in spark_env_vars.items():
        if key not in os.environ:
            os.environ[key] = value
    
    print("🔧 Local environment configured for Databricks development")