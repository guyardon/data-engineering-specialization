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

Beneath every stage of the data engineering lifecycle run a set of cross-cutting concerns - the **undercurrents**. These practices shape how data systems are built, operated, and evolved.

## 2.2.1 Security

Security in data engineering centers on the **principle of least privilege**: give users or applications access to only the essential data and resources they need, and only for the duration required. Adopt a defensive mindset - be cautious with sensitive data and design every system with the assumption that attacks will happen.

## 2.2.2 Data Management

Data management is _"the development, execution, and supervision of plans, programs, and practices that deliver, control, protect, and enhance the value of data and information assets throughout their life cycles."_ At its core, **data governance** ensures the quality, integrity, security, and usability of the data an organization collects.

<img src="/data-engineering-specialization/images/diagrams/data-governance-wheel-dark.svg" alt="Data Management - DAMA Framework" class="diagram diagram-dark" />
<img src="/data-engineering-specialization/images/diagrams/data-governance-wheel.svg" alt="Data Management - DAMA Framework" class="diagram diagram-light" />

<img src="/data-engineering-specialization/images/diagrams/data-quality-dark.svg" alt="Data Quality" class="diagram diagram-dark" />
<img src="/data-engineering-specialization/images/diagrams/data-quality.svg" alt="Data Quality" class="diagram diagram-light" />

## 2.2.3 Data Architecture

Data architecture is _"the design of systems to support the **evolving** **data needs** of an enterprise, achieved by **flexible** and **reversible** decisions reached through a careful **evaluation of trade-offs**."_

On-premises environments make flexible, reversible decisions extremely difficult. Cloud platforms change this equation significantly.

**Principles of Good Architecture:**

<img src="/data-engineering-specialization/images/diagrams/data-architecture-principles-dark.svg" alt="Principles of Good Data Architecture" class="diagram diagram-dark" />
<img src="/data-engineering-specialization/images/diagrams/data-architecture-principles.svg" alt="Principles of Good Data Architecture" class="diagram diagram-light" />

## 2.2.4 DataOps

Just as DevOps improves the development process and quality of software products, **DataOps aims to improve the development process and quality of data products.**

DataOps is a set of cultural habits and practices built on communication, collaboration, continuous improvement, and rapid iteration. Its two main pillars are:

- **Automation** - in DevOps this means CI/CD; in DataOps it means automated change management across code, configuration, environments, and data pipelines, often powered by orchestration frameworks like `Apache Airflow`
- **Observability and monitoring** - everything fails eventually, so the goal is to detect failures before they reach downstream consumers (ML models, analytics dashboards, reports) and have a clear incident response process

<img src="/data-engineering-specialization/images/diagrams/dataops-dark.svg" alt="DataOps" class="diagram diagram-dark" />
<img src="/data-engineering-specialization/images/diagrams/dataops.svg" alt="DataOps" class="diagram diagram-light" />

## 2.2.5 Orchestration

Manually running individual tasks works for prototyping but is unsustainable in production. Orchestration frameworks coordinate the execution of pipeline steps automatically.

**Scheduling**

The most popular orchestration tools today include:

- `Apache Airflow` (industry standard)
- `Dagster`
- `Prefect`
- `Mage`

<div class="tech-logos">
  <div class="tech-logo">
    <img src="/data-engineering-specialization/images/logos/airflow.svg" alt="Apache Airflow" class="logo-light" /><img src="/data-engineering-specialization/images/logos/airflow-dark.svg" alt="Apache Airflow" class="logo-dark" />
    <span>Apache Airflow</span>
  </div>
  <div class="tech-logo">
    <img src="/data-engineering-specialization/images/logos/dagster.svg" alt="Dagster" class="logo-light" /><img src="/data-engineering-specialization/images/logos/dagster-dark.svg" alt="Dagster" class="logo-dark" />
    <span>Dagster</span>
  </div>
  <div class="tech-logo">
    <img src="/data-engineering-specialization/images/logos/prefect.svg" alt="Prefect" class="logo-light" /><img src="/data-engineering-specialization/images/logos/prefect-dark.svg" alt="Prefect" class="logo-dark" />
    <span>Prefect</span>
  </div>
  <div class="tech-logo">
    <img src="/data-engineering-specialization/images/logos/mage.svg" alt="Mage" class="logo-light" /><img src="/data-engineering-specialization/images/logos/mage-dark.svg" alt="Mage" class="logo-dark" />
    <span>Mage</span>
  </div>
</div>

These frameworks model workflows as **Directed Acyclic Graphs (DAGs)** - directed (data flows one way), acyclic (no backward loops), and composed of nodes and edges. Tasks can be triggered by events, and monitoring or alerting is configured alongside them.

<img src="/data-engineering-specialization/images/diagrams/orchestration-dags-dark.svg" alt="Orchestration & DAGs" class="diagram diagram-dark" />
<img src="/data-engineering-specialization/images/diagrams/orchestration-dags.svg" alt="Orchestration & DAGs" class="diagram diagram-light" />

## 2.2.6 Software Engineering

Software engineering - the design, development, deployment, and maintenance of applications - underpins everything a data engineer builds.

Common languages and frameworks span a wide range:

- `SQL`, `Apache Spark`, `Kafka`
- `Python`, `Java`, `Scala`, `Bash`
- Occasionally `R`, `Rust`, and `Go`

In practice, the most common day-to-day tools are `SQL`, `Python`, and `Bash`.

<div class="tech-logos">
  <div class="tech-logo">
    <img src="/data-engineering-specialization/images/logos/python.svg" alt="Python" class="logo-light" /><img src="/data-engineering-specialization/images/logos/python-dark.svg" alt="Python" class="logo-dark" />
    <span>Python</span>
  </div>
  <div class="tech-logo">
    <img src="/data-engineering-specialization/images/logos/java.svg" alt="Java" class="logo-light" /><img src="/data-engineering-specialization/images/logos/java-dark.svg" alt="Java" class="logo-dark" />
    <span>Java</span>
  </div>
  <div class="tech-logo">
    <img src="/data-engineering-specialization/images/logos/scala.svg" alt="Scala" class="logo-light" /><img src="/data-engineering-specialization/images/logos/scala-dark.svg" alt="Scala" class="logo-dark" />
    <span>Scala</span>
  </div>
  <div class="tech-logo">
    <img src="/data-engineering-specialization/images/logos/sql.svg" alt="SQL" class="logo-light" /><img src="/data-engineering-specialization/images/logos/sql-dark.svg" alt="SQL" class="logo-dark" />
    <span>SQL</span>
  </div>
</div>

<img src="/data-engineering-specialization/images/diagrams/software-engineering-dark.svg" alt="Software Engineering for Data" class="diagram diagram-dark" />
<img src="/data-engineering-specialization/images/diagrams/software-engineering.svg" alt="Software Engineering for Data" class="diagram diagram-light" />
