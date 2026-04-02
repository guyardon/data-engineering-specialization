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


---

**Overview**

When data arrives continuously, query patterns must reflect that real-time nature. Frameworks like `Apache Flink`, **Spark Streaming**, and `Kafka` enable SQL queries over streaming data, typically using windowing techniques to bound the otherwise infinite stream.


---

**Windowing techniques:**

- **Session window** — groups events that arrive together and filters out periods of inactivity. You specify a gap-of-inactivity threshold; aggregations are computed per session, and a new session starts after each gap. Useful for events arriving at irregular intervals.
- **Fixed-time (Tumbling) window** — divides the stream into non-overlapping windows of equal duration.
- **Sliding window** — like tumbling windows, but overlapping — each window advances by a fixed step that is smaller than the window size.

**Joining Data Streams** is also possible, combining records from two or more streams based on matching keys within a time window.

![](/data-engineering-specialization-website/images/7d48148e-5530-4388-86d7-6da77315ff57.png)

## 3.4.2 Deploying with Amazon Managed Service for Apache Flink

**Deploying an Application with Amazon Managed Service for Apache Flink**

AWS provides a fully managed service for running Apache Flink applications, handling infrastructure provisioning, scaling, and fault tolerance so you can focus on writing streaming logic.

![](/data-engineering-specialization-website/images/6f598b43-b313-4d98-89b7-ef9cab0b67f3.png)

![](/data-engineering-specialization-website/images/97d7dafd-5dcb-4d91-8391-bbad1956d862.png)
