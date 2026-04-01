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

**Inmon vs. Kimball Data Modeling Approaches for Data Warehouses**

The data warehouse was created to separate source systems from analytical systems. Bill Inmon defined it as a **subject-oriented, integrated, non-volatile, and invariant collection of data** in support of management's decisions. It contains granular corporate data that can serve many purposes, including future requirements that are unknown today.

**Inmon Modeling Approach**

The Inmon approach stores data in the warehouse in highly **normalized third normal form**, then provides additional data marts (often as star schemas) for specific departments.
![](/data-engineering-specialization-website/images/365d1881-2ead-431f-a81b-338ce0a55c71.png)


**Kimball Data Modeling Approach**

The Kimball approach serves data structured as **star schemas directly in the data warehouse**. This enables faster modeling and iteration, but introduces more redundancy.
![](/data-engineering-specialization-website/images/3d7abbcc-bd15-45d0-afd7-2f9869953fef.png)


**What to Choose**

- Choose **Inmon** if data quality is your highest priority or analysis requirements are not yet defined.
- Choose **Kimball** if quick insights are your highest priority and you need rapid implementation and iteration.


## 1.4.2 Data Vault Modeling Approach

**Data Vault Modeling Approach**

While Inmon and Kimball focus on how business logic is structured in the warehouse, **Data Vault** focuses on separating the structural aspects of data -- business entities and their relationships. It uses separate tables for core business concepts, the relationships between them, and descriptive attributes. This separation keeps the warehouse flexible, agile, and scalable even as the business and its data evolve.

Key characteristics of Data Vault:
- Three layers: Staging, Enterprise Data Warehouse, and Information Delivery
- No notion of "good," "bad," or "conformed" data -- it only changes the storage structure
- Full traceability back to source systems
- Minimal restructuring when business requirements change

**3 Types of Tables in a Data Vault:**

- **Hub**: Stores a unique list of business keys, along with a hash key (used as the primary key), load date (when the key was first loaded), and record source.
- **Link**: Connects two or more hubs. For example, an `order_customer` link table connects the order and customer hubs. Each link contains primary and business keys from parent hubs, a load date, and a record source. The primary key is the hash of the parent hub's business key.
- **Satellite**: Contains descriptive attributes that provide context for hubs and links. Its primary key consists of the parent hub's hash key and the load date, plus the record source.
![](/data-engineering-specialization-website/images/6845e8b4-6d09-46b5-b722-4e19a19b3e7f.png)


## 1.4.3 One Big Table and Summary

**One Big Table Modeling Approach**

**Background**

The Inmon and Kimball models were developed when data warehouses were expensive, on-premises, and resource-constrained, with tightly coupled compute and storage. Modern cloud infrastructure has changed the calculus.

**One Big Table**

The One Big Table approach uses a single **wide table** (potentially thousands of columns) that is highly denormalized. It can contain nested and varied data types, requires no complex joins, and supports fast analytical queries.

**Why is it Popular**

- Low cost of cloud storage
- Nested data allows flexible schemas
- Columnar storage optimizes both storage and processing
- Wide tables are sparse, and in columnar databases reading nulls is free

**Cons**

- Business logic can get lost in analytics
- Complex data structures are needed to store nested data
- Update and aggregation performance can suffer

**When to Use:**

One Big Table works well when you have a large volume of data that needs more flexibility than traditional modeling approaches provide.

**Summary of Modeling Approaches**

![](/data-engineering-specialization-website/images/2541140f-1fad-477e-9d6f-3da0ced3e7dd.png)

![](/data-engineering-specialization-website/images/01a3268b-5540-4a7b-a579-4726665dd15f.png)


## 1.4.4 DBT

**DBT**

**dbt** (data build tool) wraps SQL statements that create fact and dimension tables with a `CREATE` statement, and helps document and validate data within the data warehouse.

- **dbt core**: An open-source command-line tool that communicates with databases through adapters (e.g. `dbt-postgres`).
- **dbt cloud**: Runs dbt core in a hosted environment with a browser-based interface.
