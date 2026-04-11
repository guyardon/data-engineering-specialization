---
title: "3.1 Batch Transformation Patterns"
course: "Course 4: Data Modeling, Transformation, and Serving"
courseSlug: "course-4-data-modeling-transformation-and-serving"
courseOrder: 4
week: "Week 3: Data Transformations & Technical Considerations"
weekSlug: "week-3-data-transformations-technical-considerations"
weekOrder: 3
order: 1
notionId: "1fc969a7-aa01-805e-8f9a-f648e027b479"
---

## 3.1.1 Batch Transformation Overview

The **transformation stage** is where raw data is manipulated and enhanced for downstream stakeholders. Transformations serve three purposes:

1. **Manipulate and enhance data** for downstream consumers
2. **Leverage massively parallel processing** for data modeling (star schemas, data vaults, etc.)
3. **Define zones** for stages of transformed data (raw, cleaned, enriched)

---

**Technical Considerations**

| Factor                 | Batch                                               | Streaming                               |
| ---------------------- | --------------------------------------------------- | --------------------------------------- |
| **Primary constraint** | Data size, hardware specs, performance requirements | Latency requirements                    |
| **Approach**           | Single machine or distributed processing framework  | Event-driven or micro-batch             |
| **Logic**              | SQL or Python                                       | SQL, Python, or framework-specific APIs |

## 3.1.2 ETL Patterns and Use Cases

**ETL vs. ELT vs. EtLT**

| Pattern  | How it Works                                                               | Best For                                                  |
| -------- | -------------------------------------------------------------------------- | --------------------------------------------------------- |
| **ETL**  | Transform data _before_ loading into the target                            | Legacy warehouses, limited target compute                 |
| **ELT**  | Load raw data first, then transform _inside_ the target                    | Cloud warehouses with strong compute (Redshift, BigQuery) |
| **EtLT** | Light transforms before load (cleaning), heavy transforms after (modeling) | Hybrid - clean early, model late                          |

---

**Transformations for Data Modeling**

Convert normalized source data into analytical models - star schemas, data vaults, one-big-table - optimized for downstream queries.

---

**Transformations for Data Cleaning (Wrangling)**

| Operation           | Example                                      |
| ------------------- | -------------------------------------------- |
| **Deduplication**   | Remove duplicate records                     |
| **Type casting**    | Convert string dates to date types           |
| **Null handling**   | Impute or drop missing values                |
| **Standardization** | Normalize formats (phone numbers, addresses) |
| **Filtering**       | Remove invalid or irrelevant rows            |
| **Validation**      | Assert business rules (e.g., price > 0)      |

## 3.1.3 Data Updating and Change Data Capture

A common use case is keeping the data warehouse in sync with source systems.

---

**Truncate and Reload**

Delete all records in the target and reload from source. Works for small datasets or infrequent updates, but becomes expensive at scale.

---

**Change Data Capture (CDC)**

CDC identifies changes in the source system and applies only those changes to the target. Changes can be detected through a `last_updated` column or database transaction logs (`I` for insert, `U` for update, `D` for delete).

| Strategy           | Behavior                                                                                             |
| ------------------ | ---------------------------------------------------------------------------------------------------- |
| **Insert-only**    | Append new records without modifying old ones - new records include metadata to distinguish versions |
| **Upsert / Merge** | Match by primary key - update on match, insert on no match                                           |

---

**Handling Deletes**

| Method                           | Description                                                   |
| -------------------------------- | ------------------------------------------------------------- |
| **Hard delete**                  | Permanently remove the record - for performance or compliance |
| **Soft delete**                  | Mark the record as deleted with a flag column                 |
| **Insert-only with delete flag** | Append a new record with a deletion marker                    |

---

**Insert Performance**

**Single-row inserts** work well for row-oriented OLTP databases but are inefficient for column-oriented OLAP systems - they create massive load and degrade read performance. **Micro-batch or batch inserts** are the preferred approach for OLAP.

## 3.1.4 Idempotency in Batch Pipelines

An **idempotent** pipeline produces the same result whether it runs once or multiple times with the same input. Idempotency is one of the most important reliability properties in data engineering - it means you can safely retry a failed run without creating duplicates, corrupting data, or producing inconsistent results.

---

**Why It Matters**

Pipelines fail for countless reasons: network timeouts, cloud service outages, schema changes, resource limits. When a pipeline fails partway through, the recovery question is critical. Without idempotency, engineers must manually inspect what succeeded and what didn't before deciding whether to rerun. With idempotency, the answer is always: just rerun the whole thing.

---

**Common Patterns for Achieving Idempotency**

| Pattern                        | How It Works                                                                                                    | Tradeoff                                                                            |
| ------------------------------ | --------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------- |
| **Truncate and reload**        | Delete all data in the target partition, then write fresh                                                       | Simple and reliable, but expensive for large datasets                               |
| **Upsert (MERGE)**             | Insert new rows, update existing ones based on a key                                                            | Efficient for incremental loads, but requires a reliable unique key                 |
| **Deterministic output paths** | Write to a path derived from the input (e.g., `/output/date=2025-03-15/`) so reruns overwrite the same location | Works well with object storage, relies on consistent naming                         |
| **Deduplication on read**      | Accept potential duplicates at write time, deduplicate downstream using `ROW_NUMBER()` or `QUALIFY`             | Shifts complexity to the consumer, but decouples write reliability from correctness |

---

**Anti-patterns to Avoid**

- **Appending without deduplication** - rerunning a pipeline that appends to a table without checking for existing records creates duplicates with every retry
- **Using wall-clock timestamps as keys** - if a pipeline reruns, the timestamp changes, making it impossible to detect duplicate records
- **Non-deterministic file names** - writing to randomly named files means reruns create new files instead of overwriting previous attempts
