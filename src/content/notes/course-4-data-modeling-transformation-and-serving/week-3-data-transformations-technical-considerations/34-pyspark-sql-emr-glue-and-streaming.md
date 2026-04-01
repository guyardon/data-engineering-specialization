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

**🧠 PySpark SQL Introduction**

- PySpark allows for:
- SQL-based data manipulation
- Python-based data manipulation
- A **hybrid** of both
- All code (SQL or Python) runs on the **same computation engine** and compiles to the **same low-level code**.

**🗂️  Creating a Temporary View**

- A **temporary view** is:
- A **virtual table**
- Doesn't hold data physically
- Exists **only while the Spark session is active**
- Lets you write SQL code to query a DataFrame
**Code Example**

```python
transactions_df.createOrReplaceTempView("orders")
spark.sql("SELECT * FROM orders").show()
```


**🔍 Running SQL Queries**

**Syntax**

- Use the Spark session's `.sql()` method
- Input a SQL query as a string
- Returns a DataFrame with the result
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


**🧩 Using UDFs in SQL**

**Define and Register a UDF**

- SQL queries **cannot use raw Python functions directly**
- First, register your function with Spark:
```python
def to_lower(word):
    return word.lower()

spark.udf.register("udf_to_lower", to_lower)
spark.sql("SELECT DISTINCT udf_to_lower(Country) FROM orders").show()
```


**🔗 Joining Multiple Views**

**Steps to Join Multiple Views**

1. Create another DataFrame (e.g., `product_category_df`)
2. Register it as a temporary view (e.g., `items`)
3. Join the views in a SQL query using appropriate keys
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

**:emr_aws: Amazon EMR**


**📘 Overview**

- Amazon EMR is a big data platform that supports multiple processing frameworks.
- Enables scalable, distributed computing using clusters of EC2 instances.
- Supports frameworks like Apache Spark, Hadoop, Hive, Presto, Flink, and HBase.
- Integrates natively with AWS services (e.g., S3, DynamoDB, RDS, Redshift).

**⚙️ How It Works**

- Utilizes a cluster of nodes, each processing a part of the job in parallel.
- Elastic cluster scaling: automatically adjusts resources based on workload.
- Job results can be stored in S3, HDFS, or other data stores.
- Decouples compute and storage via integration with S3.
- Multiple EMR clusters can process the same S3 dataset concurrently.
![](/data-engineering-specialization-website/images/c54198cd-3e49-427b-b7ca-473955b23b44.png)


**🧑‍💻 EMR Studio and Serverless**

- **EMR Studio**: A browser-based IDE (based on Jupyter Notebooks) for working with EMR.
- **EMR Serverless**: No need to manage clusters manually; scales automatically.
- EMR Studio enables interactive data analysis and job execution.

**🛠️ Setting Up an EMR Serverless Application**

1. Navigate to EMR in the AWS Console.
2. Choose **EMR Serverless** and select "Get Started."
3. Create an application (e.g., named *example app*) with default Spark settings.
4. Choose setup options:
- Defaults for batch or interactive workloads.
- Enable interactive endpoint for EMR Studio.
5. Click "Create and Start Application."

**🧾 Configuring EMR Studio**

- To enable interactive workspaces:
- Edit Studio settings.
- Configure:
  - IAM role (for AWS resource interaction).
  - S3 storage location (for workspace backups).
- Save changes and return to create a workspace.

**📝 Creating a Workspace and Notebook**

1. Create a new workspace (e.g., *example workspace*).
2. Launch the workspace.
3. Attach notebook to the EMR Serverless application.
- Select compute resources and interactive runtime IAM role.
4. Open notebook and choose kernel (e.g., PySpark).

**🚦 Running a Spark Job**

- Load sample taxi data from S3.
- Use PySpark to calculate average fare between two dates.
- Submit job via the notebook (`Shift+Enter` to execute).
- Job runs on the attached EMR Serverless backend.
- Result: Average fare is calculated and displayed (e.g., $50.64).

**🧠 Final Notes**

- EMR abstracts infrastructure management to let users focus on data workflows.
- EMR Studio + Serverless = streamlined, scalable, interactive data processing.
- You'll practice this in the upcoming lab with more advanced analysis.

## 3.4.3 AWS Glue

**:glue_aws: AWS Glue**


**🔧 What Is AWS Glue?**

- AWS Glue is a **data integration service** for ingesting, transforming, and loading data.
- AWS Glue uses **Apache Spark** under the hood to process data.
- It supports data from multiple sources: databases, object stores (e.g., Amazon S3), logs, APIs, streaming platforms, etc.
- Transformed data can be loaded into downstream systems like databases, data lakes, or warehouses.
![](/data-engineering-specialization-website/images/0a3f8fc8-7b04-4f52-a49f-85e2f077be12.png)


**⚙️ Glue Jobs**

- ETL pipelines in AWS Glue are called **Glue jobs**.
- Three main ways to create and run Glue jobs:
- **🧼 AWS Glue DataBrew**:
  - No-code/low-code visual interface.
  - Transform and manipulate data like a spreadsheet, powered by Spark.
  - No Spark knowledge or coding required.
![](/data-engineering-specialization-website/images/ff19b07b-2a5e-41d9-8142-28e2cf9b41bb.png)

- **🧱 AWS Glue Studio**:
  - For more experienced users comfortable with Spark and ETL concepts.
  - Drag and drop UI for sources, transformations, and destinations.
  - Allows writing custom Spark code.
![](/data-engineering-specialization-website/images/08f6aa8e-de5d-45ed-add7-315c4c8514dc.png)

- **📓 Jupyter Notebooks**:
  - Write Spark code from scratch.
  - Run the code using AWS Glue.
  - Optionally get help from **Amazon Q Developer** or **Q chatbot**.
![](/data-engineering-specialization-website/images/d5eb27a1-9d63-43e2-98ae-10d89427a4af.png)

- Glue jobs can be orchestrated using **Glue triggers, blueprints, and workflows**.

**📚 Data Catalog and Governance**

- AWS Glue includes a **centralized data catalog** to manage metadata and enable governance.
- You've used **Glue Crawlers** to scan data sources and populate the catalog.
- Catalog provides schema, data types, structure, and partitioning information.
- Essential for building data lakes and lake houses.

**☁️ Serverless and Scalable**

- AWS Glue is **serverless**—no infrastructure management required.
- Jobs scale with **Data Processing Units (DPUs)**, starting small and scaling as needed.

**🔗 Integrations**

- Glue Data Catalog integrates with other AWS services:
- **Amazon Athena**: run SQL queries over your data.
- **Amazon QuickSight**: build BI dashboards.
- **Amazon SageMaker**: build, train, and deploy ML models.
- And many more.
---


## 3.4.4 AWS Glue Visual ETL

**:glue_aws: AWS Glue Visual ETL**

- Low-code, no-code interface for designing ETL pipelines in AWS Glue Studio
- Generates PySpark glue_job.py script automatically from visual canvas
- Supports sources (e.g., RDS), transforms (e.g., SQL queries) and targets (e.g., S3)

**📋 Purpose**

- Ingest normalized data from relational sources (e.g., Amazon RDS)
- Apply transformations to model data into a star schema
- Load the transformed data into an Amazon S3 data lake
![](/data-engineering-specialization-website/images/7c1c27e4-db5f-4353-acc6-54b530b99847.png)


**📝 glue_job.py Walkthrough**

- **Imports**: awsglue packages and pyspark modules
- **Function definitions**: e.g., sparkSqlQuery for running SQL on DataFrames
- **Argument parsing**: getResolvedOptions for JOB_NAME, connections, database, S3 path
- **Context setup**: create SparkContext, GlueContext and initialize Glue job
- **ETL logic**:
- Extract: JDBC connection to source tables (customers, products, orders, etc.)
- Transform: series of SQL statements to build dimension tables (dim_customers, dim_products, dim_location) and fact table (fact_orders)
- Load: write DataFrames to S3 in Parquet format

**🚀 Visual ETL Walkthrough**

- **Open Glue Studio** on AWS Console and create a new Visual ETL job with blank canvas
![](/data-engineering-specialization-website/images/bfeb185e-23dd-4cc6-a010-3de4d9e196fa.png)

- **Configure sources**: click "+" → Sources tab → add MySQL source nodes (e.g., customer_source, product_source) and specify JDBC connections, table names, IAM role
![](/data-engineering-specialization-website/images/996df72b-2940-4c33-ab0a-628210926b27.png)

- **Define transforms**: click "+" → Transform tab → add SQL Query nodes for each dimension (dim_customers, dim_products, dim_location) and fact (fact_orders), paste or write SQL, set aliases and parent nodes
![](/data-engineering-specialization-website/images/1d59448b-7c64-45f3-8ecb-dcb28f3e0ab4.png)

- **Set targets**: click "+" → Target tab → add S3 target nodes (e.g., dim_customer_target, fact_order_target), choose Parquet format, point to S3 folders under processed_data
![](/data-engineering-specialization-website/images/d2bf5624-7b9c-4666-baff-4d3b901ab1ad.png)

- **Generate script**: switch to Script tab to preview the auto-generated glue_job.py
![](/data-engineering-specialization-website/images/6578b1a4-7008-4105-b41b-ea515aa3561f.png)

![](/data-engineering-specialization-website/images/d2bf5624-7b9c-4666-baff-4d3b901ab1ad.png)


**▶️ Running the Glue Job**

- **Job details**: configure number of workers (e.g., 2), timeout (e.g., 3 minutes), and IAM role
- **Save and run**: click Save, then Run job; monitor status until "Succeeded"
- **Verify output**: browse S3 processed_data folders to confirm parquet files for each dimension and fact table

**🔚 Summary**

- Visual ETL accelerates ETL development by auto-generating code from graphical pipelines
- You can still view and customize glue_job.py for deeper control
- Alternative approaches include manual scripting or notebooks, but Visual ETL offers a rapid, serverless, reusable workflow
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


**Extract data from source tables**
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


**Transform data to build a star schema**
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


**Load transformed data into S3**

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

**:spark_: PySpark - DataFrames vs. SQL**

- **Approaches for Data Transformation in PySpark**
- You can use either:
  - Spark SQL queries
  - Direct operations on Spark DataFrames using Python
  - You can combine Spark SQL and DataFrame operations to leverage the strengths of both
- **Choosing Between SQL and Python**
| **Aspect** | **Spark DataFrames (Python)** | **Spark SQL** |
| --- | --- | --- |
| **Syntax Style** | Programmatic (Python API) | Declarative (SQL queries) |
| **Performance** | Comparable to SQL for simple tasks | Comparable to Python for simple tasks |
| **Complex Transformations** | Easier to implement (e.g., transpose with `.T`) | Limited support; some tasks not straightforward |
| **Code Reusability** | High – supports modular, testable, and reusable code/libraries | Low – limited reusability for complex queries |
| **Maintainability** | Easier due to modular Python code structure | Harder with large, complex SQL queries |
| **Team Skill Dependence** | Better if team is proficient in Python | Better if team is proficient in SQL |
| **Normalization / Data Cleaning** | More concise and flexible | Possible, but often more verbose |
| **Library Support** | Easy to build and reuse custom Python functions/libraries | No native library mechanism for reuse |
| **Hybrid Use** | Can be combined with SQL for best of both | Can be combined with Python API for flexibility |
| **Use Case Suitability** | Preferred for complex logic and reusable components | Preferred for simple, declarative data manipulation |


**Spark vs. Pandas**

| **Aspect** | **Pandas** | **Spark** |
| --- | --- | --- |
| **Data Size** | Suitable for small datasets that fit entirely in memory | Designed for large datasets that exceed memory limits |
| **Execution Mode** | Runs on a single machine | Distributed computing across multiple nodes or cloud clusters |
| **Simplicity** | Simpler setup and syntax for small-scale tasks | More complex setup but scalable for big data |
| **Performance** | Fast for small data; limited by machine memory | Scales horizontally; better for large-scale data processing |
| **Use Case** | Ideal for prototyping, local data exploration, and lightweight tasks | Ideal for production-level, high-volume data pipelines |
| **Infrastructure Requirements** | No cluster management needed | Requires cluster setup (local or cloud) |
| **Overhead** | Low overhead | Higher overhead due to distributed nature |
| **Recommendation** | Use when simplicity and speed for small data are priorities | Use when scalability, fault tolerance, and distributed processing are needed |

- **Choosing the Right Tool for Batch Transformation**
- SQL: Simpler for straightforward tasks
- Python: More flexible and modular for complex logic
- Decision depends on:
  - Data size
  - Hardware specifications
  - Desired trade-offs in performance and maintainability


**Streaming Transformations**

