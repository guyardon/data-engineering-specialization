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

When data arrives continuously, query patterns must reflect that real-time nature. Frameworks like `Apache Flink`, `Spark Streaming`, and `Kafka` enable SQL queries over streaming data, typically using **windowing techniques** to bound the otherwise infinite stream.

---

**Windowing Techniques**

| Window Type | Behavior | Use Case |
|---|---|---|
| **Tumbling (fixed-time)** | Non-overlapping windows of equal duration. Each event belongs to exactly one window. | Regular aggregations — e.g., count events per minute |
| **Sliding** | Overlapping windows that advance by a fixed step smaller than the window size. Events can appear in multiple windows. | Moving averages — e.g., 5-minute average computed every 1 minute |
| **Session** | Variable-size windows grouped by activity. An inactivity gap triggers a new session. | User behavior analysis — e.g., web session tracking |

<img src="/data-engineering-specialization-website/images/diagrams/streaming-windows-dark.svg" alt="Streaming window types: tumbling, sliding, and session" class="diagram diagram-dark" />
<img src="/data-engineering-specialization-website/images/diagrams/streaming-windows.svg" alt="Streaming window types: tumbling, sliding, and session" class="diagram diagram-light" />

---

**Joining Data Streams**

Streaming joins combine records from two or more streams based on matching keys within a time window. For example, joining a clickstream with a purchase stream to correlate user behavior with transactions within a 30-minute window.

## 3.4.2 Deploying with Amazon Managed Service for Apache Flink

AWS provides a fully managed service for running `Apache Flink` applications, handling infrastructure provisioning, scaling, and fault tolerance so you can focus on writing streaming logic.

| Feature | Description |
|---|---|
| **Managed infrastructure** | No servers to provision — AWS handles cluster sizing, patching, and scaling |
| **Automatic scaling** | Adjusts parallelism based on incoming data throughput |
| **Fault tolerance** | Built-in checkpointing and state recovery — processing resumes from the last checkpoint after failures |
| **Integration** | Reads from `Kinesis Data Streams`, `Amazon MSK` (Kafka), and `S3`; writes to `S3`, `Redshift`, `OpenSearch`, and more |

A typical deployment: `Kinesis Data Streams` ingests real-time events, `Managed Apache Flink` processes and transforms the stream using SQL or Java/Python applications, and results are written to `S3` or `Redshift` for downstream analytics.
