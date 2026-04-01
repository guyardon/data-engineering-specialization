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

## Data Lakehouse

**The Data Lakehouse Architecture**

- Data Lakehouse = Data Lake + Data Warehouse
- First introduced by databricks
- Data Lake:
- flexibility
- low-cost storage
- Data Warehouse:
- superior query performance
- robust data management
![](/data-engineering-specialization-website/images/6723598f-36a0-49d5-8ab8-42fc838b68c0.png)

**Data Lakehouse Implementation**

Open Table Formats:

- Specialized storage formats that dad transactional features to your data lakehouse
- allows you to update and delete records
- supports ACID principles
- e.g. 
- Databricks Delta Lake
- Apache Iceberg
- Apache Hudi (Hadoop Update Delete Incremental)
- Features:
- Time travel + snapshots at any given time
- Schema and partition evolution
  - ability to query data even if you make changes to schema or partitioning
- Open source
  - different query engines can acess the data
- Example: Architecture of Apache Iceberg

![](/data-engineering-specialization-website/images/dbe7a62c-4d96-4114-b7f4-ea87ace47d8c.png)

![](/data-engineering-specialization-website/images/834de967-2908-4d42-9d0c-fb535b1bc30d.png)

