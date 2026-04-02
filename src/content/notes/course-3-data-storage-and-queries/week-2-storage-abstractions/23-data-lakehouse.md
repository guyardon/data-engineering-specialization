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

**Data Lakehouse**


---

**The Data Lakehouse Architecture**

The data lakehouse, first introduced by Databricks, merges the best of both worlds: the **flexibility and low-cost storage** of a data lake with the **superior query performance and robust data management** of a data warehouse — eliminating the need to maintain two separate systems.

![](/data-engineering-specialization-website/images/6723598f-36a0-49d5-8ab8-42fc838b68c0.png)

## 2.3.2 Data Lakehouse Implementation and Open Table Formats

**Data Lakehouse Implementation**

The lakehouse architecture is made possible by **open table formats** — specialized storage formats that add transactional capabilities to data stored in a lake. They enable record-level updates and deletes while supporting full **ACID** guarantees.

Leading open table formats:

- **Databricks Delta Lake**
- `Apache Iceberg`
- `Apache Hudi` (Hadoop Update Delete Incremental)

Key features shared across these formats:

- **Time travel and snapshots** — query data as it existed at any point in time
- **Schema and partition evolution** — modify schemas or partitioning strategies without breaking existing queries
- **Open source** — multiple query engines can access the same data

![](/data-engineering-specialization-website/images/dbe7a62c-4d96-4114-b7f4-ea87ace47d8c.png)

![](/data-engineering-specialization-website/images/834de967-2908-4d42-9d0c-fb535b1bc30d.png)
