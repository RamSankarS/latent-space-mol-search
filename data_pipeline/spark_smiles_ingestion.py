import argparse
import os
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType
from pyspark.sql.functions import col, length


def build_spark_session(app_name: str = "SmilesIngestion") -> SparkSession:
    """Initialize a local Spark session optimized for memory."""
    return SparkSession.builder \
        .appName(app_name) \
        .config("spark.driver.memory", "4g") \
        .config("spark.executor.memory", "4g") \
        .getOrCreate()


def process_smiles_data(spark: SparkSession, input_path: str, output_path: str):
    """
    Ingest raw SMILES CSV, enforce schema, filter by length, and serialize to Parquet.
    """
    smiles_schema = StructType([
        StructField("smiles_string", StringType(), nullable=False)
    ])

    print(f"\n--- STEP 1: Reading data from {input_path} ---")
    raw_df = spark.read.csv(input_path, schema=smiles_schema, header=True)
    raw_df.show()

    print("\n--- STEP 2: Filtering and Dropping Duplicates (Triggering Shuffle) ---")
    clean_df = raw_df.filter(length(col("smiles_string")) <= 120)
    unique_df = clean_df.dropDuplicates(["smiles_string"])
    unique_df.show()

    print(f"\n--- STEP 3: Writing Parquet to {output_path} ---")
    # Windows/Hadoop Write Workaround: Convert to Pandas for local serialization
    # In production on GCP Dataproc, this would simply be: unique_df.write.parquet("gs://...")
    pandas_df = unique_df.toPandas()
    pandas_df.to_parquet(output_path, index=False)

    print("\n--- PIPELINE COMPLETE ---")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="PySpark SMILES Ingestion Pipeline")
    parser.add_argument("--input", type=str, required=True, help="Path to raw CSV data")
    parser.add_argument("--output", type=str, required=True, help="Path to output Parquet directory")
    args = parser.parse_args()

    abs_input = os.path.abspath(args.input)
    abs_output = os.path.abspath(args.output)

    spark_session = build_spark_session()
    process_smiles_data(spark_session, abs_input, abs_output)
    spark_session.stop()