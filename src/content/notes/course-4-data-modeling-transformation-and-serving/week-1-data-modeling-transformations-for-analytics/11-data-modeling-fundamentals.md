---
title: "1.1 Data Modeling Fundamentals"
course: "Course 4: Data Modeling, Transformation, and Serving"
courseSlug: "course-4-data-modeling-transformation-and-serving"
courseOrder: 4
week: "Week 1: Data Modeling & Transformations for Analytics"
weekSlug: "week-1-data-modeling-transformations-for-analytics"
weekOrder: 1
order: 1
notionId: "1f5969a7-aa01-8098-b997-efefcc37a158"
---

## 1.1.1 Introduction and Course Overview

This course covers how to model, transform, and serve data for both analytics and machine learning workloads.

| Week       | Topic                    | Focus                                                       |
| ---------- | ------------------------ | ----------------------------------------------------------- |
| **Week 1** | Batch data modeling      | Normalization, star schemas, and modeling approaches        |
| **Week 2** | Data modeling for ML     | Tabular and unstructured data preparation                   |
| **Week 3** | Transformation deep-dive | Distributed processing with Hadoop, Spark, and AWS services |
| **Week 4** | Serving data             | End-to-end pipeline for analytics and ML                    |

## 1.1.2 Data Modeling Concepts

**Data modeling** is the practice of choosing a coherent data structure that aligns with business goals and logic. It has traditionally been used to structure data in warehouses and relational databases. During the data lake 1.0 era, modeling was often ignored, leading to "data swamps." The recommended approach today is **target data modeling** - model data for specific business domains.

A **data model** organizes and standardizes data in a precise, structured representation to enable and guide human and machine behavior, inform decision making, and facilitate actions. For tabular data, this means deciding which tables make up the model, how they relate to each other, and which columns to include.

---

**Good vs. Bad Data Models**

| Good Data Models                                                    | Bad Data Models                                  |
| ------------------------------------------------------------------- | ------------------------------------------------ |
| Reflect business goals and logic while incorporating business rules | Don't reflect how the business operates          |
| Ensure compliance with operational and legal requirements           | Create more problems than they solve             |
| Outline relationships between business processes                    | Provide stakeholders with inaccurate information |
| Serve as a communication tool, creating a shared language           | Generate confusion rather than clarity           |

---

**Building a Good Data Model**

1. Identify business goals and stakeholder needs
2. Define system requirements
3. Choose tools and technologies
4. Build, evaluate, iterate, and evolve

## 1.1.3 Conceptual, Logical, and Physical Data Models

Data models exist at three levels of abstraction, each adding more implementation detail.

| Level          | Description                                                                                    | Contains                                                   |
| -------------- | ---------------------------------------------------------------------------------------------- | ---------------------------------------------------------- |
| **Conceptual** | High-level business entities and relationships, visualized with an Entity-Relationship Diagram | Entities, relationships, cardinality notation              |
| **Logical**    | Adds implementation details to the conceptual model                                            | Data types, primary keys, foreign keys                     |
| **Physical**   | Specifies how the logical model is implemented in a specific DBMS                              | Configuration, storage approach, partitioning, replication |

---

**Entity-Relationship Cardinality**

ER diagrams use notation to express the nature of relationships between entities:

| Notation | Meaning          | Example                                            |
| -------- | ---------------- | -------------------------------------------------- |
| `\|\|`   | One and only one | Each order detail belongs to exactly one order     |
| `\|O`    | Zero or one      | A customer may or may not have a profile           |
| `\|{`    | One or many      | Each order has one or many order details           |
| `O{`     | Zero or many     | Each product appears in zero or many order details |

The symbol at each **end** of the relationship line describes the cardinality from that entity's perspective.
