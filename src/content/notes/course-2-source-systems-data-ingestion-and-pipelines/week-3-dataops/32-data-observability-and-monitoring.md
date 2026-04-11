---
title: "3.2 Data Observability and Monitoring"
course: "Course 2: Source Systems, Data Ingestion and Pipelines"
courseSlug: "course-2-source-systems-data-ingestion-and-pipelines"
courseOrder: 2
week: "Week 3: DataOps"
weekSlug: "week-3-dataops"
weekOrder: 3
order: 2
notionId: "1d3969a7-aa01-80e3-b264-c6789380bcaa"
---

## 3.2.1 Observability Concepts

Data observability borrows from DevOps observability but focuses on the health of data itself, not just the systems that process it.

**DevOps Observability** monitors metrics like CPU/RAM usage and response time to quickly detect anomalies, identify problems, prevent downtime, and ensure reliable software products.

**Data Observability** monitors the health of data and data systems, ensuring high-quality data that is accurate, complete, discoverable, and available in a timely manner. Upstream changes -- such as source systems changing their data structure -- should be expected and mitigated proactively.

**Key questions to ask** (from Barr Moses, CEO of Monte Carlo):

- Is the data up-to-date?
- Is the data complete?
- Are fields within expected ranges?
- Is the null rate higher or lower than it should be?
- Has the schema changed?

<img src="/data-engineering-specialization/images/diagrams/observability-concepts-dark.svg" alt="Observability Concepts - DevOps vs Data Observability" class="diagram diagram-dark" />
<img src="/data-engineering-specialization/images/diagrams/observability-concepts.svg" alt="Observability Concepts - DevOps vs Data Observability" class="diagram diagram-light" />

**5 Pillars of Data Observability:**

1. **Distribution / Internal Quality**: Checks metrics such as NULL percentage, unique element percentage, summary statistics, and whether data falls within expected ranges. Ensures data is trusted based on your expectations.
2. **Freshness**: How up-to-date the data is within the final asset (table, BI report) -- when it was last updated and how frequently. Stale data results in wasted time and money.
3. **Volume**: Monitors the amount of data ingested, looking for unexpected spikes or drops. Sudden drops can indicate lost data or system outages; sudden increases may signal unexpected usage surges.
4. **Lineage**: According to [Barr](https://towardsdatascience.com/introducing-the-five-pillars-of-data-observability-e73734b263d5), "When data breaks, the first question is always 'where?'" Data lineage traces the data journey from source to destination, visualizing transformations and storage locations to identify the source of errors.
5. **Schema**: Monitors changes in data structure or types to prevent pipeline failures.

<img src="/data-engineering-specialization/images/diagrams/five-pillars-dark.svg" alt="5 Pillars of Data Observability" class="diagram diagram-dark" style="max-height: 900px;" />
<img src="/data-engineering-specialization/images/diagrams/five-pillars.svg" alt="5 Pillars of Data Observability" class="diagram diagram-light" style="max-height: 900px;" />

## 3.2.2 Monitoring Data Quality

Focus your monitoring efforts on the metrics that matter most. The core dimensions to track are **volume**, **distribution**, **null values**, and **freshness**. Identify the most important metrics by checking what stakeholders care about and talking with source system owners.

## 3.2.3 Observability Tools

<img class="tech-logo-aside logo-light" src="/data-engineering-specialization/images/logos/great-expectations.svg" alt="Great Expectations" /><img class="tech-logo-aside logo-dark" src="/data-engineering-specialization/images/logos/great-expectations-dark.svg" alt="Great Expectations" />

**Great Expectations**

`Great Expectations` (GX) is an open-source Python library for validating, documenting, and profiling data. It lets you define **expectations** - declarative assertions about what your data should look like.

---

When expectations fail, GX generates detailed reports showing exactly which rows or columns violated the rules, making it easy to catch data quality issues before they reach downstream consumers. GX stores all metadata - expectations, validation results, checkpoints, and data docs - in configurable backend stores, keeping your validation logic versioned and reproducible.

**Core Components**

<img src="/data-engineering-specialization/images/diagrams/great-expectations-workflow-dark.svg" alt="Great Expectations Workflow" class="diagram diagram-dark" style="max-height: 900px;" />
<img src="/data-engineering-specialization/images/diagrams/great-expectations-workflow.svg" alt="Great Expectations Workflow" class="diagram diagram-light" style="max-height: 900px;" />

<img class="tech-logo-aside logo-light" src="/data-engineering-specialization/images/logos/cloudwatch.svg" alt="AWS CloudWatch" /><img class="tech-logo-aside logo-dark" src="/data-engineering-specialization/images/logos/cloudwatch-dark.svg" alt="AWS CloudWatch" />

**CloudWatch**

`CloudWatch` is AWS's built-in monitoring service for tracking infrastructure and application metrics.

---

It collects **system-level metrics** (CPU, memory, disk, network) automatically from AWS resources, and supports **custom metrics** for application-specific measurements like transaction counts or API response times. `CloudWatch` **Alarms** let you define thresholds on any metric and trigger notifications or automated actions when those thresholds are breached. It retains metrics data for up to 15 months, enabling long-term trend analysis and capacity planning.

<img src="/data-engineering-specialization/images/diagrams/cloudwatch-dark.svg" alt="AWS CloudWatch" class="diagram diagram-dark" />
<img src="/data-engineering-specialization/images/diagrams/cloudwatch.svg" alt="AWS CloudWatch" class="diagram diagram-light" />

## 3.2.4 Data Contracts

A **data contract** is a formal agreement between a data producer and its consumers that defines the structure, semantics, quality guarantees, and service-level expectations for a dataset. Data contracts shift quality enforcement upstream - instead of consumers discovering problems after the fact, producers commit to delivering data that meets a defined standard.

---

**What a Data Contract Specifies**

| Element                    | Description                                                                                                |
| -------------------------- | ---------------------------------------------------------------------------------------------------------- |
| **Schema**                 | Column names, data types, nullability constraints, and valid value ranges                                  |
| **Freshness SLA**          | Maximum acceptable delay between data generation and availability (e.g., "within 2 hours of midnight UTC") |
| **Volume expectations**    | Expected row count ranges - an empty table or a 10x spike may indicate a problem                           |
| **Ownership**              | The team responsible for maintaining the contract and responding to violations                             |
| **Breaking change policy** | How schema changes are communicated - e.g., deprecation windows, versioning rules                          |

---

**Why Data Contracts Matter**

Without contracts, data pipelines are fragile. A source team renames a column, changes a data type, or stops populating a field - and downstream dashboards break silently. Data contracts make these dependencies explicit and enforceable. When a producer violates the contract, automated validation catches it before the bad data propagates downstream.

Data contracts are closely related to **data observability** - the contract defines what "healthy" looks like, and observability tools monitor for violations.
