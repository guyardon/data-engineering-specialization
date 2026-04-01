---
title: "1.1 Introduction to Source Systems"
course: "Course 2: Source Systems, Data Ingestion and Pipelines"
courseSlug: "course-2-source-systems-data-ingestion-and-pipelines"
courseOrder: 2
week: "Week 1: Working with Source Systems"
weekSlug: "week-1-working-with-source-systems"
weekOrder: 1
order: 1
notionId: "18d969a7-aa01-80e1-8091-d2f8fc8a1024"
---

## 1.1.1 Different Types of Source Systems


**Types of Data**

- **Structured Data**: Organized in a table format (e.g., relational databases).
- **Semi-Structured Data**: Has some structure but is not tabular (e.g., JSON). May include nesting.
- **Unstructured Data**: Lacks predefined structure (e.g., images, videos, audio files).

**Data Sources**

- **Databases**
- Store data in an organized way.
- Follow a **transactional pattern**: CRUD (Create, Read, Update, Delete).
- Interacted with via **Database Management Systems (DBMS)**.
- Types:
  - **Relational Databases** (Tables with rows & columns).
  - **Non-Relational Databases (NoSQL)** (e.g., document stores, key-value stores).
- **Files**
- Common formats: `.txt, .png, .mp3, .mp4, .csv`, etc.
- Can be:
  - **Structured** (e.g., spreadsheets).
  - **Semi-Structured** (e.g., JSON).
  - **Unstructured** (e.g., audio, video, images).
- **Streaming Systems**
- Continuous flow of data from producers to consumers.
- Uses message queues/streaming platforms (e.g., **Amazon Kinesis, Kafka**).
---

## 1.1.2 Relational Databases


**Structure & Advantages**

- Comprised of multiple tables, reducing redundancy and improving data management.
- **One Big Table (OBT) Approach**:
- Stores everything in a single table for faster processing.
- Leads to data duplication and potential inconsistencies.

**Database Schema & Keys**

- **Schema**: Defines how tables are organized and related.
- **Primary Key**: Unique identifier for each row.
- **Foreign Key**: References a primary key from another table.
- **Columns**: Have names and data types (part of the schema).

**Data Normalization**

- Organizes data into separate tables to minimize redundancy and ensure integrity.

**Relational Database Management Systems (RDBMS)**

- Examples: **MySQL, PostgreSQL, SQL Server, Oracle Database**.
- Interact using **SQL** for:
- Cleaning
- Joining
- Aggregation
- Filtering
---

## 1.1.3 SQL Queries


**Common SQL Commands**

- **SELECT**: Retrieves data (e.g., `SELECT *` returns all rows/columns).
- **FROM**: Specifies the table.
- **JOIN**: Combines data from multiple tables based on common keys.
- **Inner Join**: Returns only matching rows.
- **Left/Right Join**: Includes all rows from one table, with missing values from the other.
- **Full Join**: Returns all rows from both tables.
- **WHERE**: Filters data based on conditions.
- **GROUP BY**: Groups data and applies aggregate functions (e.g., `COUNT(*)`).
- **ORDER BY**: Sorts data (add `DESC` for descending order).
- **LIMIT**: Restricts the number of rows returned.

**Other Commands for Data Manipulation**

- **CREATE**: Defines a new table.
- **DELETE**: Removes records.
- **INSERT INTO**: Adds new records.
- **UPDATE**: Modifies existing records.
---

## 1.1.4 NoSQL Databases


**Characteristics**

- Supports SQL or SQL-like queries.
- Uses non-tabular structures:
- **Key-Value Stores**
- **Document Stores**
- **Wide-Column Stores**
- **Graph Databases**
- No predefined schemas → More flexibility.
- **Horizontal Scaling**: Distributes data across multiple servers.
- **Eventual Consistency**: Updates propagate over time.

**Comparison with Relational Databases**

- **Eventual Consistency (NoSQL)** → Prioritizes speed & scalability.
- **Strong Consistency (Relational)** → Ensures all nodes have updated data before reading.
- **ACID Compliance**: Some NoSQL databases (e.g., **MongoDB**) support it.

**Common NoSQL Models**

- **Key-Value Databases** (e.g., caching user session data).
- **Document Databases** (e.g., storing JSON documents for content management, catalogs, sensor readings).
---

## 1.1.5 Database ACID Compliance


**OLTP Systems (Online Transaction Processing)**

- **Relational Databases**: ACID Compliant.
- **NoSQL Databases**: Not all are ACID compliant.

**ACID Principles**

- **Atomicity**: All or nothing (e.g., banking transactions).
- **Consistency**: Transactions maintain data integrity (e.g., inventory stock ≥ 0).
- **Isolation**: Concurrent transactions execute independently.
- **Durability**: Completed transactions remain permanent despite system failures.
These principles **ensure database reliability and a consistent view of data**.

---

## 1.1.6 Lab - Interacting with Amazon DynamoDB (NoSQL Database)


**Key Features**

- **Key-Value Model**
- **Schema-less**: Each item can have distinct attributes.
- **Primary Keys**:
- **Partition Key** (single key).
- **Composite Key** (Partition Key + Sort Key).
- **Nested Attributes**
- **Data Types**: String (S), Number (N), List (L), Boolean (BOOL).

**Boto3**

- Python package for interacting with AWS services.
---

## 1.1.7 Object Storage


**Concept**

- Stores files as **objects** (not hierarchical like file systems).
- Example: **Amazon S3**.
- Ideal for **semi-structured & unstructured data** (e.g., ML training data).

**Object Components**

- **UUID (Key)**: Unique identifier.
- **Metadata**: File properties (e.g., creation date, owner, version).
- **Immutable**: Objects cannot be modified—only replaced.

**Why Object Storage?**

- **Scalability**: Virtually unlimited storage.
- **Redundancy**: Data is replicated across multiple availability zones.
- **Cost-Effectiveness**: Cheaper than other storage options.
- **Used for Modern Architectures**: **Data Lakes, Data Lakehouses**.
---

## 1.1.8 Logs


**Definition**

- **Append-only sequence of records ordered by time**.
- Captures system events like:
- User activity
- Database updates
- Error logs

**Use Cases**

- **System Monitoring & Debugging**
- **Data Analysis & Automation**
- **Machine Learning Pipelines**
---

## 1.1.9 Streaming Systems


**Key Terminology**

- **Event**: A recorded occurrence or state change.
- **Message**: Data associated with an event.
- **Stream**: A sequence of messages.

**Components**

- **Event Collector**: Groups messages into batches for processing.
- **Streaming Broker/Event Router**: Routes messages from producer to consumer.
- **Message Queue**: Buffers messages (e.g., **Amazon SQS**, FIFO-based).
- **Streaming Platform**: Persistent message storage (e.g., **Kafka, Kinesis**).
- **Log**: Append-only sequence of events (enables replaying past events).


