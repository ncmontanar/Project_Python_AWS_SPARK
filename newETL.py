
# exmple to use ->
""" 
Key Changes:
Table and Database Names: Make sure you replace your_database_name and your_table_name with the correct values from your Glue Data Catalog.
Output Path: The s3://project-python-aws-spark-forutube/youtube/processed_statistics/ path for writing should be different from the input S3 path.
Unique Variable Names: I replaced AmazonS3_node1714032****** with raw_data and output_to_s3 to avoid naming conflicts.
"""

import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job

# Get the job name passed as an argument
args = getResolvedOptions(sys.argv, ['JOB_NAME'])

# Initialize Spark and Glue contexts
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session

# Initialize AWS Glue job
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# Define predicate for pushdown filter
predicate_pushdown = "region in ('ca', 'gb', 'us')"

# Reading from AWS Glue Data Catalog
# Ensure that database and table_name are correctly referenced from your Glue Catalog
raw_data = glueContext.create_dynamic_frame.from_catalog(
    database="project-python-aws-spark-dbb", 
    table_name="raw_statistics", 
    transformation_ctx="raw_data",
    push_down_predicate=predicate_pushdown
)

# Writing the output back to S3 in Parquet format with Snappy compression
glueContext.write_dynamic_frame.from_options(
    frame=raw_data,
    connection_type="s3",
    format="glueparquet",
    connection_options={
        "path": "s3://project-python-aws-spark-yt/youtube/processed_statistics/",  # Change to processed output path
        "partitionKeys": ["region"]
    },
    format_options={"compression": "snappy"},
    transformation_ctx="output_to_s3"
)

# Commit the job
job.commit()

## ------------------------------------- version corrigée----------------------------##
import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job

# Get the job name passed as an argument
args = getResolvedOptions(sys.argv, ['JOB_NAME'])

# Initialize Spark and Glue contexts
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session

# Initialize AWS Glue job
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# Define predicate for pushdown filter
predicate_pushdown = "region in ('ca', 'gb', 'us')"

# Reading from AWS Glue Data Catalog
# Ensure that database and table_name are correctly referenced from your Glue Catalog
raw_data = glueContext.create_dynamic_frame.from_catalog(
    database="your_database_name", 
    table_name="your_table_name", 
    transformation_ctx="raw_data",
    push_down_predicate=predicate_pushdown
)

# Writing the output back to S3 in Parquet format with Snappy compression
glueContext.write_dynamic_frame.from_options(
    frame=raw_data,
    connection_type="s3",
    format="glueparquet",
    connection_options={
        "path": "s3://project-python-aws-spark-fy/youtube/processed_statistics/",  # Change to processed output path
        "partitionKeys": ["region"]
    },
    format_options={"compression": "snappy"},
    transformation_ctx="output_to_s3"
)

# Commit the job
job.commit()

## ---------------------- version originale----------------##
import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job

args = getResolvedOptions(sys.argv, ['JOB_NAME'])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

predicate_pushdown = "region in ('ca','gb','us')"

# Script generated for node AWS Glue Data Catalog
AmazonS3_node1714032****** = glueContext.create_dynamic_frame.from_catalog(database="your-raw-data-bucket-path", table_name="raw_statistics", transformation_ctx="AmazonS3_node1714032******", push_down_predicate = predicate_pushdown)

# Script generated for node Amazon S3
AmazonS3_node1714032****** = glueContext.write_dynamic_frame.from_options(frame=AmazonS3_node1714032******, connection_type="s3", format="glueparquet", connection_options={"path": "s3://your-raw-data-bucket-path/youtube/raw_statistics/", "partitionKeys": ["region"]}, format_options={"compression": "snappy"}, transformation_ctx="AmazonS3_node1714032******")

job.commit()
s3://project-python-aws-spark-yt/youtube/