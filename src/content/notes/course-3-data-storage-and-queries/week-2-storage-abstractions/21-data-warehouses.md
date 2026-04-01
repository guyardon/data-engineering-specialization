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


## 2.1.1 Storage Hierarchy Overview

**Overview**

This week covers three storage abstractions, each building on the last:

1. **Data Warehouse** — the classic analytical store, now available as cloud-managed services
2. **Data Lake** — a central repository that supports growing, schema-flexible storage needs
3. **Data Lakehouse** — combines the strengths of warehouses and lakes into a single architecture


## 2.1.2 Data Warehouse Concepts

**Data Warehouse**

Bill Inmon's Definition: *A subject-oriented, integrated, nonvolatile, time-variant collection of data in support of management's decisions*

**Key Structural Ideas**

![](/data-engineering-specialization-website/images/268e8614-3a97-4dbc-a597-a2597669658f.png)

![](/data-engineering-specialization-website/images/50173c33-ecf9-40ad-aa15-75767d7f6b8f.png)

![](/data-engineering-specialization-website/images/bf8e7e01-ed44-427d-ae38-18c236e36ff8.png)

## 2.1.3 Modern Cloud Data Warehouses and Redshift

**Modern Cloud Data Warehouses**

Modern cloud data warehouses implement **MPP** (massively parallel processing) and can scale clusters dynamically based on workload. Examples include **Amazon Redshift**, **Google BigQuery**, and **Snowflake**.

Key characteristics:

- **ELT pattern** — raw data is loaded into a staging area first, then transformed in place to leverage MPP compute
- **Columnar storage** — optimized for high-performance analytical queries
- **Separation of compute and storage** — allows independent scaling to optimize cost and performance
- Like traditional warehouses, they store highly structured data modeled to support analytical queries

**Amazon Redshift MPP Architecture**

![](/data-engineering-specialization-website/images/56684670-af20-488d-8f51-83a88163bbf4.png)

![](/data-engineering-specialization-website/images/c17213d6-8e0f-406b-86ff-780be90634c2.png)

When a client application sends a query, the **leader node** creates an execution plan, compiles the code, and distributes it to the appropriate compute node slices that hold data relevant to the query.
