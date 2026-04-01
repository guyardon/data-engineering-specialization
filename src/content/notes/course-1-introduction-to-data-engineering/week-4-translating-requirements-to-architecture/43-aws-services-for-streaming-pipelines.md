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

Amazon Kinesis Data Streams

- Data producers send data to Kinesis
- Any type of data can be sent
- Minimum retention time: 24 hours
- Kinesis sends data streams to data consumers (software)
- Either pass to storage, real time analysis

Amazon Managed Streaming for Apache Kafka (Amazon MSK)

- Runs open source versions of Kafka
- Data engineer interacts with Kafka Data Plane that MSK manages for you to create topics, produce, and consume data

Both can scale up to handle petabyte-level data volumes with millisecond latency

Kinesis is considered more suer friendly and reduces operational overhead, while MSK is good if you have technical experience with Kafka, or need high degree of flexibility and control.

Amazon Data Firehouse

- Integrates with Amazon Kinesis Data Stream
- Simplifies the process of writing custom code for creating connection, reading stream, chunking data and storing data.


