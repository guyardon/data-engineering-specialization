---
title: "1.1 How to Think Like a Data Engineer"
course: "Course 1: Introduction to Data Engineering"
courseSlug: "course-1-introduction-to-data-engineering"
courseOrder: 1
week: "Week 1: How to Think Like a Data Engineer"
weekSlug: "week-1-how-to-think-like-a-data-engineer"
weekOrder: 1
order: 1
notionId: "144969a7-aa01-805a-8d43-f23e81e41cd5"
---

## 1.1.1 The Data Engineering Lifecycle

**Data Engineering Definition** (from Fundamentals of Data Engineering):

<em>Data engineering is the development, implementation, and maintenance of systems and processes that take in raw data and produce high quality consistent information that supports downstream use cases, such as analysis and machine learning. Data engineering is the intersection of security, data management, DataOps, data architecture, orchestration, and software engineering.</em>

<img src="/data-engineering-specialization/images/diagrams/data-engineering-lifecycle-dark.svg" alt="The Data Engineering Lifecycle" class="diagram diagram-dark" />
<img src="/data-engineering-specialization/images/diagrams/data-engineering-lifecycle.svg" alt="The Data Engineering Lifecycle" class="diagram diagram-light" />

---

**Data Pipeline Definition**

_The combination of architecture, systems, and processes that move data through the data engineering lifecycle._

---

**The Job of the Data Engineer**

At its core, the data engineer's job is to get raw data from somewhere, transform it into something useful, and make it available to downstream consumers.

## 1.1.2 The History of Data and Data Engineering

Data engineering didn't appear overnight - it evolved alongside decades of database and computing innovation.

<img src="/data-engineering-specialization/images/diagrams/history-of-data-engineering-dark.svg" alt="History of Data Engineering" class="diagram diagram-dark" />
<img src="/data-engineering-specialization/images/diagrams/history-of-data-engineering.svg" alt="History of Data Engineering" class="diagram diagram-light" />

- **1960s** - `IMS` (Information Management System) was IBM's **hierarchical database**, one of the first to manage data at scale. `CODASYL` defined the **network database model**, an early standard for how programs interact with databases.

- **1970s** - Edgar Codd's **relational model** changed everything. `Oracle` and `IBM DB2` turned that theory into commercial products, and `SQL` became the standard query language that still dominates today.

- **1980s** - `Teradata` pioneered **massively parallel data warehouses**, enabling analytics on large datasets. `Informatica` introduced **ETL tooling** to move and transform data between systems.

- **1990s** - **Ralph Kimball** and **Bill Inmon** defined competing approaches to **data warehouse design** (dimensional vs. enterprise). `OLAP` (Online Analytical Processing) enabled **multidimensional analysis**. The dot-com boom drove massive investment in web backends and databases.

- **2000s** - Google's papers on `GFS` (Google File System) and `MapReduce` laid the foundation for **distributed computing**. `Hadoop` made those ideas open source, kicking off the **Big Data era**.

- **2010s** - `Spark` replaced MapReduce with faster **in-memory processing**. `Kafka` enabled **real-time event streaming**. `Redshift` brought **cloud-native data warehousing** to the masses.

- **Today** - `dbt` brought **software engineering practices** to SQL transformations. `Snowflake` decoupled **storage from compute** in the cloud warehouse. `Airflow` became the standard for **pipeline orchestration**. The "Big Data Engineer" role has matured into the modern "Data Engineer" - focused on building with existing tools rather than inventing infrastructure from scratch.

## 1.1.3 The Data Engineer Among Other Stakeholders

Data engineers sit between the teams that produce data and the teams that consume it.

<img src="/data-engineering-specialization/images/diagrams/data-engineer-stakeholders-dark.svg" alt="The Data Engineer Among Stakeholders" class="diagram diagram-dark" />
<img src="/data-engineering-specialization/images/diagrams/data-engineer-stakeholders.svg" alt="The Data Engineer Among Stakeholders" class="diagram diagram-light" />

Communication with **upstream** stakeholders matters for understanding the data you're ingesting and catching anything that might disrupt the pipeline. Communication with **downstream** stakeholders matters for understanding how the data you serve relates to their goals and where it adds business value.

## 1.1.4 Business Value

The most important question for a data engineer: how does your work add value to the organization? Don't get hung up on every new technology - focus on what drives business outcomes.

<img src="/data-engineering-specialization/images/diagrams/business-value-dark.svg" alt="Business Value of Data Engineering" class="diagram diagram-dark" />
<img src="/data-engineering-specialization/images/diagrams/business-value.svg" alt="Business Value of Data Engineering" class="diagram diagram-light" />

## 1.1.5 Gathering System Requirements

Once you understand the business need, translate it into system requirements. These fall into two categories.

<img src="/data-engineering-specialization/images/diagrams/system-requirements-dark.svg" alt="Gathering System Requirements" class="diagram diagram-dark" />
<img src="/data-engineering-specialization/images/diagrams/system-requirements.svg" alt="Gathering System Requirements" class="diagram diagram-light" />

Cost and security constraints should be factored in from the start.

## 1.1.6 Translating Stakeholder Needs into Specific Requirements

Turning vague stakeholder needs into concrete requirements takes structured discovery.

<img src="/data-engineering-specialization/images/diagrams/translating-needs-dark.svg" alt="Translating Stakeholder Needs" class="diagram diagram-dark" />
<img src="/data-engineering-specialization/images/diagrams/translating-needs.svg" alt="Translating Stakeholder Needs" class="diagram diagram-light" />

## 1.1.7 Thinking Like a Data Engineer

Putting it all together, here is a repeatable framework for approaching any data engineering problem:

<img src="/data-engineering-specialization/images/diagrams/thinking-like-de-dark.svg" alt="Thinking Like a Data Engineer" class="diagram diagram-dark" />
<img src="/data-engineering-specialization/images/diagrams/thinking-like-de.svg" alt="Thinking Like a Data Engineer" class="diagram diagram-light" />
