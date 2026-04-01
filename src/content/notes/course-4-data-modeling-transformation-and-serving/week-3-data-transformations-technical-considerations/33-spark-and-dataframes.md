---
title: "3.3 Spark and DataFrames"
course: "Course 4: Data Modeling, Transformation, and Serving"
courseSlug: "course-4-data-modeling-transformation-and-serving"
courseOrder: 4
week: "Week 3: Data Transformations & Technical Considerations"
weekSlug: "week-3-data-transformations-technical-considerations"
weekOrder: 3
order: 3
notionId: "1fc969a7-aa01-805e-8f9a-f648e027b479"
---


## 3.3.1 Spark Overview and Architecture

**Distributed Processing Framework - Spark**

Apache Spark started at UC Berkeley in 2009 to address MapReduce's shortcomings -- primarily by storing intermediate results in memory and enabling interactive data processing. Modern Spark includes stream processing, ML/graphing libraries, and a continuously expanding feature set.

![](/data-engineering-specialization-website/images/f02da27a-5058-4a43-b2f9-b83ef90d1d36.png)

![](/data-engineering-specialization-website/images/949d3939-649e-4c8d-b083-7ade222eff53.png)


**Spark Application Architecture**

A Spark application runs on a cluster of nodes with three roles:

- **Driver Node** -- The central controller of the Spark application
- **Cluster Manager Node** -- Allocates and manages memory resources across the cluster
- **Worker Nodes** -- Each contains a **Spark Executor** that runs tasks assigned by the driver

**Spark Partitioning Scheme**

Spark breaks data into partitions when loading from disk, allocates partitions to executors based on network proximity, and assigns one partition per CPU core.

**Writing a Spark Application**

The **SparkSession** object is the single unified entry point to all Spark functionality -- defining DataFrames, reading data sources, and running SQL queries. The Driver Node translates instructions (Python, Scala, etc.) into **Spark Jobs**, which execute sequentially by priority. Each job compiles into a DAG of **stages**, and each stage contains **tasks** that run in parallel. Stages with shared dependencies run serially; those with independent dependencies run in parallel.

![](/data-engineering-specialization-website/images/ff665232-a359-4af1-8f32-2a5ed35ba338.png)

![](/data-engineering-specialization-website/images/0b9f86c6-eb83-432e-adee-d85d9afbfdbf.png)


## 3.3.2 Spark DataFrames and Core Concepts

**Spark DataFrames Overview**

Spark DataFrames provide a high-level abstraction for working with large, distributed tabular datasets, hiding the complexity of distributed computation. They are built on top of **RDDs** (Resilient Distributed Datasets).

**Spark DataFrames vs RDDs**

RDDs are low-level and require manual optimization. DataFrames offer an expressive API (`filter`, `select`, `groupBy`) with automatic optimization. Both are immutable and fault-tolerant.

**Transformations vs Actions**

- **Transformations** (`select`, `filter`, `join`, `groupBy`) are lazily evaluated and return new DataFrames without modifying originals.
- **Actions** (`count`, `show`, `save`) trigger the actual execution of queued transformations.

**Key Spark Concepts**

- **Immutability** -- Original data is never modified
- **Lineage** -- A record of transformations enables fault recovery
- **Lazy Evaluation** -- Defers computation to optimize the execution plan


## 3.3.3 Basic PySpark DataFrame Operations

**Basic PySpark DataFrame Operations**

This section covers fundamental operations for working with Spark DataFrames: creation, manipulation, cleaning, aggregation, and user-defined functions (UDFs).

---


**Installation**

To install the required packages locally:

```bash
pip install pyspark findspark
```

Initialize `findspark` so that Spark can be found at runtime:

```python
import findspark
findspark.init()

import pyspark
```

---


**Create a Spark Session**

```python
from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("example").getOrCreate()

```

---


**Creating DataFrames**

**Manually:**

```python
from pyspark.sql.types import StructType, StructField, LongType, IntegerType, DoubleType, StringType


**Define data**
data = [
    (100, 1, 1, 50.1, 1, "Thingamjig", 5, "Joe Reis"),
    (100, 2, 2, 25.08, 2, "Whatchamacallit", 5, "Joe Reis"),
    (101, 1, 3, 75.23, 1, "Whoozeewhatzit", 7, "Matt Housley")
]


**Define schema using StructType**
schema = StructType([
    StructField("OrderID", LongType(), True),
    StructField("ItemNumber", IntegerType(), True),
    StructField("SKU", IntegerType(), True),
    StructField("Price", DoubleType(), True),
    StructField("Quantity", IntegerType(), True),
    StructField("Name", StringType(), True),
    StructField("CustomerID", LongType(), True),
    StructField("CustomerName", StringType(), True)
])


**Create DataFrame**
orders_df = spark.createDataFrame(data, schema)


**Show DataFrame**
orders_df.show()

```

**From CSV:**

```python
transactions_df = spark.read.csv("transactions.csv", header=True)
transactions_df.show(5)
```

---


**Selecting and Summarizing Columns**

```python
print(transactions_df.columns)
transactions_df.select("price", "quantity", "country").show(5)
transactions_df.select("price", "quantity", "country").describe().show(5)

```

---


**Manipulating DataFrames**

**Add a new column / Modify an existing column:**

```python
from pyspark.sql.functions import col


**spark dataframes are immutible so this creates a new dataframe**
transactions_df = transactions_df.withColumn(column_name="amount", col=transactions_df.price * transactions_df.quantity)
transactions_df.show()

```

**Rename a column:**

```python
transactions_df = transactions_df.withColumnRenamed(existing="invoice", new="id")

```

**Drop a column:**

```python
transactions_df = transactions_df.drop("description")

```

---


**Data Cleaning**

**Remove nulls:**

```python
transactions_df = transactions_df.dropna()

```

**Filter rows (e.g., quantity > 0):**

```python
transactions_df = transactions_df.filter(transactions_df.quantity > 0)

```

---


**Aggregation**

**Total amount per order ID:**

```python
transactions_df.groupBy("id").sum("amount").show()

```

**Count per country (descending):**

```python
transactions_df.groupBy("country").count().orderBy("count", ascending=False).show()

```

---


**User-Defined Functions (UDFs)**

**Using a UDF to convert to uppercase:**

```python
from pyspark.sql.functions import udf
from pyspark.sql.types import StringType

def toUpper(s: str):
    return s.upper()

udf_to_upper = udf(toUpper, StringType())
transactions_df.select("id", udf_to_upper("country")).show(n=5)

```

**Alternative with decorator:**

```python
from pyspark.sql.functions import udf

@udf(StringType())
def toUpper(s):
    return s.upper()

transactions_df = transactions_df.withColumn("country", toUpper("country"))

```

**Performance Note:** Python UDFs are less efficient due to serialization overhead between the JVM and Python. For optimal performance, consider writing UDFs in Scala or Java and registering them for use in Python.
