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

**Introduction to Data Modeling and Analytics**

This course covers how to model, transform, and serve data for both analytics and machine learning workloads.

**Course Overview**

- **Week 1: Batch Data Modeling** -- normalization, star schemas, and modeling approaches
- **Week 2: Data modeling and transformation for ML** -- tabular and unstructured data preparation
- **Week 3: Transformation deep-dive** -- distributed processing with Hadoop, Spark, and AWS services
- **Week 4: Build an end-to-end data pipeline** -- serving data for analytics and ML


## 1.1.2 Data Modeling Concepts

**Data Modeling**

Data modeling is the practice of choosing a coherent data structure that aligns with business goals and logic. It has traditionally been used to structure data in warehouses and relational databases. During the data lake 1.0 era, modeling was often ignored, leading to "data swamps." The recommended approach today is **target data modeling**, where you model data for specific business domains.

**Data Model**

A **data model** organizes and standardizes data in a precise, structured representation to enable and guide human and machine behavior, inform decision making, and facilitate actions. For tabular data, this means deciding which tables make up the model, how they relate to each other, and which columns to include.

The key principle is to structure data in a way that connects back to the organization. For analytics, model the data so it is understandable and valuable. For machine learning, model it so it is useful for ML algorithms.

**Good data models:**
- Reflect business goals and logic while incorporating business rules
- Ensure compliance with operational standards and legal requirements
- Outline the relationships between business processes
- Serve as a powerful communication tool, creating a shared language

**Bad data models:**
- Don't reflect how the business operates
- Create more problems than they solve
- Provide stakeholders with inaccurate information and create confusion

**To ensure a good data model:**
- Identify business goals and stakeholder needs
- Define system requirements
- Choose tools and technologies
- Build, evaluate, iterate, and evolve


## 1.1.3 Conceptual, Logical, and Physical Data Models

**Conceptual, Logical, and Physical Data Models**

Data models exist at three levels of abstraction, each adding more implementation detail.

**Conceptual**

A conceptual model describes business entities, relationships, and attributes at a high level. It reflects business logic and rules, and is typically visualized with an **Entity-Relationship Diagram**. Relationship notation on the diagram indicates cardinality:

- `||` means a one-to-one relationship
- The symbol next to `product code` means zero-or-one-to-many
- The symbol next to `orderNumber` means one-to-many
- The relationship can differ based on direction -- the symbol relating to each direction sits at the far end of the line

In the diagram below:
- Each order detail can be associated with **one and only one product**
- Each product can be associated with **zero or many order details**
- Each order detail can be associated with **one and only one order**
- Each order can be associated with **one or many order details**
![](/data-engineering-specialization-website/images/c7b5e1bd-7fbd-454b-854b-e16b560e738a.png)


**Logical Model**

The logical model adds implementation details to the conceptual model, including data types, primary keys, and foreign keys.

**Physical Model**

The physical model specifies how the logical model is implemented in a specific DBMS. This includes configuration details, data storage approach, partitioning, and replication settings.
