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

This is the first stage of the data engineering lifecycle

Data can come from various sources:

- Database
- Relational databases
- NoSQL databases (key-value stores, document stores)
- Files
- Text, audio, video, etc.
- APIs
- Application Programming Interface
- data returned as .json or .xml files from request
- Data sharing platforms
- internal data user or third party
- IoT devices
- “Swarm of IoT devices”
- Sent to a database, and made available via API or data sharing platform

The upstream stakeholders of the data generation are commonly software engineers or third party platforms.

Source systems are often unpredictable:

It is important to understand how the source systems are set up (interact with the source system owners), and understand how the data might change.



## 2.1.2 Ingestion

Ingestion means moving raw data from source systems into the data pipeline for further processing.

Frequency of Ingestion

- Batch vs. stream Ingestion
- Batch Ingestion
- Based on predetermined time interval or preset size threshold
- Stream Ingestion
- Need to use event-streaming platform or message queue
- Continuous near real-time ingestion
- Data available shortly after it is produced
- What to consider?
- real-time actions
- time, money, maintenance, downtime
- stream ingestion only when there is a business use-case for streaming. 
- Often data engineers choose where the boundary between batch and streaming occurs.



## 2.1.3 Data Storage

Raw hardware ingredients:

- SSDs
- Magnetic Disks (2-3 times cheaper than SSDs)
- RAM (faster reads and writes, 30-50 times more expensive than SSD, volatile).
Process components (part of CPU):

- Networking
- Compression
- Serialization
- Caching

As a data engineer, you’ll work with storage systems such as:

- Database management systems,
- Object storage
- Apache Iceberg
- Cache/Memory-based storage
- Streaming storage

Storage Abstractions:

- Data Warehouse
- Data Lake
- Data Lakehouse

These allow to configure:

- Latency
- Scalability
- Cost

## 2.1.4 Data Transformation

The “turn it into something useful” stage

3 Parts:

- Queries
- Insert a request to read requests from a database or other storage systems, e.g. cleaning, joining, aggregating and filtering data
- Modeling
- Choosing a coherent structure for your data to make it useful for the business
- Transformation
- Manipulating, enhancing and saving data for downstream use

## 2.1.5 Serving Data

Analytics, ML and Reverse ETL

Analytics:

The process of identifying key insights and patterns within data

- Business Intelligence
- Explore historical or current business data to discover insights
- Usually used served data to create reports and dashboards
- Operational Analytics
- Monitoring real-time data for immediate action
- Embedded Analytics
- Eternal or customer facing analytics (i.e. creating dashboards inside a product).

Machine Learning

- Serving feature stores
- Serving data for realtime inference
- Track data history and lineage

Reverse ETL

- Feeding back transformed data to source systems
