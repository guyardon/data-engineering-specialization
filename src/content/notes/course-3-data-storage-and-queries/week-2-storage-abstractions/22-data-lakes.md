---
title: "2.2 Data Lakes"
course: "Course 3: Data Storage and Queries"
courseSlug: "course-3-data-storage-and-queries"
courseOrder: 3
week: "Week 2: Storage Abstractions"
weekSlug: "week-2-storage-abstractions"
weekOrder: 2
order: 2
notionId: "1e3969a7-aa01-80c6-8d1b-d10f852165d0"
---

## 2.2.1 Data Lake Architecture

Semi-structured and unstructured data do not fit neatly into a fixed schema. Data lakes address this by providing a central repository for storing large volumes of data with no predefined schema or set of transformations. Instead, they use a **schema-on-read** pattern — structure is applied when data is queried, not when it is written.

| Property | Data Warehouse | Data Lake |
|---|---|---|
| **Schema** | Schema-on-write (defined before loading) | Schema-on-read (applied at query time) |
| **Data types** | Structured only | Structured, semi-structured, unstructured |
| **Storage cost** | Higher (optimized storage engines) | Lower (object storage like `S3`) |
| **Query performance** | Fast (pre-modeled, indexed) | Slower (no pre-optimization) |
| **Flexibility** | Low (rigid schema changes) | High (store anything, decide later) |

## 2.2.2 Data Lake 1.0 and Its Shortcomings

The first generation of data lakes combined storage technologies (`Hadoop HDFS`, `Amazon S3`) with processing engines (`Apache Pig`, `Presto`, `Hive`). While functional, they suffered from significant shortcomings:

- **Data swamp** — without proper data management, cataloging, or discovery tools, there was no guarantee of data integrity or quality
- **Write-only storage** — DML operations like deleting or updating rows required creating entirely new tables, making regulatory compliance painful
- **No schema management or data modeling** — data was not optimized for query operations like joins, making it difficult to process

Large companies like Facebook built custom tooling to work around these issues, but most organizations struggled to extract value from Data Lake 1.0.

## 2.2.3 Next-Generation Data Lakes

Next-generation data lakes introduced several key improvements:

| Improvement | Description |
|---|---|
| **Zones** | Data organized by processing stage — raw landing, cleaned/transformed, and curated/enriched zones with appropriate governance at each stage |
| **Data partitioning** | Datasets divided by criteria like time or location, allowing queries to scan only relevant partitions |
| **Data catalog** | Centralized metadata about each dataset — owner, source, partitions, schema, and schema evolution history |

<img src="/data-engineering-specialization-website/images/diagrams/data-lake-zones-dark.svg" alt="Data lake zone architecture with raw, cleaned, and curated zones" class="diagram diagram-dark" style="max-height: 900px;" />
<img src="/data-engineering-specialization-website/images/diagrams/data-lake-zones.svg" alt="Data lake zone architecture with raw, cleaned, and curated zones" class="diagram diagram-light" style="max-height: 900px;" />

---

**The Two-System Problem**

Even with these improvements, a fundamental limitation remained: organizations still needed both a data lake (for low-cost, high-volume storage) and a separate data warehouse (for high-performance analytical queries). Moving data between the two was expensive, introduced bugs and failures, and risked data quality, duplication, and consistency issues. This "two-system problem" motivated the next evolution — the **data lakehouse**.
