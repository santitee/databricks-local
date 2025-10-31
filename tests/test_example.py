"""
Unit tests for the example Spark job
"""

import pytest
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from utils import get_spark_session
from pyspark.sql import SparkSession


@pytest.fixture(scope="session")
def spark():
    """
    Create a Spark session for testing
    """
    spark = get_spark_session("Test Session")
    yield spark
    spark.stop()


def test_spark_session_creation():
    """
    Test that we can create a Spark session
    """
    spark = get_spark_session("Test App")
    assert isinstance(spark, SparkSession)
    assert spark.sparkContext.appName == "Test App"
    spark.stop()


def test_basic_dataframe_operations(spark):
    """
    Test basic DataFrame operations
    """
    # Create test data
    data = [("Alice", 25), ("Bob", 30), ("Charlie", 35)]
    columns = ["name", "age"]
    df = spark.createDataFrame(data, columns)
    
    # Test basic operations
    assert df.count() == 3
    assert len(df.columns) == 2
    assert "name" in df.columns
    assert "age" in df.columns
    
    # Test filtering
    filtered_df = df.filter(df.age > 25)
    assert filtered_df.count() == 2


def test_aggregations(spark):
    """
    Test aggregation operations
    """
    from pyspark.sql.functions import avg, max as spark_max
    
    # Create test data
    data = [("A", 10), ("B", 20), ("A", 30), ("B", 40)]
    columns = ["category", "value"]
    df = spark.createDataFrame(data, columns)
    
    # Test aggregation
    result = df.groupBy("category").agg(
        avg("value").alias("avg_value"),
        spark_max("value").alias("max_value")
    ).collect()
    
    assert len(result) == 2
    
    # Check results (order might vary)
    results_dict = {row.category: (row.avg_value, row.max_value) for row in result}
    assert results_dict["A"] == (20.0, 30)
    assert results_dict["B"] == (30.0, 40)


def test_sql_operations(spark):
    """
    Test SQL operations
    """
    # Create test data
    data = [("Product1", 100), ("Product2", 200), ("Product3", 150)]
    columns = ["product", "sales"]
    df = spark.createDataFrame(data, columns)
    
    # Create temp view
    df.createOrReplaceTempView("sales")
    
    # Test SQL query
    result = spark.sql("SELECT COUNT(*) as row_count FROM sales").collect()
    assert result[0].row_count == 3
    
    # Test SQL with filtering
    result = spark.sql("SELECT * FROM sales WHERE sales > 120").collect()
    assert len(result) == 2