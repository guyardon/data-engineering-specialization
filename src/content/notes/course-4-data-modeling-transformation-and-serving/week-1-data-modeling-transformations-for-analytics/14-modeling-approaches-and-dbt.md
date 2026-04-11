---
title: "1.4 Advanced Modeling Approaches"
course: "Course 4: Data Modeling, Transformation, and Serving"
courseSlug: "course-4-data-modeling-transformation-and-serving"
courseOrder: 4
week: "Week 1: Data Modeling & Transformations for Analytics"
weekSlug: "week-1-data-modeling-transformations-for-analytics"
weekOrder: 1
order: 4
notionId: "1f5969a7-aa01-8098-b997-efefcc37a158"
---

## 1.4.1 Inmon vs. Kimball Modeling Approaches

The data warehouse was created to separate source systems from analytical systems. Two foundational approaches define how data should be structured inside the warehouse.

---

**Inmon Approach**

Stores data in the warehouse in highly **normalized third normal form**, then provides additional data marts (often as star schemas) for specific departments.

- Source systems → 3NF warehouse → Star schema data marts → Business users
- Prioritizes **data quality and consistency** - single source of truth
- Slower to set up, but more robust and flexible long-term

---

**Kimball Approach**

Serves data structured as **star schemas directly in the data warehouse**, skipping the normalized intermediate layer.

- Source systems → Star schema warehouse → Business users
- Prioritizes **speed of delivery** - faster modeling and iteration
- Introduces more redundancy, but simpler for business users to query

---

**When to Choose**

| Scenario                                   | Recommended Approach |
| ------------------------------------------ | -------------------- |
| Data quality is the highest priority       | **Inmon**            |
| Analysis requirements are not yet defined  | **Inmon**            |
| Quick insights and rapid iteration needed  | **Kimball**          |
| Small team with limited modeling resources | **Kimball**          |

<img src="/data-engineering-specialization/images/diagrams/inmon-vs-kimball-dark.svg" alt="Inmon top-down vs Kimball bottom-up warehouse data flow" class="diagram diagram-dark" style="max-height: 900px;" />
<img src="/data-engineering-specialization/images/diagrams/inmon-vs-kimball.svg" alt="Inmon top-down vs Kimball bottom-up warehouse data flow" class="diagram diagram-light" style="max-height: 900px;" />

## 1.4.2 Data Vault Modeling Approach

While Inmon and Kimball focus on how business logic is structured in the warehouse, **Data Vault** focuses on separating the structural aspects of data - business entities and their relationships. This separation keeps the warehouse flexible, agile, and scalable even as the business evolves.

**Key characteristics:**

- Three layers: Staging → Enterprise Data Warehouse → Information Delivery
- No notion of "good," "bad," or "conformed" data - only changes the storage structure
- Full traceability back to source systems
- Minimal restructuring when business requirements change

---

**3 Types of Tables in a Data Vault**

| Table Type    | Purpose                                                                 | Key Columns                                                           |
| ------------- | ----------------------------------------------------------------------- | --------------------------------------------------------------------- |
| **Hub**       | Stores a unique list of business keys (core entities)                   | Hash key (PK), business key, load date, record source                 |
| **Link**      | Connects two or more hubs (relationships between entities)              | Hash key (PK), parent hub hash keys, load date, record source         |
| **Satellite** | Contains descriptive attributes that provide context for hubs and links | Parent hash key + load date (composite PK), attributes, record source |

For example, an `order_customer` link table connects the order and customer hubs. The link's primary key is the hash of the combined parent business keys.

## 1.4.3 One Big Table and Summary

The Inmon and Kimball models were developed when warehouses were expensive, on-premises, and resource-constrained with tightly coupled compute and storage. Modern cloud infrastructure has changed the calculus.

---

**One Big Table**

The One Big Table approach uses a single **wide table** (potentially thousands of columns) that is highly denormalized. It can contain nested and varied data types, requires no complex joins, and supports fast analytical queries.

| Advantages                                | Disadvantages                                 |
| ----------------------------------------- | --------------------------------------------- |
| Low storage cost on cloud columnar stores | Business logic can get lost in analytics      |
| Nested data allows flexible schemas       | Complex data structures for nested data       |
| Reading nulls in columnar storage is free | Update and aggregation performance can suffer |
| No joins needed - simpler queries         | Harder to maintain data integrity             |

Works well when you have a large volume of data that needs more flexibility than traditional modeling approaches provide.

---

**Summary of Modeling Approaches**

<img src="/data-engineering-specialization/images/diagrams/modeling-approaches-dark.svg" alt="Four modeling approaches compared: Inmon, Kimball, Data Vault, One Big Table" class="diagram diagram-dark" />
<img src="/data-engineering-specialization/images/diagrams/modeling-approaches.svg" alt="Four modeling approaches compared: Inmon, Kimball, Data Vault, One Big Table" class="diagram diagram-light" />

## 1.4.4 dbt (Data Build Tool)

<img class="tech-logo-aside logo-light" src="/data-engineering-specialization/images/logos/dbt.svg" alt="dbt" /><img class="tech-logo-aside logo-dark" src="/data-engineering-specialization/images/logos/dbt-dark.svg" alt="dbt" />

`dbt` (data build tool) wraps SQL statements that create fact and dimension tables with a `CREATE` statement.

---

It helps document and validate data within the data warehouse.

| Variant       | Description                                                                                                   |
| ------------- | ------------------------------------------------------------------------------------------------------------- |
| **dbt Core**  | Open-source CLI tool that communicates with databases through adapters (e.g., `dbt-postgres`, `dbt-redshift`) |
| **dbt Cloud** | Hosted environment with a browser-based interface that runs dbt Core under the hood                           |

`dbt` enables version-controlled, testable, and documented data transformations - treating SQL-based modeling like software engineering.
