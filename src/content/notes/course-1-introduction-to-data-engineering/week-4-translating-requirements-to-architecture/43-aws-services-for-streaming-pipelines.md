---
title: "4.3 AWS Services for Streaming Pipelines"
course: "Course 1: Introduction to Data Engineering"
courseSlug: "course-1-introduction-to-data-engineering"
courseOrder: 1
week: "Week 4: Translating Requirements to Architecture"
weekSlug: "week-4-translating-requirements-to-architecture"
weekOrder: 5
order: 3
notionId: "18d969a7-aa01-80dc-9629-c246ca2a0883"
---

## 4.3.1 AWS Services for Streaming Pipelines

AWS offers two primary managed services for streaming data ingestion.

**Amazon Kinesis Data Streams** accepts any type of data from producers, retains it for a minimum of 24 hours, and delivers it to consumer applications for storage or real-time analysis.

**Amazon Managed Streaming for Apache Kafka (Amazon MSK)** runs open-source Kafka. Data engineers interact with the Kafka data plane — which MSK manages — to create topics, produce data, and consume data.

Both services scale to handle petabyte-level data volumes with millisecond latency. **Kinesis** is more user-friendly and reduces operational overhead, while **MSK** is the better choice if your team has Kafka experience or needs a high degree of flexibility and control.

**Amazon Data Firehose** integrates with Kinesis Data Streams to simplify the downstream work — it handles creating connections, reading from the stream, chunking data, and writing to storage, eliminating the need for custom code.
