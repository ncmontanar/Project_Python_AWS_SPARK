## EndtoEnd DE Project_Python_AWS_SPARK_forUTube
from *https://deepakdewani484.medium.com/end-to-end-data-engineering-project-with-python-aws-and-spark-for-youtube-analysis-4e9f01e32ed1*

In today’s data-driven landscape, harnessing the power of large-scale data processing is paramount for organizations aiming to extract actionable insights. This article delves into an end-to-end data engineering project utilizing Python, AWS (Amazon Web Services), and SPARK. On average, it’s estimated that around 2.5 quintillion bytes of data are generated every day. This staggering amount of data comes from various sources such as social media interactions, online transactions, sensor readings, and more. With the proliferation of connected devices and digital technologies, this figure is expected to continue growing exponentially. Here, we’ll gather raw data from diverse sources and formats, posing a significant challenge due to its sheer volume, variety, and speed of accumulation. Through this comprehensive guide, we navigate the complexities of data ingestion, processing, and analysis, showcasing how these powerful technologies synergize to unlock the potential of big data.

--- 
1) aws configure 
fournir ID + secret key de mon user (à partir de la creation d'access keys en Identity and Access Management (IAM))

---
2) Transferring Source Data from Local to AWS S3 Bucket

  *https://www.kaggle.com/datasets/datasnaek/youtube-new?source=post_page-----4e9f01e32ed1--------------------------------*

---
3) 
#### Creation d'un bucket S3 en aws par console
: project-python-aws-spark-forutube
: project-python-aws-spark-yt 


   - 3.2 apreès d'avoir recuperer les fichier localment, aller au dossier et les copier en bucketS3 crée (en  aws cli, dans le dossier du projet- creer un dosser *data* et y coller)
   - exem : `aws s3 cp . s3://your-bucket-name/youtube/raw_statistics_reference_data/ --recursive --exclude "*" --include "*.json"`

  ``` 
        `aws s3 cp . s3://project-python-aws-spark-forutube/youtube/raw_statistics_reference_data/ --recursive --exclude "*" --include "*.json"`

        aws s3 cp CAvideos.csv s3://your-bucket-name/youtube/raw_statistics/region=ca/
        aws s3 cp DEvideos.csv s3://your-bucket-name/youtube/raw_statistics/region=de/
        aws s3 cp FRvideos.csv s3://your-bucket-name/youtube/raw_statistics/region=fr/
        aws s3 cp GBvideos.csv s3://your-bucket-name/youtube/raw_statistics/region=gb/
        aws s3 cp INvideos.csv s3://your-bucket-name/youtube/raw_statistics/region=in/
        aws s3 cp JPvideos.csv s3://your-bucket-name/youtube/raw_statistics/region=jp/
        aws s3 cp KRvideos.csv s3://your-bucket-name/youtube/raw_statistics/region=kr/
        aws s3 cp MXvideos.csv s3://your-bucket-name/youtube/raw_statistics/region=mx/
        aws s3 cp RUvideos.csv s3://your-bucket-name/youtube/raw_statistics/region=ru/
        aws s3 cp USvideos.csv s3://your-bucket-name/youtube/raw_statistics/region=us/
  ```
---
4) 
#### Creation of Data Catalog with AWS Glue

*project-python-aws-spark-yt-crawler*

Navigate to the AWS Management Console and search for AWS Glue. 
Once in the Glue service, locate and select “Crawlers” from the menu. 
Click on “Add Crawler” and proceed to the next step.

Add a datasource == our S3 bucket 

Specify the S3 bucket name where your data resides. Create an IAM role for Glue, 
ensuring it has sufficient permissions to access the S3 bucket. 
This involves attaching the policy for S3 Full Access to the IAM role. 
Name the role appropriately, and repeat this process for the GLUEServiceRole. 
Select these roles under “Choose an existing role.” 

Create a dBB *project-python-aws-spark-dbb*

Run the crawler (process of scanning the data and generating metadata for the data schema)

When finished, go to aws-athena, and localisate the *table data* (raw_statistics_reference_data)
-----------------------------
 there is an error here !!!
 This error typically surfaces after generating metadata and attempting to execute queries in AWS Athena. It stems from Athena’s expectation of data being in a format where keys and values are on a single line. However, if your data is structured differently, such as dictionaries spanning multiple lines, it can trigger errors like the one described.
-----------------------------
   - 4.2  ***Resolving the Uncleaned Data issue for the YouTube Analysis DE Project***
    Adding Output location for AWS Athena : in Athena, creer une DBB qui va stocker les résultats : athena/settings/add destination  (s3/buckets/results-queries-tosavetemp)
    
   - 4.3 Writing the ETL Code to convert JSON to Paraquet format using AWS Lambda : go to Lambda/Create function/Author from scratch
     - *convert-json-to-parquet-ncmontanar*
  
  - Creer una function lamda, from scratch, python 3.8 (voir fichier lambadafuntion)
  - This setup enables the Lambda function to utilize these variables during execution : Navigate to : lamda/configuration/Environment variables/Edit

    | Column Name | Value |
    |---|---|
    | glue_catalog_db_name | project-python-aws-spark-forutube-dbb |
    | glue_catalog_table_name | cleaned_statistics_reference_data |
    | s3_cleansed_layer |s3://cleaned-data-yt-ncmontanar/cleaned/ |
    | write_data_operation | append |

   - glue_catalog_db_name: Set this to the name of the database in AWS Glue Data Catalog. It's recommended to create a new database in Athena with the same name.
   - glue_catalog_table_name: Assign this variable the name of the table in the Glue Data Catalog where cleaned data will be stored. For example, "cleaned_statistics_reference_data".
   - s3_cleansed_layer: Specify the S3 path where cleaned data will be stored after execution. It's recommended to create a new bucket in S3 for this purpose.
   - write_data_operation: Set this variable to define the operation to perform when writing data. For example, "append".
 
 - To test our code, we first need to deploy it. Go to :  lambda/code/ deploy / Configure test events /Create a new test event/ Give the event a name, such as “S3 PUT/
     - complete the json template (see eventJson file) with the right names
     --- 
      **First Error**
      { “errorMessage”: “Unable to import module ‘lambda_function’: No module named ‘awswrangler’”, “errorType”: “Runtime.ImportModuleError”, “stackTrace”: [] }

      To resolve the error, we need to install the AWS wrangler module within the AWS Lambda function. Follow these steps:

      In the Lambda function configuration, scroll down to the bottom of the page.
      Search for the “Add Layer” section and click on it.
      From the drop-down menu of AWS Layers, search for “AWSSDKPandas-Python38.”
      Select the Layer version “18” or the latest available version.
      Click on “ADD” to add the layer to your Lambda function.
      This will install the AWS wrangler module within the Lambda function, allowing it to utilize the necessary functionality to process data effectively.

      **Second Error **
      we should increase the timeout duration for the Lambda function. Follow these steps:
      Go to the Lambda function configuration.
      Under “Configuration,” locate the “General configuration” section and click on “Edit.”
      Increase the “Memory” from 128 MB to 512 MB to ensure optimal performance.
      Next, adjust the “Timeout” from “3 sec” to “10 min 3 Sec” to provide sufficient time for the function to execute.
      Click on “Save” to apply the changes.
  
  - test it :
      ```
            {
        "paths": [
          "s3://cleaned-data-yt-ncmontanar/cleaned/b60670be085240a595a7692a4954d8a0.snappy.parquet"
        ],
        "partitions_values": {}
      } 
      ```
    the response indicates the successful completion of the Lambda function execution. It also provides information about the paths where the processed data is stored in Amazon S3. Typically, the cleaned data will be stored in the Parquet format within your designated S3 bucket.

  - Next, click on “Change default execution role” to configure permissions. 
    You’ll need to create a role in IAM that allows Lambda to communicate with various AWS services. 
    Head to IAM, search for “Role,” and click on “Create role.” Select “Lambda” as the service 
    that will use this role. Attach the “S3FullAccessRole” and “GlueServiceRole” 
    permission policies to the role, then save the role.
 
  - After confirming that the data has been stored in the expected Parquet format in your S3 bucket, you can proceed to check the Glue Data Catalog. Under “Database/tables,” you should find the table named “cleaned_statistics_reference_data.” This table will contain the cleaned metadata, including its columns and data types.
--- 
RESUME
   - creer les S3 
    results-queries-tosavetemp
    cleaned-data-ncmontanar/cleaned/

   - creer les DBB 
    project-python-aws-spark-forutube-dbb
   - creer les tables
    cleaned_statistics_reference_data
    raw_statistics
    raw_statistics_reference_data

   - creer les variables environn : 
    glue_catalog_db_name   		project-python-aws-spark-forutube-dbb
    glue_catalog_table_name		"cleaned_statistics_reference_data"
    s3_cleansed_layer			s3://cleaned-data-ncmontanar/cleaned/
    write_data_operation		append 
---  
5. ####  check your cleaned S3 bucket
go to athena / _cleaned_statistics_reference_data_ / SQL query

 - In the Lambda function, you’ll need to write code to process 
 the uncleaned data into a cleaned format :
---
6. #### Creation of Data Catalog with AWS Glue on cleaned Data
- To create the data catalog for the CSV files, go to :
Glue/Crawlers/Add Crawler/
  *crawfor_cleandata*
- Provide the S3 bucket path for the CSV files (the raw files)
  *s3://project-python-aws-spark-yt/youtube/raw_statistics/*
- chose the S3+glue role (admin)
- chose the raw dbb to store 
  *project-python-aws-spark-dbb*
- run the crawler and finish : create a data catalog for the CSV files, facilitating easy access and analysis of the raw data stored in Amazon S3.?

--- 
By ensuring that the raw_statistics data is partitioned by region, you’ll obtain data segmented according to regions. This enables you to query the data and retrieve outputs tailored to each specific region, enhancing the granularity and precision of your analysis.

Now that we have both the raw data and the newly generated cleaned data, we can perform a joining transformation to combine the information from both tables. This can be achieved using an Athena query
  ```
  SELECT a.title, a.category_id, b.snippet_title 
  FROM "project-python-aws-spark-dbb"."raw_statistics" a
  INNER JOIN "project-python-aws-spark-dbb"."_cleaned_statistics_reference_data_" b
  ON a.category_id = CAST(b.id as int);
  ```
---
#### Fixing the issue of Datatype
To rectify the datatype issue, follow these steps:

Change the datatype of the crawled version:
Navigate to Database/tables and select “cleaned_statistics_reference_data.”
Click on “Edit schema” and modify the datatype of the “id” column from “string” to “bigint”. Save the changes.
2. Delete the cleaned crawled version of data in the Parquet file.

3. Return to the Lambda function and test the function code using the existing test event.

4. This will generate the cleaned joined from two table Parquet file. Confirm this by checking inside the S3 bucket for the generated file.

5. Finally, run the query in Athena and check the output, which should be the same but without the need for the cast function.
---
7. #### PySpark Job to clean raw data
To transform the raw data CSV files into cleaned Parquet files, we’ll create an ETL (Extract, Transform, Load) job in AWS Glue. Follow these steps:

- go to Glue/ETL jobs/ new job
- use the ***newETL.py*** script to replace the sample script ; check the DBB names
- Chose the IAM role
- save and RUN (It then creates Parquet files containing the cleaned data. For simplicity, we’re partitioning the data for three regions only.)
  
    - The script retrieves the raw data from the raw data bucket and partitions it by region (e.g., “US”, “CA”, “GB”). It then creates Parquet files containing the cleaned data. For simplicity, we’re partitioning the data for three regions only.
    - After running the job, create new crawlers to catalog the data for each region.
    - Query the generated data in Athena and run join queries to combine the data from the two different tables.
    - This process streamlines the transformation of raw CSV data into cleaned Parquet format, enabling efficient querying and analysis in AWS Athena. 
---
8. #### Adding Triggers to Lambda Function