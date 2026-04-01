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

Data engineering incorporates various practices such as:


## 2.2.1 Security

Principle of least privilege

- give users or applications access to only the essential data and resources they need for only the duration required

Defensive Mindset:

- Be cautious with sensitive data
- Design for potential attacks

## 2.2.2 Data Management

“*the development, execution, and supervision of plans, programs, and practices that deliver, control, protect, and enhance the value of data and information assets throughout their life cycles”*

*“data governance is, first and foremost ,a data management function to ensure the quality, integrity, security, and usability of the data collected by an organization”*

![](/data-engineering-specialization-website/images/adf4b2ca4.png)

![](/data-engineering-specialization-website/images/5803be52-9139-45d0-b34f-af7660196951.png)


## 2.2.3 Data Architecture

*“the design of systems to support the ****evolving**** ****data needs**** of an enterprise, achieved by** ****flexible**** and ****reversible**** decisions reached through a careful ****evaluation of trade-offs****”*

on-premesis - very hard to make reversible and flexible decisions

In the cloud, this can be different.

Principles of Good Architecture:

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

Similar to how DevOps improve the development process and quality or software products, **DataOps aims to improve the development process and quality of data products. **

It’s a set of cultural habits and practices:

- Communication and collaboration
- Continuous improvement
- Rapid iteration

Pillars of DataOps

- Automation
- e.g. in DevOps: CI/CD
- in DataOps: automated change management (code, configuration, environment, data processing pipelines, data). Use automation using orchestration frameworks such as Apache Airflow.
- Observability and monitoring
- Everything fails all the time
- Find failures before they reach downstream users (ML, analytics, reports, etc.)
- Incident response



## 2.2.5 Orchestration

Manually running each task (ingestion, storage, transformation, serving, etc) might be good for prototyping but not sustainable in the long term.

**Scheduling**

- Orchestration frameworks
- Apache Airflow (most popular today)
- dagster
- prefect
- mage
- Based on Directed Acyclic Graph (DAG)
- Directed: data flows in one direction
- Acyclic: data doesn’t flow backward
- Composed of nodes and edges
- Tasks triggered by events
- Set up monitoring or alerts



## 2.2.6 Software Engineering

The design development, deployment, and maintenance of software applications.

Examples of Languages and Frameworks:

- SQL, Apache Spark, Kafka
- Python, Java, Scala, Bash
- Sometimes even R, Rust, and Go.

Most Common:

- SQL, Python and Bash


