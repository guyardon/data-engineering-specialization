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

## Data Observability and Monitoring

**DevOps Observability**

- Metrics:
- CPU and RAM usage
- Response Time
- Use Cases:
- Quickly detect anomalies
- Identify problems
- prevent downtime
- Ensure reliable software products

**Data Observability**

Monitor the health of data and data systems

- High Quality Data
- Accurate
- Complete
- Discoverable
- Available in a timely manner
- Upstream changes should be expected and mitigated
- E.g. if source systems change structure of data

Takeaways from Conversation with Barr Moses (CEO of Monte Carlo)

- Ask the following questions:
- Is the data up-to-date?
- Is the data complete?
- Are fields within expected ranges?
- Is the null rate higher or lower than it should be?
- Has the schema changed?
5 Pillars for Data Observablity:

1. **Distribution/ Internal Quality**: The quality pillar refers to the internal characteristics of the data, and checks metrics such as the percentage of NULL elements, percentage of unique elements, summary statistics and if your data is within the expected range. It helps you ensure that your data is trusted based on your data expectation.
2. **Freshness**: Data freshness refers to how "fresh" or "up-to-date" the data is within the final asset (table, BI report), i.e., when the data was last updated, and how frequently it is updated. Stale data results in wasted time and money.
3. **Volume**: Data volume refers to checking the amount of data ingested and looking for unexpected spikes or drops. Sudden drops in data volume can indicate issues like lost data or system outages, and sudden increases may indicate unexpected surges in usage.
4. **Lineage**: According to [Barr](https://towardsdatascience.com/introducing-the-five-pillars-of-data-observability-e73734b263d5), "When data breaks, the first question is always "where?" Data lineage helps you trace the data journey from its source to its destination, visualizing how data was transformed and where it was stored. This way, you can identify the source of errors or anomalies.
5. **Schema**: Data schema refers to monitoring changes in data structure or types. This pillar helps avoid the failure of the data pipeline.

**Monitoring Data Quality**

- Volume
- Distribution
- Null Values
- Freshness
Identify and focus on most important metrics (check what stakeholders care about, and talk with source system owners).

## Great Expectations

**Core Components**

![](/data-engineering-specialization-website/images/cd3cd7f0-368b-4ad6-b595-91ff95e55de6.png)

### AWS Cloudwatch

Monitoring on AWS

![](/data-engineering-specialization-website/images/d602344c-befd-49ae-8d1c-9a6983035691.png)
