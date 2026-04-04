---
title: "2.3 Data Lakehouse"
course: "Course 3: Data Storage and Queries"
courseSlug: "course-3-data-storage-and-queries"
courseOrder: 3
week: "Week 2: Storage Abstractions"
weekSlug: "week-2-storage-abstractions"
weekOrder: 2
order: 3
notionId: "1e3969a7-aa01-80c6-8d1b-d10f852165d0"
---

## 2.3.1 The Data Lakehouse Architecture

The data lakehouse, first introduced by Databricks, merges the best of both worlds: the **flexibility and low-cost storage** of a data lake with the **superior query performance and robust data management** of a data warehouse — eliminating the need to maintain two separate systems.

The key insight is that an **open table format** layer sits between the query engines and the raw storage, adding transactional capabilities and metadata management on top of cheap object storage.

<img src="/data-engineering-specialization-website/images/diagrams/lakehouse-architecture-dark.svg" alt="Data lakehouse architecture with query engines, open table format, and object storage layers" class="diagram diagram-dark" />
<img src="/data-engineering-specialization-website/images/diagrams/lakehouse-architecture.svg" alt="Data lakehouse architecture with query engines, open table format, and object storage layers" class="diagram diagram-light" />

## 2.3.2 Open Table Formats

The lakehouse architecture is made possible by **open table formats** — specialized storage formats that add transactional capabilities to data stored in a lake. They enable record-level updates and deletes while supporting full **ACID** guarantees.

| Format | Origin | Key Differentiator |
|---|---|---|
| `Delta Lake` | Databricks | Tight Spark integration, transaction log-based, most mature ecosystem |
| `Apache Iceberg` | Netflix | Engine-agnostic design, hidden partitioning, best multi-engine support |
| `Apache Hudi` | Uber | Optimized for incremental upserts and streaming ingestion |

---

**Shared Capabilities**

All three formats provide capabilities that were previously only available in traditional data warehouses:

- **ACID transactions** — concurrent reads and writes without data corruption, even at scale
- **Time travel and snapshots** — query data as it existed at any point in time, enabling auditing and rollback
- **Schema evolution** — add, drop, or rename columns without breaking existing queries or rewriting data
- **Partition evolution** — change partitioning strategies on existing tables without a full rewrite
- **Open source** — multiple query engines (Spark, Trino, Flink, Athena) can read and write the same data

---

**How Open Table Formats Work**

Under the hood, data remains stored as **Parquet** or **ORC** files on object storage. The table format adds a **metadata layer** — a set of manifest files and logs that track which data files belong to each table version. When a write occurs, new data files are created and the metadata is atomically updated to point to the new snapshot, enabling ACID semantics without locks on the underlying storage.
