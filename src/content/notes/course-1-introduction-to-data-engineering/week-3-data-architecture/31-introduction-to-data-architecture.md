---
title: "3.1 Introduction to Data Architecture"
course: "Course 1: Introduction to Data Engineering"
courseSlug: "course-1-introduction-to-data-engineering"
courseOrder: 1
week: "Week 3: Data Architecture"
weekSlug: "week-3-data-architecture"
weekOrder: 4
order: 1
notionId: "18c969a7-aa01-8012-908e-cb0e0b1f7b79"
---



## What is Data Architecture?

**Enterprise Architecture:**

- “the design of systems to **support change in enterprise**, achieved by flexible and reversible decisions reached through a careful evaluation of trade-offs”
- Domains:
- Business architecture
  - Product or service strategy and business model
- Application architecture
  - Structure and interaction of key applications
- Technical architecture
  - interaction of software and hardware components
- Data architecture
  - supporting the evolving data needs
- Change management
- adapt to organizational changes
- “one-way” (impossible to reverse) and “two-way” (possible to reverse) door decisions. Depends on the stakes involved..

**Conway’s Law:**

- “Any organization that designs a system will produce a design whose structure is a copy of the organization’s communication structure”
- E.g. if the departments are isolated, the systems they create will be isolated. If departments work together, they can use shared data systems. 


## Principles of Good Architecture


How data architecture impacts other teams and individuals:

**Choose common components wisely**:

- “Wise Choice”
- Common components facilitate team collaboration. 
- Need to identify tools that benefit all teams.

---

**Always be architecting**:

- Make reversible
-  2 way doors 
- Support the needs of today but also the needs of tomorrow
- Build loosely coupled systems 
- Components that can be swapped out and replaced without having to redesign the system
- Components should interface via an API
---

**Plan for Failure:**

1. Availability: the percentage of time an IT service or a component is expected to be in an operable state:
1. 99.5% availability - 44 hour downtime in a year
2. 99.99% availability - 1 hour downtime in a year
2. Reliability - the probability of a particular service or component performing its intended function during a particular time interval.
3. Durability - the ability of a storage system to withstand data loss due to hardware, software failures or natural disasters. (e.g. Amazon S3 Durability is 99.99999999999% (11 decimal places) durable.
4. Recovery time objective: maximum acceptable time for a service or a system outage (RTO)
5. Recovery point objective (RPO) A definition of the acceptable state after recovery (e.g. maximum acceptable data loss)

**Prioritize security**

**Embrace FinOps**

- Large unforeseen costs
- Missed opportunities for revenues



## Batch Architectures

- Data is processed (ingested and transformed) in batches
- Real-time analysis is not critical

**ETL (Extract-Transform-Load) Architecture:**

- Extract batches and store in staging area
- Transform data into usable format (standardize, clean up, model the data)
- Load into data warehouse for storage and serving

**ELT (Extract-Load-Transform) Architecture: **

- Extract batches of data
- Load the data into a data warehouse
- Perform the transformations inside the data warehouse

ELT is becoming more popular because of modern cloud data warehouses.

**Downstream Use-cases:**

- Analytics and reports
- Machine learning
- Reverse ETL (Processed data is sent back to the source systems)

**Data Mart**

- Optional subset of a data warehouse for a specific department/ function/ business area
- Comes after transformation but before serving
- May have its own stages of transformation

## Streaming Architectures

- At its source, the data is a continuous stream of events

![](/data-engineering-specialization-website/images/a21164ad1.png)

Event streaming platform:

- Apache Kafka

Streaming and real-time analytics:

- Apache storm
- Samza

Batch + stream architectures can be combined into a **Lambda Architecture.**

- Parallel systems for streaming and batch processing
- Serving layer is combined (i.e. data is aggregated from both batch and streaming systems into a single view)
- Not so popular anymore

**Kappa Architecture**

- Stream processing architecture that retains some historical data
- Not widely adopted

Tools for unifying multiple code paths:

- Google Dataflow
- Beam

**Apache Flink** allows to combine stream processing and batch processing by providing a single system. Batch processing is simply stream processing where data is bounded.

**Today:**

Batch is a “special case” of streaming. 



## Architecting for Compliance

- General Data Protection Regulation (GDPR)
- Enacted in the EU in 2018
- To collect personal information you must ask for consent from the individual, and they have the right to ask for their data to be deleted.
- Similar regulations in other countries
- Systems need to be constantly complying with the regulations of today and tomorrow. 
- Building loosely coupled systems allows to swap components that comply with new regulations.

Industry Regulations:

- Medical Industry: Health Insurance Portability and Accountability Act
- Financial Industry: Sarbanes Oxley Act in the US. 
