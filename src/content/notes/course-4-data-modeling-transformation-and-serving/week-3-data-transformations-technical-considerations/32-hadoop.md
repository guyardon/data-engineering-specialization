---
title: "3.2 Hadoop"
course: "Course 4: Data Modeling, Transformation, and Serving"
courseSlug: "course-4-data-modeling-transformation-and-serving"
courseOrder: 4
week: "Week 3: Data Transformations & Technical Considerations"
weekSlug: "week-3-data-transformations-technical-considerations"
weekOrder: 3
order: 2
notionId: "1fc969a7-aa01-805e-8f9a-f648e027b479"
---

## :hadoop: Distributed Processing Framework -  Hadoop

### Historical Background

1990's-2000's: Big Data Era

- Traditional monolithic data warehouses were not able to handle massive amounts of data effectively
- Commodity hardware became cheap and ubiquitous

Several innovations in large-scale distributed storage and computing

### Hadoop Distributed File System

- **HDFS**: combines compute and storage on the same nodes
- **Object Storage:** limited compute support for internal processing

- Large files are broken into **blocks** (each a few hundred megabytes in size)
- File System is managed by the **NameNode**
- **NameNode** manages:
- directories
- file metadata
- detailed catalog describing location of file blocks in the cluster
- Typical Configuration
- Replication:
  - each block of data is replicated across 3 **DataNodes**
  - increases durability and availability of the data
- Combination of compute and storage
  - allows in-place data processing
  - achieved via **MapReduce**

### Hadoop MapReduce

- send computation code to the nodes that contain the data
- favors locality
- instead of bringing data to the application
- Computation code
- **Map**
  - Read individual data blocks (inside the DataNode) and produce key-value pairs
- **Shuffle**
  - Redistribute results across the cluster
  - each DataNode contains a unique keys
- **Reduce**
  - Aggregate data on each node
![](/data-engineering-specialization-website/images/575a54c8-916b-4f16-83ef-ffb51e3bcb8f.png)

Example: SQL Query in MapReduce

- Keys are in yellow/red (user_ids)
- Values are counts
![](/data-engineering-specialization-website/images/d6a542c5-c54a-4d2c-8592-2a7d08fe7fdf.png)

**Shortcomings of MapReduce**

- I/O to disk in all intermediate steps (never in memory)
- Pros:
  - Simplifies state and workflow management
  - minimizes memory consumption
- Cons:
  - High-disk bandwidth utilization
  - Increases processing time
- Newer approaches (e.g. Spark) improved on MapReduce by
- In-memory caching (RAM is faster than SSD/HDD in transfer speed and seek time)
- dramatic speedup
- Spark:
  - treats data as a distributed set that resides in memory, and
  - treats disk as a second-class data storage layer for processing (only used if data overflows available memory)
