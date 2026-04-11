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

<img src="/data-engineering-specialization/images/diagrams/data-engineering-lifecycle-dark.svg" alt="The Data Engineering Lifecycle" class="diagram diagram-dark" />
<img src="/data-engineering-specialization/images/diagrams/data-engineering-lifecycle.svg" alt="The Data Engineering Lifecycle" class="diagram diagram-light" />

## 2.1.1 Data Generation in Source Systems

The data engineering lifecycle begins at the source. Data can originate from a wide variety of systems, and understanding those systems is the first step toward building reliable pipelines.

- **Databases** — relational databases, NoSQL stores (key-value, document)
- **Files** — text, audio, video, and other formats
- **APIs** — data returned as `JSON` or XML from programmatic requests
- **Data sharing platforms** — internal datasets or third-party providers
- **IoT devices** — fleets of sensors that typically feed into a database, API, or sharing platform

The upstream stakeholders for data generation are usually software engineers or third-party platform owners. Source systems are often unpredictable, so it is important to build relationships with source system owners and understand how the data and its schema might change over time.

<img src="/data-engineering-specialization/images/diagrams/source-systems-dark.svg" alt="Data Generation — Source Systems" class="diagram diagram-dark" />
<img src="/data-engineering-specialization/images/diagrams/source-systems.svg" alt="Data Generation — Source Systems" class="diagram diagram-light" />

## 2.1.2 Ingestion

**Ingestion** is the process of moving raw data from source systems into the data pipeline for further processing. The key design decision here is frequency.

**Batch ingestion** processes data on a predetermined time interval or once a size threshold is reached. **Stream ingestion** uses an event-streaming platform or message queue to provide continuous, near-real-time data availability shortly after production. Streaming adds cost, complexity, and maintenance burden, so it should only be adopted when there is a clear business use case. In practice, data engineers often decide where the boundary between batch and streaming falls.

<img src="/data-engineering-specialization/images/diagrams/ingestion-batch-stream-dark.svg" alt="Ingestion — Batch vs Stream" class="diagram diagram-dark" />
<img src="/data-engineering-specialization/images/diagrams/ingestion-batch-stream.svg" alt="Ingestion — Batch vs Stream" class="diagram diagram-light" />

## 2.1.3 Data Storage

Storage sits at every stage of the lifecycle. The raw hardware ingredients trade off against each other in predictable ways. Process-level components such as networking, compression, serialization, and caching also influence storage performance.

Data engineers typically work with **database management systems**, **object storage**, `Apache Iceberg`, **cache/memory-based stores**, and **streaming storage**. These sit behind higher-level abstractions — **data warehouses**, **data lakes**, and **data lakehouses** — that let you configure latency, scalability, and cost to match your workload.

<img src="/data-engineering-specialization/images/diagrams/data-storage-dark.svg" alt="Data Storage" class="diagram diagram-dark" />
<img src="/data-engineering-specialization/images/diagrams/data-storage.svg" alt="Data Storage" class="diagram diagram-light" />

## 2.1.4 Data Transformation

Transformation is where raw data becomes something useful. It breaks down into three parts.

<img src="/data-engineering-specialization/images/diagrams/data-transformation-dark.svg" alt="Data Transformation" class="diagram diagram-dark" />
<img src="/data-engineering-specialization/images/diagrams/data-transformation.svg" alt="Data Transformation" class="diagram diagram-light" />

## 2.1.5 Serving Data

The final stage delivers data to end consumers across three main channels: **analytics**, **machine learning**, and **reverse ETL**.

<img src="/data-engineering-specialization/images/diagrams/serving-data-dark.svg" alt="Serving Data" class="diagram diagram-dark" />
<img src="/data-engineering-specialization/images/diagrams/serving-data.svg" alt="Serving Data" class="diagram diagram-light" />
