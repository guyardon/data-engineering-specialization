---
title: "2.2 Introduction to the Undercurrents"
course: "Course 1: Introduction to Data Engineering"
courseSlug: "course-1-introduction-to-data-engineering"
courseOrder: 1
week: "Week 2: The Data Engineering Lifecycle & Undercurrents"
weekSlug: "week-2-the-data-engineering-lifecycle-undercurrents"
weekOrder: 3
order: 2
notionId: "145969a7-aa01-8084-ba9c-d2bb87535441"
---

Beneath every stage of the data engineering lifecycle run a set of cross-cutting concerns — the **undercurrents**. These practices shape how data systems are built, operated, and evolved.


## 2.2.1 Security

Security in data engineering centers on the **principle of least privilege**: give users or applications access to only the essential data and resources they need, and only for the duration required. Adopt a defensive mindset — be cautious with sensitive data and design every system with the assumption that attacks will happen.

## 2.2.2 Data Management

Data management is *"the development, execution, and supervision of plans, programs, and practices that deliver, control, protect, and enhance the value of data and information assets throughout their life cycles."* At its core, **data governance** ensures the quality, integrity, security, and usability of the data an organization collects.

![](/data-engineering-specialization-website/images/adf4b2ca4.png)

![](/data-engineering-specialization-website/images/5803be52-9139-45d0-b34f-af7660196951.png)


## 2.2.3 Data Architecture

Data architecture is *"the design of systems to support the **evolving** **data needs** of an enterprise, achieved by **flexible** and **reversible** decisions reached through a careful **evaluation of trade-offs**."*

On-premises environments make flexible, reversible decisions extremely difficult. Cloud platforms change this equation significantly.

**Principles of Good Architecture:**

1. Choose common components wisely
2. Plan for failure
3. Architect for scalability
4. Architecture is leadership
5. Always be architecting
6. Build loosely coupled systems
7. Make reversible decisions
8. Prioritize security
9. Embrace FinOps



## 2.2.4 DataOps

Just as DevOps improves the development process and quality of software products, **DataOps aims to improve the development process and quality of data products.**

DataOps is a set of cultural habits and practices built on communication, collaboration, continuous improvement, and rapid iteration. Its two main pillars are:

- **Automation** — in DevOps this means CI/CD; in DataOps it means automated change management across code, configuration, environments, and data pipelines, often powered by orchestration frameworks like `Apache Airflow`
- **Observability and monitoring** — everything fails eventually, so the goal is to detect failures before they reach downstream consumers (ML models, analytics dashboards, reports) and have a clear incident response process



## 2.2.5 Orchestration

Manually running individual tasks works for prototyping but is unsustainable in production. Orchestration frameworks coordinate the execution of pipeline steps automatically.

**Scheduling**

The most popular orchestration tools today include:

- `Apache Airflow` (industry standard)
- `Dagster`
- `Prefect`
- `Mage`

These frameworks model workflows as **Directed Acyclic Graphs (DAGs)** — directed (data flows one way), acyclic (no backward loops), and composed of nodes and edges. Tasks can be triggered by events, and monitoring or alerting is configured alongside them.



## 2.2.6 Software Engineering

Software engineering — the design, development, deployment, and maintenance of applications — underpins everything a data engineer builds.

Common languages and frameworks span a wide range:

- `SQL`, `Apache Spark`, `Kafka`
- `Python`, `Java`, `Scala`, `Bash`
- Occasionally `R`, `Rust`, and `Go`

In practice, the most common day-to-day tools are `SQL`, `Python`, and `Bash`.
