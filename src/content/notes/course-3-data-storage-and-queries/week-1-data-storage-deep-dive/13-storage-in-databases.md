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

**Introduction**

A database management system sits between your application and the raw storage hardware. Understanding its architecture helps explain why different databases perform differently.


---

**Database Management System (DBMS)**

The DBMS is the software layer that manages both relational and non-relational databases (such as graph databases). Its architecture consists of four main components:

- **Transport system** — handles client connections
- **Query processor** — parses and optimizes queries
- **Execution engine** — runs the query plan
- **Storage engine** — manages how data is serialized, arranged on disk, and indexed. An **index** is a data structure that lets you locate data in O(log n) time via binary search instead of scanning all rows in O(n). Modern storage engines are optimized for SSDs, handle modern data types, and offer columnar support for analytical workloads.


---

**In-Memory Storage Systems**

In-memory stores trade durability for speed — they are fast and low-latency, but volatile. Common use cases include caching, real-time applications, and gaming.

- **Memcached** — a key-value store for caching database query results or API calls; acceptable when data loss is tolerable.
- `Redis` — a key-value store supporting richer data types; suited for high-performance applications that can tolerate minor data loss.

## 1.3.2 Row vs. Column Storage

**Row vs. Column Storage**

The way data is physically arranged on disk has a dramatic impact on query performance.

**Row-oriented storage** stores each row as a consecutive sequence of bytes. This layout is ideal for **OLTP** workloads where you frequently read or write entire rows with low latency. However, it is inefficient for analytical queries that only need a single column — the system must still scan every column across every row.

Consider a table with 1 million rows, 30 columns, and 100 bytes per entry at a 200 MB/s transfer speed. A simple `SELECT SUM(price)` query would need to load the entire table:

```sql
SELECT SUM(price)
FROM my_table
```

That is 1M x 30 x 100 bytes = 3,000 MB, taking about 15 seconds. At 1 billion rows, row storage would take over 4 hours — clearly not scalable.

**Column-oriented storage** stores each column contiguously. For the same billion-row query, only the single `price` column needs to be read: 1B x 100 bytes = 100,000 MB, which takes roughly 8.3 minutes. Column storage is excellent for **OLAP** analytical queries but terrible for transactional workloads that touch entire rows.
