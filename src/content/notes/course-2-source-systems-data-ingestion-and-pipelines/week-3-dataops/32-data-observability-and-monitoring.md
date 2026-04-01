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

**5 Pillars of Data Observability:**

1. **Distribution / Internal Quality**: Checks metrics such as NULL percentage, unique element percentage, summary statistics, and whether data falls within expected ranges. Ensures data is trusted based on your expectations.
2. **Freshness**: How up-to-date the data is within the final asset (table, BI report) -- when it was last updated and how frequently. Stale data results in wasted time and money.
3. **Volume**: Monitors the amount of data ingested, looking for unexpected spikes or drops. Sudden drops can indicate lost data or system outages; sudden increases may signal unexpected usage surges.
4. **Lineage**: According to [Barr](https://towardsdatascience.com/introducing-the-five-pillars-of-data-observability-e73734b263d5), "When data breaks, the first question is always 'where?'" Data lineage traces the data journey from source to destination, visualizing transformations and storage locations to identify the source of errors.
5. **Schema**: Monitors changes in data structure or types to prevent pipeline failures.

## 3.2.2 Monitoring Data Quality

Focus your monitoring efforts on the metrics that matter most. The core dimensions to track are **volume**, **distribution**, **null values**, and **freshness**. Identify the most important metrics by checking what stakeholders care about and talking with source system owners.


## 3.2.3 Observability Tools

**Great Expectations**

**Core Components**

![](/data-engineering-specialization-website/images/cd3cd7f0-368b-4ad6-b595-91ff95e55de6.png)


**AWS CloudWatch**

AWS's built-in monitoring service for tracking infrastructure and application metrics.

![](/data-engineering-specialization-website/images/d602344c-befd-49ae-8d1c-9a6983035691.png)
