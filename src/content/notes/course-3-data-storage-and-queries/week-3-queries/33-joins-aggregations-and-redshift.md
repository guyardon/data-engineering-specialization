---
title: "3.3 Joins, Aggregations, and Redshift"
course: "Course 3: Data Storage and Queries"
courseSlug: "course-3-data-storage-and-queries"
courseOrder: 3
week: "Week 3: Queries"
weekSlug: "week-3-queries"
weekOrder: 3
order: 3
notionId: "1e7969a7-aa01-80f3-9892-df23d918832b"
---

## 3.3.1 Joins and Join Methods

**The Join Statement**

Joins are one of the most time-consuming query operations. An inner join, for example, combines only the rows that share a matching key across both tables.

![](/data-engineering-specialization-website/images/9f861c1e-fd7b-4a70-a34e-e214962ff3a8.png)


---

**3 Common Methods for Implementing Join**

- **Nested Loop Join** — O(n * m). For each row in the outer table, scan the entire inner table for matching join keys. Simple but slow.
- **Index-based Nested Loop** — O(n log m). For each row in the outer table, look up the join key in the inner table's B-Tree index.
- **Hash Join** — O(n * num_buckets), where num_buckets << m. A hash function maps rows from both tables into buckets based on the join attribute, then matches are found within each bucket.

![](/data-engineering-specialization-website/images/fd73b6a9-7fa8-430a-8e9a-60186ad8f1d6.png)

To reduce join overhead in practice, you can either normalize data to minimize joins needed for analysis (e.g., using fact and dimension tables) or adopt a **one-big-table** approach that eliminates downstream joins entirely.

A common pitfall is **row explosion** from many-to-many relationships — for example, when an "order" maps to many "payments" and a "payment" maps to many "orders." The query returns far more rows than expected. The fix is to verify your query logic and, if needed, introduce a mapping table that correctly describes the relationship.

## 3.3.2 Aggregate Queries

**Aggregate Queries**

Aggregations compute summary values over a column — SUM, AVG, MAX, MIN, COUNT.

```sql
SELECT MIN(price) from orders

# can either do a full table scan O(n)

# or faster index-scan on b-tree if available O(log n)
```

Adding `GROUP BY` returns one result per group instead of a single value for the whole table. Grouping can be done via sorting algorithms, hash functions, or indexes.

```sql
SELECT MIN(price) from orders GROUP BY country
```

For large datasets, aggregation queries run faster on **columnar storage** because only the relevant columns are transferred from disk to memory — not every row.

## 3.3.3 Amazon Redshift and Cloud Data Warehouse

**Amazon Redshift and Cloud Data Warehouse**

Amazon Redshift is a cloud data warehouse built around three performance pillars:

- **Columnar storage** — data is stored column-wise on disk, making OLAP and analytical queries significantly faster
- **Massively Parallel Processing (MPP)** — a leader node parses requests, forms execution plans, and distributes workload across compute nodes. Each compute node is partitioned into slices, each using a portion of the node's memory and disk to process its share of data.
- **Data compression** — Redshift reads compressed data into memory and decompresses on the fly, freeing up memory and speeding queries

**Distribution Style** defines how data is divided across compute nodes. The goal is to balance workloads evenly while minimizing data movement:

- **AUTO** — Redshift picks the optimal style
- **EVEN** — round-robin distribution; best when no joins are needed
- **KEY** — rows distributed based on a specific column; co-locates join partners
- **ALL** — full table copy on every node; useful for frequently joined small dimension tables

**Sort Key** stores data on disk in a defined order, helping the query optimizer reduce the amount of data scanned — analogous to how OLTP databases use indexes.

## 3.3.4 Additional Query Strategies

**Additional Query Strategy**

- **Leverage Query Caching** — frequently running complex queries is expensive. Many databases cache query results, reducing load and improving response times.
- **Prioritize Readability** — readable SQL is less error-prone, simpler to debug, and easier to collaborate on. Use CTEs to break complex logic into named, reusable steps.
- **Vacuuming to Reduce Table Bloat** — over time, databases accumulate outdated blocks on disk, causing **table bloat** (data size on disk exceeds actual data size). This leads to slow queries, inaccurate execution plans, and inefficient indexes. **Vacuuming** removes dead records and is critical for relational databases like PostgreSQL and MySQL.
