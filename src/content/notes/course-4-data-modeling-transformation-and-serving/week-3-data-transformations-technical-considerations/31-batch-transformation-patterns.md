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

| Factor | Batch | Streaming |
|---|---|---|
| **Primary constraint** | Data size, hardware specs, performance requirements | Latency requirements |
| **Approach** | Single machine or distributed processing framework | Event-driven or micro-batch |
| **Logic** | SQL or Python | SQL, Python, or framework-specific APIs |

## 3.1.2 ETL Patterns and Use Cases

**ETL vs. ELT vs. EtLT**

| Pattern | How it Works | Best For |
|---|---|---|
| **ETL** | Transform data *before* loading into the target | Legacy warehouses, limited target compute |
| **ELT** | Load raw data first, then transform *inside* the target | Cloud warehouses with strong compute (Redshift, BigQuery) |
| **EtLT** | Light transforms before load (cleaning), heavy transforms after (modeling) | Hybrid — clean early, model late |

---

**Transformations for Data Modeling**

Convert normalized source data into analytical models — star schemas, data vaults, one-big-table — optimized for downstream queries.

---

**Transformations for Data Cleaning (Wrangling)**

| Operation | Example |
|---|---|
| **Deduplication** | Remove duplicate records |
| **Type casting** | Convert string dates to date types |
| **Null handling** | Impute or drop missing values |
| **Standardization** | Normalize formats (phone numbers, addresses) |
| **Filtering** | Remove invalid or irrelevant rows |
| **Validation** | Assert business rules (e.g., price > 0) |

## 3.1.3 Data Updating and Change Data Capture

A common use case is keeping the data warehouse in sync with source systems.

---

**Truncate and Reload**

Delete all records in the target and reload from source. Works for small datasets or infrequent updates, but becomes expensive at scale.

---

**Change Data Capture (CDC)**

CDC identifies changes in the source system and applies only those changes to the target. Changes can be detected through a `last_updated` column or database transaction logs (`I` for insert, `U` for update, `D` for delete).

| Strategy | Behavior |
|---|---|
| **Insert-only** | Append new records without modifying old ones — new records include metadata to distinguish versions |
| **Upsert / Merge** | Match by primary key — update on match, insert on no match |

---

**Handling Deletes**

| Method | Description |
|---|---|
| **Hard delete** | Permanently remove the record — for performance or compliance |
| **Soft delete** | Mark the record as deleted with a flag column |
| **Insert-only with delete flag** | Append a new record with a deletion marker |

---

**Insert Performance**

**Single-row inserts** work well for row-oriented OLTP databases but are inefficient for column-oriented OLAP systems — they create massive load and degrade read performance. **Micro-batch or batch inserts** are the preferred approach for OLAP.
