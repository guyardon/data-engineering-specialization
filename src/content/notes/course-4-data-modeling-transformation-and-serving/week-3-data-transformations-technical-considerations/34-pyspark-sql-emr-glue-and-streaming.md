---
title: "3.4 PySpark SQL, EMR, Glue, and Streaming"
course: "Course 4: Data Modeling, Transformation, and Serving"
courseSlug: "course-4-data-modeling-transformation-and-serving"
courseOrder: 4
week: "Week 3: Data Transformations & Technical Considerations"
weekSlug: "week-3-data-transformations-technical-considerations"
weekOrder: 3
order: 4
notionId: "1fc969a7-aa01-805e-8f9a-f648e027b479"
---

## 3.4.1 PySpark SQL

**PySpark SQL Introduction**

PySpark supports three approaches to data transformation: SQL-based manipulation, Python-based DataFrame operations, and a hybrid of both. All approaches run on the **same computation engine** and compile to the **same low-level code**.


---

**Creating a Temporary View**

A **temporary view** is a virtual table that exists only while the Spark session is active. It lets you write SQL queries against a DataFrame without physically storing data.


---

**Code Example**

```python
transactions_df.createOrReplaceTempView("orders")
spark.sql("SELECT * FROM orders").show()
```


---

**Running SQL Queries**

Use the Spark session's `.sql()` method with a SQL string, which returns a DataFrame with the result.


---

**Example: Total Amount Spent Per Order**

```python
spark.sql("""
    SELECT ID, SUM(Amount) AS total
    FROM orders
    GROUP BY ID
    ORDER BY total DESC
""").show()
```

---


**Using UDFs in SQL**

SQL queries cannot use raw Python functions directly. You must first register the function with Spark:

```python
def to_lower(word):
    return word.lower()

spark.udf.register("udf_to_lower", to_lower)
spark.sql("SELECT DISTINCT udf_to_lower(Country) FROM orders").show()
```


---

**Joining Multiple Views**

To join data from multiple DataFrames in SQL:

1. Create another DataFrame (e.g., `product_category_df`)
2. Register it as a temporary view (e.g., `items`)
3. Join the views using appropriate keys


---

**Example: Average Amount by Category**

```python
product_category_df.createOrReplaceTempView("items")
spark.sql("""
    SELECT items.Category, AVG(orders.Amount) AS avg_amount
    FROM items
    LEFT JOIN orders ON items.ItemID = orders.StockCode
    GROUP BY items.Category
""").show()
```

## 3.4.2 Amazon EMR

`Amazon EMR`

Amazon EMR is AWS's managed big data platform for scalable, distributed computing.


---

**Overview**

EMR enables distributed processing using clusters of EC2 instances and supports frameworks like Apache Spark, Hadoop, Hive, Presto, Flink, and HBase. It integrates natively with AWS services (S3, DynamoDB, RDS, Redshift) and decouples compute from storage via S3, allowing multiple EMR clusters to process the same dataset concurrently.


---

**How It Works**

EMR utilizes a cluster of nodes, each processing part of a job in parallel. Clusters scale elastically based on workload, and results can be stored in S3, HDFS, or other data stores.
![](/data-engineering-specialization-website/images/c54198cd-3e49-427b-b7ca-473955b23b44.png)


---

**EMR Studio and Serverless**

- **EMR Studio**: A browser-based IDE (built on Jupyter Notebooks) for interactive data analysis and job execution.
- **EMR Serverless**: Eliminates manual cluster management with automatic scaling.


---

**Setting Up an EMR Serverless Application**

1. Navigate to EMR in the AWS Console
2. Choose **EMR Serverless** and select "Get Started"
3. Create an application (e.g., *example app*) with default Spark settings
4. Choose setup options for batch or interactive workloads, and enable the interactive endpoint for EMR Studio
5. Click "Create and Start Application"


---

**Configuring EMR Studio**

To enable interactive workspaces, edit Studio settings and configure the IAM role (for AWS resource interaction) and S3 storage location (for workspace backups).


---

**Creating a Workspace and Notebook**

1. Create a new workspace (e.g., *example workspace*) and launch it
2. Attach the notebook to the EMR Serverless application, selecting compute resources and IAM role
3. Open the notebook and choose the PySpark kernel


---

**Running a Spark Job**

Load sample data from S3, use PySpark to perform calculations, and submit the job via the notebook. The job runs on the attached EMR Serverless backend.

EMR abstracts infrastructure management so you can focus on data workflows. EMR Studio combined with Serverless provides a streamlined, scalable, interactive processing experience.

## 3.4.3 AWS Glue

`AWS Glue`

AWS Glue is a **serverless data integration service** for ingesting, transforming, and loading data. It uses Apache Spark under the hood and supports data from databases, object stores (S3), logs, APIs, and streaming platforms. Transformed data can be loaded into downstream databases, data lakes, or warehouses.
![](/data-engineering-specialization-website/images/0a3f8fc8-7b04-4f52-a49f-85e2f077be12.png)


---

**Glue Jobs**

ETL pipelines in AWS Glue are called **Glue jobs**. There are three ways to create them:

- **AWS Glue DataBrew** -- A no-code/low-code visual interface that lets you transform data like a spreadsheet, powered by Spark. No coding required.
![](/data-engineering-specialization-website/images/ff19b07b-2a5e-41d9-8142-28e2cf9b41bb.png)

- **AWS Glue Studio** -- For users comfortable with Spark and ETL concepts. Provides a drag-and-drop UI for sources, transformations, and destinations, with the option to write custom Spark code.
![](/data-engineering-specialization-website/images/08f6aa8e-de5d-45ed-add7-315c4c8514dc.png)

- **Jupyter Notebooks** -- Write Spark code from scratch and run it via Glue, with optional assistance from Amazon Q Developer.
![](/data-engineering-specialization-website/images/d5eb27a1-9d63-43e2-98ae-10d89427a4af.png)

Glue jobs can be orchestrated using **Glue triggers, blueprints, and workflows**.


---

**Data Catalog and Governance**

AWS Glue includes a **centralized data catalog** for managing metadata and enabling governance. **Glue Crawlers** scan data sources to populate the catalog with schema, data types, structure, and partitioning information -- essential for building data lakes and lakehouses.


---

**Serverless and Scalable**

Glue is fully serverless. Jobs scale with **Data Processing Units (DPUs)**, starting small and expanding as needed.


---

**Integrations**

The Glue Data Catalog integrates with:
- `Amazon Athena` -- Run SQL queries over your data
- **Amazon QuickSight** -- Build BI dashboards
- **Amazon SageMaker** -- Build, train, and deploy ML models

---

## 3.4.4 AWS Glue Visual ETL

**AWS Glue Visual ETL**

Glue Visual ETL is a low-code, no-code interface in AWS Glue Studio for designing ETL pipelines. It generates a PySpark `glue_job.py` script automatically from a visual canvas, supporting sources (e.g., RDS), transforms (e.g., SQL queries), and targets (e.g., S3).


---

**Purpose**

The typical workflow is to ingest normalized data from relational sources (e.g., Amazon RDS), apply transformations to model it into a star schema, and load the results into an Amazon S3 data lake.
![](/data-engineering-specialization-website/images/7c1c27e4-db5f-4353-acc6-54b530b99847.png)


---

**glue_job.py Walkthrough**

The generated script includes:
- **Imports**: awsglue packages and pyspark modules
- **Function definitions**: e.g., `sparkSqlQuery` for running SQL on DataFrames
- **Argument parsing**: `getResolvedOptions` for JOB_NAME, connections, database, and S3 path
- **Context setup**: SparkContext, GlueContext, and Glue job initialization
- **ETL logic**: Extract via JDBC from source tables, transform with SQL to build dimension and fact tables, and load to S3 in Parquet format


---

**Visual ETL Walkthrough**

Open Glue Studio and create a new Visual ETL job with a blank canvas.
![](/data-engineering-specialization-website/images/bfeb185e-23dd-4cc6-a010-3de4d9e196fa.png)

**Configure sources**: Add MySQL source nodes (e.g., `customer_source`, `product_source`) and specify JDBC connections, table names, and IAM role.
![](/data-engineering-specialization-website/images/996df72b-2940-4c33-ab0a-628210926b27.png)

**Define transforms**: Add SQL Query nodes for each dimension (`dim_customers`, `dim_products`, `dim_location`) and fact (`fact_orders`), set aliases and parent nodes.
![](/data-engineering-specialization-website/images/1d59448b-7c64-45f3-8ecb-dcb28f3e0ab4.png)

**Set targets**: Add S3 target nodes, choose Parquet format, and point to S3 folders under `processed_data`.
![](/data-engineering-specialization-website/images/d2bf5624-7b9c-4666-baff-4d3b901ab1ad.png)

**Generate script**: Switch to the Script tab to preview the auto-generated `glue_job.py`.
![](/data-engineering-specialization-website/images/6578b1a4-7008-4105-b41b-ea515aa3561f.png)

![](/data-engineering-specialization-website/images/d2bf5624-7b9c-4666-baff-4d3b901ab1ad.png)


---

**Running the Glue Job**

Configure job details (number of workers, timeout, IAM role), save and run the job, then monitor until "Succeeded." Verify output by browsing the S3 `processed_data` folders for parquet files.


---

**Summary**

Visual ETL accelerates development by auto-generating code from graphical pipelines. You can still view and customize `glue_job.py` for deeper control. Alternative approaches include manual scripting or notebooks, but Visual ETL offers a rapid, serverless, reusable workflow.
![](/data-engineering-specialization-website/images/08722abf-5772-4086-b37e-163d528388dc.png)

```python
import sys

from awsglue import DynamicFrame
from awsglue.context import GlueContext
from awsglue.job import Job
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext

def sparkSqlQuery(
    glueContext, query, mapping, transformation_ctx
) -> DynamicFrame:
    for alias, frame in mapping.items():
        frame.toDF().createOrReplaceTempView(alias)
    result = spark.sql(query)
    return DynamicFrame.fromDF(result, glueContext, transformation_ctx)

args = getResolvedOptions(
    sys.argv, ["JOB_NAME", "glue_connection", "glue_database", "target_path"]
)
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args["JOB_NAME"], args)


# Extract data from source tables
customers = glueContext.create_dynamic_frame.from_options(
    connection_type="mysql",
    connection_options={
        "useConnectionProperties": "true",
        "dbtable": "classicmodels.customers",
        "connectionName": args["glue_connection"],
    },
    transformation_ctx="customers",
)

orders = glueContext.create_dynamic_frame.from_options(
    connection_type="mysql",
    connection_options={
        "useConnectionProperties": "true",
        "dbtable": "classicmodels.orders",
        "connectionName": args["glue_connection"],
    },
    transformation_ctx="orders",
)

orderdetails = glueContext.create_dynamic_frame.from_options(
    connection_type="mysql",
    connection_options={
        "useConnectionProperties": "true",
        "dbtable": "classicmodels.orderdetails",
        "connectionName": args["glue_connection"],
    },
    transformation_ctx="orderdetails",
)

products = glueContext.create_dynamic_frame.from_options(
    connection_type="mysql",
    connection_options={
        "useConnectionProperties": "true",
        "dbtable": "classicmodels.products",
        "connectionName": args["glue_connection"],
    },
    transformation_ctx="products",
)

productlines = glueContext.create_dynamic_frame.from_options(
    connection_type="mysql",
    connection_options={
        "useConnectionProperties": "true",
        "dbtable": "classicmodels.productlines",
        "connectionName": args["glue_connection"],
    },
    transformation_ctx="productslines",
)


# Transform data to build a star schema
sql_query_dim_customers = """
with dim_customers as (
    select
        customerNumber,
        customerName,
        contactLastName,
        contactFirstName,
        phone,
        addressLine1,
        addressLine2,
        creditLimit
    from customers
)
select * from dim_customers
"""

dim_customers = sparkSqlQuery(
    glueContext,
    query=sql_query_dim_customers,
    mapping={"customers": customers},
    transformation_ctx="dim_customers",
)

sql_query_dim_products = """
with dim_products as (
    select
        products.productCode,
        products.productName,
        products.productLine,
        products.productScale,
        products.productVendor,
        products.productDescription,
        productlines.textDescription as productLineDescription
    from products
    left join productlines using (productLine)
)
select * from dim_products
"""

dim_products = sparkSqlQuery(
    glueContext,
    query=sql_query_dim_products,
    mapping={
        "products": products,
        "productlines": productlines,
    },
    transformation_ctx="dim_products",
)

sql_query_dim_locations = """
with dim_locations as (
    select distinct
        postalCode,
        city,
        state,
        country
    from customers
)
select * from dim_locations
"""

dim_locations = sparkSqlQuery(
    glueContext,
    query=sql_query_dim_locations,
    mapping={"customers": customers},
    transformation_ctx="dim_locations",
)

sql_query_fact_orders = """
with fact_orders as (
    select
        orderLineNumber,
        orders.orderNumber,
        orders.customerNumber,
        location.postalCode,
        orderdetails.productCode,
        orders.orderDate,
        orders.requiredDate,
        orders.shippedDate,
        orders.status,
        orders.comments,
        orderdetails.quantityOrdered,
        orderdetails.priceEach,
        (orderdetails.quantityOrdered * orderdetails.priceEach) AS orderAmount,
        products.buyPrice,
        products.MSRP
    from orders
    left join orderdetails using (orderNumber)
    left join products using (productCode)
    left join customers using (customerNumber)
    left join location using (postalCode)
)
select * from fact_orders
"""

fact_orders = sparkSqlQuery(
    glueContext,
    query=sql_query_fact_orders,
    mapping={
        "orders": orders,
        "orderdetails": orderdetails,
        "products": products,
        "location": dim_locations,
    },
    transformation_ctx="fact_orders",
)


# Load transformed data into S3

dim_customers_to_s3 = glueContext.getSink(
    path=f"{args['target_path']}/dim_customers/",
    connection_type="s3",
    updateBehavior="UPDATE_IN_DATABASE",
    partitionKeys=[],
    compression="snappy",
    enableUpdateCatalog=True,
    transformation_ctx="dim_customers_to_s3",
)
dim_customers_to_s3.setCatalogInfo(
    catalogDatabase=args["glue_database"],
    catalogTableName="dim_customers",
)
dim_customers_to_s3.setFormat("glueparquet")
dim_customers_to_s3.writeFrame(dim_customers)

dim_products_to_s3 = glueContext.getSink(
    path=f"{args['target_path']}/dim_products/",
    connection_type="s3",
    updateBehavior="UPDATE_IN_DATABASE",
    partitionKeys=[],
    compression="snappy",
    enableUpdateCatalog=True,
    transformation_ctx="dim_products_to_s3",
)
dim_products_to_s3.setCatalogInfo(
    catalogDatabase=args["glue_database"],
    catalogTableName="dim_products",
)
dim_products_to_s3.setFormat("glueparquet")
dim_products_to_s3.writeFrame(dim_products)

dim_locations_to_s3 = glueContext.getSink(
    path=f"{args['target_path']}/dim_locations/",
    connection_type="s3",
    updateBehavior="UPDATE_IN_DATABASE",
    partitionKeys=[],
    compression="snappy",
    enableUpdateCatalog=True,
    transformation_ctx="dim_locations_to_s3",
)
dim_locations_to_s3.setCatalogInfo(
    catalogDatabase=args["glue_database"],
    catalogTableName="dim_locations",
)
dim_locations_to_s3.setFormat("glueparquet")
dim_locations_to_s3.writeFrame(dim_locations)

fact_orders_to_s3 = glueContext.getSink(
    path=f"{args['target_path']}/fact_orders/",
    connection_type="s3",
    updateBehavior="UPDATE_IN_DATABASE",
    partitionKeys=[],
    compression="snappy",
    enableUpdateCatalog=True,
    transformation_ctx="fact_orders_to_s3",
)
fact_orders_to_s3.setCatalogInfo(
    catalogDatabase=args["glue_database"],
    catalogTableName="fact_orders",
)
fact_orders_to_s3.setFormat("glueparquet")
fact_orders_to_s3.writeFrame(fact_orders)

job.commit()

```

## 3.4.5 DataFrames vs. SQL and Streaming

**PySpark - DataFrames vs. SQL**

PySpark offers two equivalent approaches for data transformation, and you can combine them freely since they compile to the same underlying code.


---

**Choosing Between SQL and Python**

| **Aspect** | **Spark DataFrames (Python)** | **Spark SQL** |
| --- | --- | --- |
| **Syntax Style** | Programmatic (Python API) | Declarative (SQL queries) |
| **Performance** | Comparable to SQL for simple tasks | Comparable to Python for simple tasks |
| **Complex Transformations** | Easier to implement (e.g., transpose with `.T`) | Limited support; some tasks not straightforward |
| **Code Reusability** | High -- supports modular, testable, and reusable code/libraries | Low -- limited reusability for complex queries |
| **Maintainability** | Easier due to modular Python code structure | Harder with large, complex SQL queries |
| **Team Skill Dependence** | Better if team is proficient in Python | Better if team is proficient in SQL |
| **Normalization / Data Cleaning** | More concise and flexible | Possible, but often more verbose |
| **Library Support** | Easy to build and reuse custom Python functions/libraries | No native library mechanism for reuse |
| **Hybrid Use** | Can be combined with SQL for best of both | Can be combined with Python API for flexibility |
| **Use Case Suitability** | Preferred for complex logic and reusable components | Preferred for simple, declarative data manipulation |


---

**Spark vs. Pandas**

| **Aspect** | **Pandas** | `Spark` |
| --- | --- | --- |
| **Data Size** | Suitable for small datasets that fit entirely in memory | Designed for large datasets that exceed memory limits |
| **Execution Mode** | Runs on a single machine | Distributed computing across multiple nodes or cloud clusters |
| **Simplicity** | Simpler setup and syntax for small-scale tasks | More complex setup but scalable for big data |
| **Performance** | Fast for small data; limited by machine memory | Scales horizontally; better for large-scale data processing |
| **Use Case** | Ideal for prototyping, local data exploration, and lightweight tasks | Ideal for production-level, high-volume data pipelines |
| **Infrastructure Requirements** | No cluster management needed | Requires cluster setup (local or cloud) |
| **Overhead** | Low overhead | Higher overhead due to distributed nature |
| **Recommendation** | Use when simplicity and speed for small data are priorities | Use when scalability, fault tolerance, and distributed processing are needed |


---

**Choosing the Right Tool for Batch Transformation**

The decision depends on data size, hardware specifications, and the desired trade-offs between performance and maintainability. SQL is simpler for straightforward tasks, while Python is more flexible and modular for complex logic.


---

**Streaming Transformations**

