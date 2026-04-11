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

<img src="/data-engineering-specialization/images/diagrams/enterprise-architecture-dark.svg" alt="Enterprise Architecture Domains" class="diagram diagram-dark" />
<img src="/data-engineering-specialization/images/diagrams/enterprise-architecture.svg" alt="Enterprise Architecture Domains" class="diagram diagram-light" />

**What is Data Architecture?**

**Enterprise Architecture:**

Enterprise architecture is _"the design of systems to **support change in enterprise**, achieved by flexible and reversible decisions reached through a careful evaluation of trade-offs."_ It spans several domains:

- **Business architecture** — product or service strategy and business model
- **Application architecture** — structure and interaction of key applications
- **Technical architecture** — interaction of software and hardware components
- **Data architecture** — supporting the evolving data needs of the organization

A key concept in enterprise architecture is **change management** — adapting to organizational changes. Decisions fall into two categories: "one-way door" decisions that are impossible to reverse and "two-way door" decisions that can be undone. The distinction depends on the stakes involved.

---

**Conway's Law:**

_"Any organization that designs a system will produce a design whose structure is a copy of the organization's communication structure."_ In practice, isolated departments build isolated systems; collaborative departments build shared data platforms.

## 3.1.2 Principles of Good Architecture

<img src="/data-engineering-specialization/images/diagrams/architecture-principles-w3-dark.svg" alt="Principles of Good Data Architecture" class="diagram diagram-dark" />
<img src="/data-engineering-specialization/images/diagrams/architecture-principles-w3.svg" alt="Principles of Good Data Architecture" class="diagram diagram-light" />

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

<img src="/data-engineering-specialization/images/diagrams/batch-streaming-dark.svg" alt="Batch and Streaming Architectures" class="diagram diagram-dark" />
<img src="/data-engineering-specialization/images/diagrams/batch-streaming.svg" alt="Batch and Streaming Architectures" class="diagram diagram-light" />

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

<img src="/data-engineering-specialization/images/diagrams/data-marts-dark.svg" alt="Data Warehouse to Data Marts" class="diagram diagram-dark" />
<img src="/data-engineering-specialization/images/diagrams/data-marts.svg" alt="Data Warehouse to Data Marts" class="diagram diagram-light" />

---

**Streaming Architectures**

In streaming architectures, data originates as a continuous stream of events rather than discrete batches.

Key technologies include `Apache Kafka` as the event streaming platform, and tools like `Apache Storm` and `Samza` for streaming and real-time analytics.

Batch and stream architectures can be combined. The **Lambda Architecture** runs parallel batch and streaming systems with a unified serving layer that aggregates results from both, though it has fallen out of favor due to its complexity. The **Kappa Architecture** uses a single stream-processing system that retains some historical data, but it has not seen wide adoption either.

Tools like `Google Dataflow` and `Beam` attempt to unify multiple code paths. `Apache Flink` takes this further by providing a single system for both stream and batch processing — treating batch as simply bounded streaming.

<div class="tech-logos">
  <div class="tech-logo">
    <img src="/data-engineering-specialization/images/logos/kafka.svg" alt="Apache Kafka" class="logo-light" /><img src="/data-engineering-specialization/images/logos/kafka-dark.svg" alt="Apache Kafka" class="logo-dark" />
    <span>Apache Kafka</span>
  </div>
  <div class="tech-logo">
    <img src="/data-engineering-specialization/images/logos/flink.svg" alt="Apache Flink" class="logo-light" /><img src="/data-engineering-specialization/images/logos/flink-dark.svg" alt="Apache Flink" class="logo-dark" />
    <span>Apache Flink</span>
  </div>
  <div class="tech-logo">
    <img src="/data-engineering-specialization/images/logos/spark.svg" alt="Apache Spark" class="logo-light" /><img src="/data-engineering-specialization/images/logos/spark-dark.svg" alt="Apache Spark" class="logo-dark" />
    <span>Apache Spark</span>
  </div>
</div>

---

**Today:**

The prevailing view is that batch is a "special case" of streaming.

## 3.1.4 Architecting for Compliance

<img src="/data-engineering-specialization/images/diagrams/compliance-framework-dark.svg" alt="Architecting for Compliance" class="diagram diagram-dark" />
<img src="/data-engineering-specialization/images/diagrams/compliance-framework.svg" alt="Architecting for Compliance" class="diagram diagram-light" />

**Architecting for Compliance**

Regulatory compliance is a non-negotiable concern in data architecture. The **General Data Protection Regulation (GDPR)**, enacted in the EU in 2018, requires explicit consent to collect personal information and grants individuals the right to request deletion. Similar regulations exist in other countries and are evolving constantly.

Systems must continuously comply with current and future regulations. Building loosely coupled architectures makes it possible to swap in components that meet new requirements without rebuilding everything.

**Industry-specific regulations** add further constraints:

- Medical: Health Insurance Portability and Accountability Act (HIPAA)
- Financial: Sarbanes-Oxley Act (SOX) in the US

## 3.1.5 Data Mesh

**Data Mesh** is a decentralized architectural paradigm that shifts data ownership from a central data team to the individual business domains that produce and understand the data. Rather than funneling all data through a monolithic platform team, each domain (e.g., payments, logistics, marketing) takes responsibility for publishing its own data as a product.

<img src="/data-engineering-specialization/images/diagrams/data-mesh-dark.svg" alt="Data Mesh principles: domain ownership, data as a product, self-serve platform, federated governance" class="diagram diagram-dark" />
<img src="/data-engineering-specialization/images/diagrams/data-mesh.svg" alt="Data Mesh principles: domain ownership, data as a product, self-serve platform, federated governance" class="diagram diagram-light" />

Data Mesh is built on four principles:

- **Domain ownership** — each business domain owns, produces, and serves its own analytical data rather than handing raw data to a central team for processing
- **Data as a product** — domains treat their published datasets as products with clear documentation, SLAs, discoverability, and quality guarantees
- **Self-serve data platform** — a shared infrastructure layer provides the tools, storage, and compute that domains need without requiring each team to build its own platform from scratch
- **Federated computational governance** — global interoperability standards (naming conventions, security policies, quality thresholds) are enforced automatically through the platform, while domains retain autonomy over their internal implementation

---

**When Data Mesh Applies**

Data Mesh is primarily relevant for large organizations where a central data team has become a bottleneck — too many domains competing for the same team's capacity, each with different data semantics that the central team struggles to understand deeply. For smaller organizations or teams with a manageable number of data sources, a centralized architecture is simpler and more practical.
