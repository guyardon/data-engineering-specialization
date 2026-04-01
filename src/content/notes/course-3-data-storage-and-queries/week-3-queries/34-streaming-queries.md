---
title: "3.4 Streaming Queries"
course: "Course 3: Data Storage and Queries"
courseSlug: "course-3-data-storage-and-queries"
courseOrder: 3
week: "Week 3: Queries"
weekSlug: "week-3-queries"
weekOrder: 3
order: 4
notionId: "1e7969a7-aa01-80f3-9892-df23d918832b"
---


## 3.4.1 Streaming Query Patterns

**Streaming Queries**


**Overview**

- Query patterns need to reflect the real time nature of the data
- SQL Queries on continuously streaming data is enabled by:
- Apache Flink
- Spark Streaming
- Kafka also allows querying data by windowed queries
- Windowing techniques:
- Session window
  - useful for handling events that arrive at irregular intervals
  - groups events that arrive together, and filters out periods with no events
  - Need to specify gap of inactivity (lower bound)
  - aggregations are computed on sessions, and after a gap of inactivity a new session is created
- Fixed-time (Tumbling) window
  - Each window has the size size in time
  - Non overlapping
- Sliding window
  - Overlapping fixed-time windows
- Joining Data Streams
![](/data-engineering-specialization-website/images/7d48148e-5530-4388-86d7-6da77315ff57.png)


## 3.4.2 Deploying with Amazon Managed Service for Apache Flink

**Deploying an Application with Amazon Managed Service for Apache Flink**

![](/data-engineering-specialization-website/images/6f598b43-b313-4d98-89b7-ef9cab0b67f3.png)

![](/data-engineering-specialization-website/images/97d7dafd-5dcb-4d91-8391-bbad1956d862.png)
