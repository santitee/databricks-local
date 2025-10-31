"""
Example Spark job for local development
"""

import os
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, count, avg


def create_spark_session(app_name: str = "LocalSparkApp") -> SparkSession:
    """
    Create a Spark session configured for local development
    """
    # Configure Spark for local mode
    spark = (SparkSession
             .builder
             .appName(app_name)
             .config("spark.sql.adaptive.enabled", "true")
             .config("spark.sql.adaptive.coalescePartitions.enabled", "true")
             .config("spark.serializer", "org.apache.spark.serializer.KryoSerializer")
             .getOrCreate())
    
    # Set log level to reduce noise
    spark.sparkContext.setLogLevel("WARN")
    
    return spark


def run_example_job():
    """
    Example Spark job that creates sample data and performs basic operations
    """
    spark = create_spark_session("Example Local Job")
    
    try:
        print("🚀 Starting Databricks local example job...")
        
        # Create sample data
        data = [
            ("Alice", 25, "Engineering", 75000),
            ("Bob", 30, "Marketing", 65000),
            ("Charlie", 35, "Engineering", 85000),
            ("Diana", 28, "Sales", 55000),
            ("Eve", 32, "Engineering", 90000),
            ("Frank", 29, "Marketing", 60000),
        ]
        
        columns = ["name", "age", "department", "salary"]
        df = spark.createDataFrame(data, columns)
        
        print("📊 Sample data created:")
        df.show()
        
        # Basic transformations
        print("🔍 Department summary:")
        dept_summary = (df
                       .groupBy("department")
                       .agg(
                           count("*").alias("employee_count"),
                           avg("salary").alias("avg_salary")
                       )
                       .orderBy("department"))
        
        dept_summary.show()
        
        # Filter high earners
        print("💰 High earners (>70k):")
        high_earners = df.filter(col("salary") > 70000)
        high_earners.show()
        
        # Save results to local file (optional)
        output_path = "data/output"
        if not os.path.exists("data"):
            os.makedirs("data")
            
        print(f"💾 Saving results to {output_path}")
        dept_summary.coalesce(1).write.mode("overwrite").option("header", "true").csv(output_path)
        
        print("✅ Job completed successfully!")
        
    except Exception as e:
        print(f"❌ Job failed with error: {str(e)}")
        raise
    finally:
        spark.stop()


def main():
    """
    Main entry point for the application
    """
    run_example_job()


if __name__ == "__main__":
    main()