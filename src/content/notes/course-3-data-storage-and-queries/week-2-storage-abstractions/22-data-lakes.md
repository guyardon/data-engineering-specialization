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

## Data Lakes - Key Architectural Ideas

- Semi-structured data and unstructured data do not fit well into a structured schema
- Data lakes solve this through a central repository for storing large volumes of data
- No fixed schema or predefined set of transformations
- **Schema on read pattern**

**Data Lake 1.0**

- Combined different storage and processing technologies
- storage: hadoop hdfs/amazon s3
- processing: Apache Pig, presto, hive
- **Many shortcomings**:
- Data Swamp
  - No proper data management
  - No data cataloging
  - No data discovery tools
  - No guarantee on the data integrity and quality
- Write only storage
  - DML (data manipulation language) operations such as deleting or updating rows were painful to implement, and required creating new tables
  - Difficult to comply with data regulations
- No schema management or data modeling
  - Data not optimized for query operations such as joins
  - Hard to process stored data
- Large companies such as facebook were able to leverage data lake 1.0 with custom tools, but most companies had a hard time to use it

**Next-Generation Data Lakes**

- Attempt to solve shortcomings of data lake 1.0
- Improved storage, management and processing of data
- **Zones**
- used to organize data in a data lake, where each zone houses data that has been processed to a varying degree
- no set rules for number of zones or naming, but conventions are
  - landing/ raw zone
  - cleaned/ transformed zone
  - curated/ enriched zone
- advantages of zones:
  - apply appropriate data governance policies and each "stage" of the data
  - ensure data quality
- **Data Partitioning**
- divide a dataset into smaller, more manageable parts based on a set of criteria (e.g. time, date, location recorded in data, etc).
- allows faster queries (since only related partitions are scanned)
- **Data Catalog**
- metadata about the dataset (owner, source, partitions, schema of the data and changes over time).

![](/data-engineering-specialization-website/images/65ba9042-6afc-43dc-9cee-4195e49e439e.png)

- Shortcomings:
- Seperate data lake and data warehouse
  - data lake: low-cost storage for large amounts of data
  - data warehouse: subset of data moved from data lake to data warehouse for superior analytical queries
- This is expensive
  - can introduce bugs/failures
  - can cause issues with data quality, duplication and consistency
