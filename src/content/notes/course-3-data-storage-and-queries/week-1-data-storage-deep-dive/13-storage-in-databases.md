---
title: "1.3 Storage in Databases"
course: "Course 3: Data Storage and Queries"
courseSlug: "course-3-data-storage-and-queries"
courseOrder: 3
week: "Week 1: Data Storage Deep Dive"
weekSlug: "week-1-data-storage-deep-dive"
weekOrder: 1
order: 3
notionId: "1de969a7-aa01-8031-b2e1-cef9c6db8b8d"
---

## 1.3.1 Database Management Systems

A **database management system (DBMS)** is the software layer that sits between your application and the raw storage hardware. It manages both relational and non-relational databases (such as graph databases). Understanding its architecture helps explain why different databases perform differently.

**DBMS Architecture**

| Component            | Role                                                          |
| -------------------- | ------------------------------------------------------------- |
| **Transport system** | Handles client connections and network communication          |
| **Query processor**  | Parses SQL/query language and optimizes the execution plan    |
| **Execution engine** | Runs the optimized query plan against the storage layer       |
| **Storage engine**   | Manages how data is serialized, arranged on disk, and indexed |

The **storage engine** is the most relevant component for understanding performance tradeoffs.

<img src="/data-engineering-specialization/images/diagrams/dbms-architecture-dark.svg" alt="DBMS architecture layers from client to disk" class="diagram diagram-dark" style="max-height: 900px;" />
<img src="/data-engineering-specialization/images/diagrams/dbms-architecture.svg" alt="DBMS architecture layers from client to disk" class="diagram diagram-light" style="max-height: 900px;" /> An **index** is a data structure that locates data in O(log n) time via binary search, instead of scanning all rows in O(n). Modern storage engines are optimized for SSDs, handle complex data types, and offer columnar support for analytical workloads.

---

**In-Memory Storage Systems**

In-memory stores trade durability for speed -- they are fast and low-latency, but volatile. Common use cases include caching, real-time applications, and gaming.

| System        | Type            | Use case                                                                                          |
| ------------- | --------------- | ------------------------------------------------------------------------------------------------- |
| **Memcached** | Key-value store | Caching database query results or API responses. Acceptable when data loss is tolerable.          |
| `Redis`       | Key-value store | Richer data types (lists, sets, hashes). High-performance apps that can tolerate minor data loss. |

<div class="tech-logos">
  <div class="tech-logo">
    <img src="/data-engineering-specialization/images/logos/memcached.svg" alt="Memcached" class="logo-light" /><img src="/data-engineering-specialization/images/logos/memcached-dark.svg" alt="Memcached" class="logo-dark" />
  </div>
  <div class="tech-logo">
    <img src="/data-engineering-specialization/images/logos/redis.svg" alt="Redis" class="logo-light" /><img src="/data-engineering-specialization/images/logos/redis-dark.svg" alt="Redis" class="logo-dark" />
  </div>
</div>

## 1.3.2 Row vs. Column Storage

The way data is physically arranged on disk has a dramatic impact on query performance.

**Row-oriented storage** writes each row as a contiguous sequence of bytes. This layout is ideal for **OLTP** workloads where you frequently read or write entire rows with low latency. However, it is inefficient for analytical queries that only need a subset of columns -- the system must still scan every column across every row.

**Column-oriented storage** writes each column contiguously. This is ideal for **OLAP** analytical queries that aggregate a single column across millions of rows, but inefficient for transactional workloads that read/write entire rows.

---

**Performance Example**

Consider a table with 1 billion rows, 30 columns, 100 bytes per entry, and a 200 MB/s disk transfer speed:

```sql
-- how long does this take with row vs. column storage?
SELECT SUM(price) FROM my_table
```

| Storage type        | Data read                | Calculation                        | Time         |
| ------------------- | ------------------------ | ---------------------------------- | ------------ |
| **Row-oriented**    | All 30 columns, all rows | 1B × 30 × 100 bytes = 3,000,000 MB | ~4.2 hours   |
| **Column-oriented** | Only the `price` column  | 1B × 100 bytes = 100,000 MB        | ~8.3 minutes |

|                   | Row-Oriented                     | Column-Oriented                             |
| ----------------- | -------------------------------- | ------------------------------------------- |
| **Optimized for** | OLTP (transactional)             | OLAP (analytical)                           |
| **Read pattern**  | Full rows at a time              | Individual columns at a time                |
| **Write pattern** | Append entire rows efficiently   | Must write to each column file separately   |
| **Best when**     | Reading/writing complete records | Aggregating single columns across many rows |
| **Examples**      | `PostgreSQL`, `MySQL`            | `Redshift`, `BigQuery`, `Snowflake`         |

<div class="tech-logos">
  <div class="tech-logo">
    <img src="/data-engineering-specialization/images/logos/postgresql.svg" alt="PostgreSQL" class="logo-light" /><img src="/data-engineering-specialization/images/logos/postgresql-dark.svg" alt="PostgreSQL" class="logo-dark" />
    <span>PostgreSQL</span>
  </div>
  <div class="tech-logo">
    <img src="/data-engineering-specialization/images/logos/mysql.svg" alt="MySQL" class="logo-light" /><img src="/data-engineering-specialization/images/logos/mysql-dark.svg" alt="MySQL" class="logo-dark" />
    <span>MySQL</span>
  </div>
  <div class="tech-logo">
    <img src="/data-engineering-specialization/images/logos/redshift.svg" alt="Amazon Redshift" class="logo-light" /><img src="/data-engineering-specialization/images/logos/redshift-dark.svg" alt="Amazon Redshift" class="logo-dark" />
    <span>Redshift</span>
  </div>
  <div class="tech-logo">
    <img src="/data-engineering-specialization/images/logos/bigquery.svg" alt="Google BigQuery" class="logo-light" /><img src="/data-engineering-specialization/images/logos/bigquery-dark.svg" alt="Google BigQuery" class="logo-dark" />
    <span>BigQuery</span>
  </div>
  <div class="tech-logo">
    <img src="/data-engineering-specialization/images/logos/snowflake.svg" alt="Snowflake" class="logo-light" /><img src="/data-engineering-specialization/images/logos/snowflake-dark.svg" alt="Snowflake" class="logo-dark" />
    <span>Snowflake</span>
  </div>
</div>
