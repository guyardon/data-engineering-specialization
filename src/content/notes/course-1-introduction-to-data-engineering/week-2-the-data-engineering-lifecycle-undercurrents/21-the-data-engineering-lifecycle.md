---
title: "2.1 The Data Engineering Lifecycle"
course: "Course 1: Introduction to Data Engineering"
courseSlug: "course-1-introduction-to-data-engineering"
courseOrder: 1
week: "Week 2: The Data Engineering Lifecycle & Undercurrents"
weekSlug: "week-2-the-data-engineering-lifecycle-undercurrents"
weekOrder: 3
order: 1
notionId: "146969a7-aa01-8042-9f80-da699a7409de"
---



## 2.1.1 Data Generation in Source Systems

The data engineering lifecycle begins at the source. Data can originate from a wide variety of systems, and understanding those systems is the first step toward building reliable pipelines.

- **Databases** — relational databases, NoSQL stores (key-value, document)
- **Files** — text, audio, video, and other formats
- **APIs** — data returned as JSON or XML from programmatic requests
- **Data sharing platforms** — internal datasets or third-party providers
- **IoT devices** — fleets of sensors that typically feed into a database, API, or sharing platform

The upstream stakeholders for data generation are usually software engineers or third-party platform owners. Source systems are often unpredictable, so it is important to build relationships with source system owners and understand how the data and its schema might change over time.



## 2.1.2 Ingestion

**Ingestion** is the process of moving raw data from source systems into the data pipeline for further processing. The key design decision here is frequency.

**Batch ingestion** processes data on a predetermined time interval or once a size threshold is reached. **Stream ingestion** uses an event-streaming platform or message queue to provide continuous, near-real-time data availability shortly after production. Streaming adds cost, complexity, and maintenance burden, so it should only be adopted when there is a clear business use case. In practice, data engineers often decide where the boundary between batch and streaming falls.



## 2.1.3 Data Storage

Storage sits at every stage of the lifecycle. The raw hardware ingredients trade off against each other in predictable ways:

- **SSDs** — solid-state, general purpose
- **Magnetic disks** — 2-3x cheaper than SSDs
- **RAM** — fastest reads and writes, but 30-50x more expensive than SSD and volatile

Process-level components such as networking, compression, serialization, and caching also influence storage performance.

Data engineers typically work with **database management systems**, **object storage**, **Apache Iceberg**, **cache/memory-based stores**, and **streaming storage**. These sit behind higher-level abstractions — **data warehouses**, **data lakes**, and **data lakehouses** — that let you configure latency, scalability, and cost to match your workload.

## 2.1.4 Data Transformation

Transformation is where raw data becomes something useful. It breaks down into three parts:

- **Queries** — requests to read from a database or storage system, including cleaning, joining, aggregating, and filtering
- **Modeling** — choosing a coherent structure that makes data useful for the business
- **Transformation** — manipulating, enhancing, and saving data for downstream consumption

## 2.1.5 Serving Data

The final stage delivers data to end consumers across three main channels.

**Analytics** is the process of identifying key insights and patterns within data:

- **Business Intelligence** — exploring historical or current data to discover insights, typically through reports and dashboards
- **Operational Analytics** — monitoring real-time data for immediate action
- **Embedded Analytics** — customer-facing analytics built directly into a product

**Machine Learning** consumes served data through feature stores, real-time inference endpoints, and data lineage tracking.

**Reverse ETL** closes the loop by feeding transformed data back into source systems.
