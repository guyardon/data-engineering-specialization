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

Joins are one of the most time-consuming query operations. An **inner join** combines only the rows that share a matching key across both tables - rows without a match in the other table are excluded.

---

**Join Implementation Methods**

| Method                      | Complexity   | How it Works                                                                                                                             |
| --------------------------- | ------------ | ---------------------------------------------------------------------------------------------------------------------------------------- |
| **Nested Loop**             | O(n × m)     | For each row in the outer table, scan the entire inner table for matches. Simple but slow for large tables.                              |
| **Index-based Nested Loop** | O(n × log m) | For each row in the outer table, look up the join key in the inner table's B-Tree index. Much faster when an index exists.               |
| **Hash Join**               | O(n + m)     | Build a hash table from the smaller table, then probe it with each row from the larger table. Best for large equi-joins without indexes. |

---

**Reducing Join Overhead**

- **Normalize data** to minimize joins needed for analysis - use fact and dimension tables so common queries only need simple star-schema joins
- **One-big-table approach** - pre-join and denormalize into a single wide table that eliminates downstream joins entirely

---

**Row Explosion Pitfall**

A common issue with many-to-many relationships: an "order" maps to many "payments" and a "payment" maps to many "orders," producing a **Cartesian product** with far more rows than expected. The fix is to verify your join logic and, if needed, introduce a **mapping table** that correctly describes the relationship.

## 3.3.2 Aggregate Queries

Aggregations compute summary values over a column - `SUM`, `AVG`, `MAX`, `MIN`, `COUNT`.

```sql
-- Without index: full table scan O(n)
-- With B-Tree index on price: index scan O(log n)
SELECT MIN(price) FROM orders;
```

Adding `GROUP BY` returns one result per group instead of a single value for the whole table. Grouping can be done via sorting algorithms, hash functions, or indexes.

```sql
-- Returns the minimum price per country
SELECT country, MIN(price)
FROM orders
GROUP BY country;
```

For large datasets, aggregation queries run faster on **columnar storage** because only the relevant columns are transferred from disk to memory - not entire rows.

## 3.3.3 Amazon Redshift Performance

`Amazon Redshift` is built around three performance pillars:

| Pillar               | Description                                                                              |
| -------------------- | ---------------------------------------------------------------------------------------- |
| **Columnar storage** | Data stored column-wise on disk - OLAP queries read only the columns they need           |
| **MPP**              | Leader node distributes workload across compute node slices that process in parallel     |
| **Compression**      | Compressed data read into memory, decompressed on the fly - reduces I/O and memory usage |

---

**Distribution Styles**

Distribution style defines how data is divided across compute nodes. The goal is to balance workloads evenly while minimizing data movement during joins.

| Style  | Behavior                                          | Best For                                        |
| ------ | ------------------------------------------------- | ----------------------------------------------- |
| `AUTO` | Redshift picks the optimal style automatically    | Default - let Redshift decide                   |
| `EVEN` | Round-robin distribution across all slices        | Tables with no joins                            |
| `KEY`  | Rows with the same key value go to the same slice | Co-locating join partners for large fact tables |
| `ALL`  | Full copy on every node                           | Small dimension tables joined frequently        |

---

**Sort Keys**

Sort keys store data on disk in a defined order, helping the query optimizer skip irrelevant data blocks - analogous to how OLTP databases use indexes.

## 3.3.4 Additional Query Strategies

- **Leverage query caching** - frequently running complex queries is expensive. Many databases cache query results, reducing load and improving response times on repeated queries.

- **Prioritize readability** - readable SQL is less error-prone, simpler to debug, and easier to collaborate on. Use CTEs to break complex logic into named, reusable steps.

- **Vacuum to reduce table bloat** - over time, databases accumulate outdated blocks on disk, causing **table bloat** (data size on disk exceeds actual data size). This leads to slow queries, inaccurate execution plans, and inefficient indexes. `VACUUM` removes dead records and is critical for relational databases like `PostgreSQL` and `MySQL`.
