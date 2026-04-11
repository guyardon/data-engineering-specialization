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

<img class="tech-logo-aside logo-light" src="/data-engineering-specialization/images/logos/hadoop.svg" alt="Apache Hadoop" /><img class="tech-logo-aside logo-dark" src="/data-engineering-specialization/images/logos/hadoop-dark.svg" alt="Apache Hadoop" />

**Apache Hadoop**

`Hadoop` emerged in the mid-2000s, inspired by Google's GFS (2003) and MapReduce (2004) papers, when traditional monolithic data warehouses could not handle massive data volumes.

---

**Hadoop Distributed File System (HDFS)**

`HDFS` combines compute and storage on the same nodes, unlike object storage which has limited compute support for internal processing. Large files are broken into **blocks** of a few hundred megabytes each.

| Component     | Role                                                                                                       |
| ------------- | ---------------------------------------------------------------------------------------------------------- |
| **NameNode**  | Manages directories, file metadata, and a catalog describing where file blocks reside in the cluster       |
| **DataNodes** | Store the actual data blocks - each block is replicated across 3 DataNodes for durability and availability |

Key properties:

- **Replication** - each block stored on 3 nodes increases durability and availability
- **Combined compute and storage** - enables in-place data processing via `MapReduce`

## 3.2.2 Hadoop MapReduce

`MapReduce` sends computation code to the nodes that contain the data, favoring **data locality** rather than moving data to the application. The computation has three phases:

| Phase       | Action                                                                     |
| ----------- | -------------------------------------------------------------------------- |
| **Map**     | Read individual data blocks inside DataNodes and produce key-value pairs   |
| **Shuffle** | Redistribute results across the cluster so each DataNode holds unique keys |
| **Reduce**  | Aggregate data on each node into final results                             |

For example, counting user events: the Map phase scans log blocks and emits `(user_id, 1)` pairs, the Shuffle phase groups all pairs by `user_id`, and the Reduce phase sums the counts per user.

<img src="/data-engineering-specialization/images/diagrams/mapreduce-flow-dark.svg" alt="MapReduce flow: Map emits key-value pairs, Shuffle groups by key, Reduce aggregates" class="diagram diagram-dark" />
<img src="/data-engineering-specialization/images/diagrams/mapreduce-flow.svg" alt="MapReduce flow: Map emits key-value pairs, Shuffle groups by key, Reduce aggregates" class="diagram diagram-light" />

---

**Shortcomings of MapReduce**

MapReduce writes to disk at every intermediate step - never to memory. This simplifies state management and minimizes memory consumption, but results in high disk bandwidth utilization and slow processing for iterative algorithms.

`Spark` improved on this with **in-memory caching**. RAM is faster than SSD/HDD in both transfer speed and seek time, delivering dramatic speedups. Spark treats data as a distributed set that resides in memory, using disk only as a fallback when data overflows available memory.
