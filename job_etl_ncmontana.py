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
raw_data = glueContext.create_dynamic_frame.from_catalog(
    database="project-python-aws-spark-forutube-dbb", 
    table_name="raw_statistics", 
    transformation_ctx="raw_data", 
    push_down_predicate = predicate_pushdown
    )

# Script generated for node Amazon S3
glueContext.write_dynamic_frame.from_options(
    frame=raw_data, 
    connection_type="s3", 
    format="glueparquet", 
    connection_options={
        "path": "s3://project-python-aws-spark-forutube/youtube/raw_statistics/", 
        "partitionKeys": ["region"]
    },
    format_options={"compression": "snappy"}, 
    transformation_ctx="output_to_s3")

# Commit the job
job.commit()