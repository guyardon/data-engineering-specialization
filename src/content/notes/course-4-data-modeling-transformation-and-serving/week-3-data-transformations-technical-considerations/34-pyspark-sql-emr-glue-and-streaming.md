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

PySpark supports three approaches to data transformation: SQL-based manipulation, Python-based DataFrame operations, and a hybrid of both. All approaches run on the **same computation engine** and compile to the **same low-level code**.

---

**Temporary Views**

A **temporary view** is a virtual table that exists only while the Spark session is active. It lets you write SQL queries against a DataFrame without physically storing data.

```python
# Register DataFrame as a temporary SQL view
transactions_df.createOrReplaceTempView("orders")

# Query using SQL syntax — returns a DataFrame
spark.sql("SELECT * FROM orders").show()
```

---

**SQL Queries**

```python
# Aggregate: total amount per order
spark.sql("""
    SELECT ID, SUM(Amount) AS total
    FROM orders
    GROUP BY ID
    ORDER BY total DESC
""").show()
```

---

**UDFs in SQL**

SQL queries cannot use raw Python functions directly — register them with Spark first:

```python
def to_lower(word):
    return word.lower()

# Register for use in SQL
spark.udf.register("udf_to_lower", to_lower)
spark.sql("SELECT DISTINCT udf_to_lower(Country) FROM orders").show()
```

---

**Joining Multiple Views**

```python
# Register a second DataFrame as a view
product_category_df.createOrReplaceTempView("items")

# Join views using standard SQL
spark.sql("""
    SELECT items.Category, AVG(orders.Amount) AS avg_amount
    FROM items
    LEFT JOIN orders ON items.ItemID = orders.StockCode
    GROUP BY items.Category
""").show()
```

## 3.4.2 Amazon EMR

`Amazon EMR` is AWS's managed big data platform for scalable, distributed computing.

| Feature | Description |
|---|---|
| **Frameworks** | `Apache Spark`, `Hadoop`, `Hive`, `Presto`, `Flink`, `HBase` |
| **Integration** | Native with `S3`, `DynamoDB`, `RDS`, `Redshift` |
| **Storage** | Decouples compute from storage via `S3` — multiple clusters can process the same data |
| **Scaling** | Clusters scale elastically based on workload |

---

**EMR Studio and Serverless**

| Variant | Description |
|---|---|
| **EMR Studio** | Browser-based IDE (built on Jupyter) for interactive analysis and job execution |
| **EMR Serverless** | Eliminates manual cluster management — automatic scaling, pay only for what you use |

A typical workflow: create an EMR Serverless application with default Spark settings, launch an EMR Studio workspace, attach it to the application, choose the PySpark kernel, and run Spark jobs interactively.

## 3.4.3 AWS Glue

`AWS Glue` is a **serverless data integration service** for ingesting, transforming, and loading data. It uses `Apache Spark` under the hood and supports data from databases, object stores (`S3`), logs, APIs, and streaming platforms.

---

**Glue Jobs**

ETL pipelines in AWS Glue are called **Glue jobs**. Three ways to create them:

| Method | Skill Level | Description |
|---|---|---|
| **Glue DataBrew** | No-code | Visual spreadsheet-like interface for transforms, powered by Spark |
| **Glue Studio** | Low-code | Drag-and-drop UI for sources, transforms, and destinations with optional custom code |
| **Jupyter Notebooks** | Code | Write Spark code from scratch, run via Glue |

Glue jobs can be orchestrated using **Glue triggers, blueprints, and workflows**.

---

**Data Catalog and Governance**

`AWS Glue` includes a **centralized data catalog** for managing metadata and enabling governance. **Glue Crawlers** scan data sources to populate the catalog with schema, data types, structure, and partitioning information — essential for data lakes and lakehouses.

The Glue Data Catalog integrates with `Amazon Athena` (SQL queries), `Amazon QuickSight` (BI dashboards), and `Amazon SageMaker` (ML models).

## 3.4.4 AWS Glue Visual ETL

Glue Visual ETL is a low-code interface in `AWS Glue Studio` for designing ETL pipelines. It generates a PySpark `glue_job.py` script automatically from a visual canvas.

---

**Typical Workflow**

1. **Configure sources** — add source nodes (e.g., MySQL tables via JDBC) and specify connections
2. **Define transforms** — add SQL Query nodes for each dimension and fact table
3. **Set targets** — add `S3` target nodes with Parquet format
4. **Generate script** — preview and customize the auto-generated PySpark script
5. **Run and verify** — configure workers, run the job, monitor until succeeded

---

**Generated Glue Script Structure**

The auto-generated `glue_job.py` follows this pattern:

```python
import sys
from awsglue import DynamicFrame
from awsglue.context import GlueContext
from awsglue.job import Job
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext

def sparkSqlQuery(glueContext, query, mapping, transformation_ctx):
    """Run a SQL query against DynamicFrames registered as temp views."""
    for alias, frame in mapping.items():
        frame.toDF().createOrReplaceTempView(alias)
    result = spark.sql(query)
    return DynamicFrame.fromDF(result, glueContext, transformation_ctx)

# Parse job arguments and initialize context
args = getResolvedOptions(
    sys.argv, ["JOB_NAME", "glue_connection", "glue_database", "target_path"]
)
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args["JOB_NAME"], args)

# --- EXTRACT: read source tables via JDBC ---
customers = glueContext.create_dynamic_frame.from_options(
    connection_type="mysql",
    connection_options={
        "useConnectionProperties": "true",
        "dbtable": "classicmodels.customers",
        "connectionName": args["glue_connection"],
    },
    transformation_ctx="customers",
)

# --- TRANSFORM: build star schema with SQL ---
dim_customers = sparkSqlQuery(
    glueContext,
    query="""
        SELECT customerNumber, customerName,
               contactLastName, contactFirstName,
               phone, addressLine1, creditLimit
        FROM customers
    """,
    mapping={"customers": customers},
    transformation_ctx="dim_customers",
)

# --- LOAD: write to S3 as Parquet ---
sink = glueContext.getSink(
    path=f"{args['target_path']}/dim_customers/",
    connection_type="s3",
    updateBehavior="UPDATE_IN_DATABASE",
    compression="snappy",
    enableUpdateCatalog=True,
    transformation_ctx="dim_customers_to_s3",
)
sink.setCatalogInfo(
    catalogDatabase=args["glue_database"],
    catalogTableName="dim_customers",
)
sink.setFormat("glueparquet")
sink.writeFrame(dim_customers)

job.commit()
```

## 3.4.5 DataFrames vs. SQL and Streaming

**Choosing Between SQL and Python**

| Aspect | Spark DataFrames (Python) | Spark SQL |
|---|---|---|
| **Syntax** | Programmatic (Python API) | Declarative (SQL queries) |
| **Complex transforms** | Easier to implement (e.g., transpose, custom logic) | Limited for non-standard operations |
| **Reusability** | High — modular, testable, supports libraries | Low — limited reuse for complex queries |
| **Maintainability** | Easier with modular code structure | Harder with large, nested queries |
| **Best for** | Complex logic, reusable components | Simple, declarative data manipulation |

Both compile to the same execution plan — mix and match freely.

---

**Spark vs. Pandas**

| Aspect | Pandas | `Spark` |
|---|---|---|
| **Data size** | Fits in memory on a single machine | Exceeds memory — distributed across nodes |
| **Execution** | Single machine | Distributed cluster |
| **Setup** | Minimal | Requires cluster (local or cloud) |
| **Best for** | Prototyping, local exploration, lightweight tasks | Production pipelines, high-volume processing |

---

**Streaming Transformations**

For streaming, the key consideration is **latency requirements**:

- **Micro-batch** (e.g., Spark Structured Streaming) — processes small batches at regular intervals, trading a few seconds of latency for simpler semantics
- **True streaming** (e.g., `Apache Flink`) — processes events individually with millisecond latency, more complex but lower latency
