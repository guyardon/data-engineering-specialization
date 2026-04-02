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


## 3.1.1 What is Data Architecture

**What is Data Architecture?**

**Enterprise Architecture:**

Enterprise architecture is *"the design of systems to **support change in enterprise**, achieved by flexible and reversible decisions reached through a careful evaluation of trade-offs."* It spans several domains:

- **Business architecture** — product or service strategy and business model
- **Application architecture** — structure and interaction of key applications
- **Technical architecture** — interaction of software and hardware components
- **Data architecture** — supporting the evolving data needs of the organization

A key concept in enterprise architecture is **change management** — adapting to organizational changes. Decisions fall into two categories: "one-way door" decisions that are impossible to reverse and "two-way door" decisions that can be undone. The distinction depends on the stakes involved.

---

**Conway's Law:**

*"Any organization that designs a system will produce a design whose structure is a copy of the organization's communication structure."* In practice, isolated departments build isolated systems; collaborative departments build shared data platforms.


## 3.1.2 Principles of Good Architecture

**Principles of Good Architecture**

Good data architecture has a direct impact on how effectively other teams and individuals can use data.

**Choose common components wisely**:

Common components facilitate team collaboration. The key is identifying tools that benefit all teams rather than optimizing for one group.

---

**Always be architecting**:

Architecture is never finished. Make reversible "two-way door" decisions, support today's needs while anticipating tomorrow's, and build **loosely coupled systems** — components that can be swapped out without redesigning the entire system, interfacing via APIs.

---

**Plan for Failure:**

Designing for failure means understanding several key metrics:

1. **Availability** — the percentage of time a service is in an operable state (e.g., 99.5% = ~44 hours of downtime/year; 99.99% = ~1 hour/year)
2. **Reliability** — the probability a service performs its intended function during a given time interval
3. **Durability** — the ability of a storage system to withstand data loss from hardware failures, software failures, or natural disasters (e.g., `Amazon S3` offers 99.999999999% durability)
4. **Recovery Time Objective (RTO)** — the maximum acceptable duration for a service outage
5. **Recovery Point Objective (RPO)** — the maximum acceptable data loss after recovery

---

**Prioritize security**

---

**Embrace FinOps**

FinOps guards against large unforeseen costs and missed revenue opportunities by making cloud spending a first-class engineering concern.


## 3.1.3 Batch and Streaming Architectures

**Batch Architectures**

In batch architectures, data is ingested and transformed in discrete chunks, and real-time analysis is not critical.

**ETL (Extract-Transform-Load) Architecture:**

- Extract batches of data and store them in a staging area
- Transform the data into a usable format (standardize, clean, model)
- Load the results into a data warehouse for storage and serving

**ELT (Extract-Load-Transform) Architecture:**

- Extract batches of data
- Load directly into a data warehouse
- Perform transformations inside the warehouse

ELT is becoming more popular thanks to the power of modern cloud data warehouses.

---

**Downstream Use-cases:**

- Analytics and reports
- Machine learning
- Reverse ETL (processed data sent back to source systems)

---

**Data Mart**

A **data mart** is an optional subset of a data warehouse scoped to a specific department, function, or business area. It sits after transformation but before serving, and may have its own additional transformation stages.

---

**Streaming Architectures**

In streaming architectures, data originates as a continuous stream of events rather than discrete batches.

![](/data-engineering-specialization-website/images/a21164ad1.png)

Key technologies include `Apache Kafka` as the event streaming platform, and tools like `Apache Storm` and `Samza` for streaming and real-time analytics.

Batch and stream architectures can be combined. The **Lambda Architecture** runs parallel batch and streaming systems with a unified serving layer that aggregates results from both, though it has fallen out of favor due to its complexity. The **Kappa Architecture** uses a single stream-processing system that retains some historical data, but it has not seen wide adoption either.

Tools like `Google Dataflow` and `Beam` attempt to unify multiple code paths. `Apache Flink` takes this further by providing a single system for both stream and batch processing — treating batch as simply bounded streaming.

---

**Today:**

The prevailing view is that batch is a "special case" of streaming.


## 3.1.4 Architecting for Compliance

**Architecting for Compliance**

Regulatory compliance is a non-negotiable concern in data architecture. The **General Data Protection Regulation (GDPR)**, enacted in the EU in 2018, requires explicit consent to collect personal information and grants individuals the right to request deletion. Similar regulations exist in other countries and are evolving constantly.

Systems must continuously comply with current and future regulations. Building loosely coupled architectures makes it possible to swap in components that meet new requirements without rebuilding everything.

**Industry-specific regulations** add further constraints:

- Medical: Health Insurance Portability and Accountability Act (HIPAA)
- Financial: Sarbanes-Oxley Act (SOX) in the US
