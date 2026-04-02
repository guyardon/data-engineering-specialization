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

## 3.2.1 Hadoop Background and HDFS

**Distributed Processing Framework - Hadoop**

Hadoop emerged from the big data era of the late 1990s and 2000s, when traditional monolithic data warehouses could not handle massive data volumes and commodity hardware became cheap and ubiquitous.


---

**Historical Background**

Several innovations in large-scale distributed storage and computing laid the groundwork for Hadoop's architecture.


---

**Hadoop Distributed File System**

`HDFS` combines compute and storage on the same nodes, unlike **object storage** which has limited compute support for internal processing. Large files are broken into **blocks** of a few hundred megabytes each.

The file system is managed by the **NameNode**, which handles directories, file metadata, and a detailed catalog describing where file blocks reside in the cluster.

A typical HDFS configuration includes:
- **Replication**: each block is replicated across 3 **DataNodes**, increasing durability and availability
- **Combined compute and storage**: enables in-place data processing via `MapReduce`

## 3.2.2 Hadoop MapReduce

**Hadoop MapReduce**

MapReduce sends computation code to the nodes that contain the data, favoring data locality rather than bringing data to the application. The computation has three phases:

- **Map** -- Read individual data blocks inside DataNodes and produce key-value pairs
- **Shuffle** -- Redistribute results across the cluster so each DataNode holds unique keys
- **Reduce** -- Aggregate data on each node
![](/data-engineering-specialization-website/images/575a54c8-916b-4f16-83ef-ffb51e3bcb8f.png)

Example: SQL Query in MapReduce

In the diagram below, keys (in yellow/red) are user IDs and values are counts.
![](/data-engineering-specialization-website/images/d6a542c5-c54a-4d2c-8592-2a7d08fe7fdf.png)


---

**Shortcomings of MapReduce**

MapReduce writes to disk at every intermediate step -- never to memory. This simplifies state and workflow management and minimizes memory consumption, but results in high disk bandwidth utilization and increased processing time.

Newer approaches like `Spark` improved on this with **in-memory caching**. RAM is faster than SSD/HDD in both transfer speed and seek time, delivering dramatic speedups. Spark treats data as a distributed set that resides in memory, using disk only as a fallback when data overflows available memory.
