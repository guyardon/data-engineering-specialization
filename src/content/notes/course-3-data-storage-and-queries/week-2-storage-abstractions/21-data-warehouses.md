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

## Overview

**Storage Hierarchy**

1. **Data Warehouse**
1. Cloud data warehouse
2. **Data Lake**
1. Supports growing storage needs
3. **Data Lakehouse**
1. Combines the advantages of data warehouses and data lakes

### Data Warehouse

Bill Inman's Definition: *A subject-oriented, integrated, nonvolatile, time-variant collection of data in support of management's decisions*

**Key Structural Ideas**

![](/data-engineering-specialization-website/images/268e8614-3a97-4dbc-a597-a2597669658f.png)

![](/data-engineering-specialization-website/images/50173c33-ecf9-40ad-aa15-75767d7f6b8f.png)

![](/data-engineering-specialization-website/images/bf8e7e01-ed44-427d-ae38-18c236e36ff8.png)

**Modern Cloud Data Warehouses**

- Data warehouses typically implement MPP (massively parallel processing)
- In cloud data warehouses, clusters can be scaled dynamically based on needs
- Examples:
- Amazon Redshift
- Google Big Query
- Snowflake
- Support ELT (Extract-Load-Transform)
- Raw unprocessed data is loaded into a staging area within the data warehouse
- Then transformation is performed in staging area to leverage MPP
- Supports Columnar for high performance analytical storage
- Seperation of compute and storage to optimize cost and performance
- Similar to traditional data warehouses, stores data that is highly structured, and models data in a way that supports analytical queries

**Amazon Redshift MPP Architecture**

![](/data-engineering-specialization-website/images/56684670-af20-488d-8f51-83a88163bbf4.png)

![](/data-engineering-specialization-website/images/c17213d6-8e0f-406b-86ff-780be90634c2.png)

- Client application sends a query request into the data warehouse
- The leader node creates an execution plan, compiles the code, and distributes it to the appropriate compute nodes slices that contains data thats relevant to the query.
