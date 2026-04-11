---
title: "2.1 Data Warehouses"
course: "Course 3: Data Storage and Queries"
courseSlug: "course-3-data-storage-and-queries"
courseOrder: 3
week: "Week 2: Storage Abstractions"
weekSlug: "week-2-storage-abstractions"
weekOrder: 2
order: 1
notionId: "1e3969a7-aa01-80c6-8d1b-d10f852165d0"
---

## 2.1.1 Storage Abstractions Overview

This week covers three storage abstractions, each building on the last:

| Abstraction        | Description                                                           | Key Idea                                         |
| ------------------ | --------------------------------------------------------------------- | ------------------------------------------------ |
| **Data Warehouse** | The classic analytical store, now available as cloud-managed services | Structured data, modeled for fast queries        |
| **Data Lake**      | A central repository for raw data at any scale                        | Schema-on-read, supports all data types          |
| **Data Lakehouse** | Combines warehouse query performance with lake flexibility            | Open table formats enable ACID on object storage |

## 2.1.2 Data Warehouse Concepts

Bill Inmon's definition: _"A subject-oriented, integrated, nonvolatile, time-variant collection of data in support of management's decisions."_

---

**Key Structural Properties**

| Property             | Meaning                                                                                                         |
| -------------------- | --------------------------------------------------------------------------------------------------------------- |
| **Subject-oriented** | Organized around business domains (sales, inventory, customers) rather than applications                        |
| **Integrated**       | Data from multiple source systems is cleaned, standardized, and consolidated into a single consistent format    |
| **Nonvolatile**      | Once loaded, data is not modified or deleted - historical records are preserved for auditing and trend analysis |
| **Time-variant**     | Every record carries a time dimension, enabling analysis across different time periods                          |

---

**How Data Flows Into a Warehouse**

Source systems (CRM, ERP, flat files) feed data through an **ETL** or **ELT** process. Inside the warehouse, data moves through a **staging area** (raw landing zone), gets modeled into **dimension and fact tables** (star or snowflake schema), and is then served to downstream consumers through **data marts** - subsets of the warehouse tailored to specific business units.

<img src="/data-engineering-specialization/images/diagrams/warehouse-architecture-dark.svg" alt="Data warehouse architecture showing ETL flow from sources through staging to modeled tables" class="diagram diagram-dark" style="max-height: 900px;" />
<img src="/data-engineering-specialization/images/diagrams/warehouse-architecture.svg" alt="Data warehouse architecture showing ETL flow from sources through staging to modeled tables" class="diagram diagram-light" style="max-height: 900px;" />

---

**Separation of Storage and Compute**

Traditional on-premise warehouses coupled storage and compute on the same hardware. Cloud warehouses decouple them - storage lives on cheap object storage (`S3`, GCS) while compute scales independently via on-demand clusters. This means you can store petabytes affordably and only pay for compute when queries are running.

## 2.1.3 Modern Cloud Data Warehouses and Redshift

Modern cloud data warehouses implement **MPP** (massively parallel processing) and can scale clusters dynamically based on workload.

| Warehouse         | Provider    | Key Differentiator                                     |
| ----------------- | ----------- | ------------------------------------------------------ |
| `Amazon Redshift` | AWS         | Deep AWS integration, Redshift Spectrum for S3 queries |
| `Google BigQuery` | GCP         | Serverless, automatic scaling, slot-based pricing      |
| `Snowflake`       | Multi-cloud | Virtual warehouses, time travel, data sharing          |

<div class="tech-logos">
  <div class="tech-logo">
    <img src="/data-engineering-specialization/images/logos/redshift.svg" alt="Amazon Redshift" class="logo-light" /><img src="/data-engineering-specialization/images/logos/redshift-dark.svg" alt="Amazon Redshift" class="logo-dark" />
    <span>Amazon Redshift</span>
  </div>
  <div class="tech-logo">
    <img src="/data-engineering-specialization/images/logos/bigquery.svg" alt="Google BigQuery" class="logo-light" /><img src="/data-engineering-specialization/images/logos/bigquery-dark.svg" alt="Google BigQuery" class="logo-dark" />
    <span>Google BigQuery</span>
  </div>
  <div class="tech-logo">
    <img src="/data-engineering-specialization/images/logos/snowflake.svg" alt="Snowflake" class="logo-light" /><img src="/data-engineering-specialization/images/logos/snowflake-dark.svg" alt="Snowflake" class="logo-dark" />
    <span>Snowflake</span>
  </div>
  <div class="tech-logo">
    <img src="/data-engineering-specialization/images/logos/databricks.svg" alt="Databricks" class="logo-light" /><img src="/data-engineering-specialization/images/logos/databricks-dark.svg" alt="Databricks" class="logo-dark" />
    <span>Databricks</span>
  </div>
</div>

**Common characteristics:**

- **ELT pattern** - raw data is loaded first, then transformed in place using MPP compute
- **Columnar storage** - optimized for analytical queries that scan specific columns across many rows
- **Separation of compute and storage** - allows independent scaling to optimize cost and performance
- **Highly structured data** - modeled to support analytical queries with predefined schemas

---

**Amazon Redshift MPP Architecture**

When a client application sends a query, the **leader node** parses it, creates an execution plan, compiles the code, and distributes it to the **compute nodes**. Each compute node is divided into **slices** - independent processing units that each hold a portion of the data. Slices execute query fragments in parallel, then the leader node aggregates the results and returns them to the client.

<img src="/data-engineering-specialization/images/diagrams/redshift-mpp-dark.svg" alt="Redshift MPP architecture with leader node distributing queries to compute node slices" class="diagram diagram-dark" style="max-height: 900px;" />
<img src="/data-engineering-specialization/images/diagrams/redshift-mpp.svg" alt="Redshift MPP architecture with leader node distributing queries to compute node slices" class="diagram diagram-light" style="max-height: 900px;" />

Key Redshift concepts:

- **Leader node** - receives client queries, builds execution plans, coordinates compute nodes, and aggregates final results
- **Compute nodes** - execute query fragments against their local data slices in parallel
- **Node slices** - each node is partitioned into slices based on CPU count; each slice gets its own memory and disk allocation
- **Distribution styles** - control how data is distributed across slices (`KEY`, `EVEN`, `ALL`) to minimize data movement during joins
