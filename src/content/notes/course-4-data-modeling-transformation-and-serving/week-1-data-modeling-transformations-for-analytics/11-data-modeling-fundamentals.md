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

# Introduction to Data Modeling and Analytics

## Course Overview

**Week 1: Batch Data Modeling**

**Week 2: Data modeling and transformation for ML**

**Week 3: Transformation deep-dive**

**Week 4: Build an end-to-end data pipline**

## **Data Modeling**

- Choosing a coherent data structure that aligns with business goals and logic
- Traditionally used to structure data stored in data warehouses and relational databases
- Was ignored in the data lake 1.0 era, leading to data swamps
- Recommendation: target data modeling approach, where you model data for specific business domains

## **Data Model**

- A data model organizes and standardizes data in a precise structured representation to enable and guide human and machine behavior, inform decision making, and facilitate actions.
- e.g. modeling tabular data
  - what tables make up the model
  - how do the tables relate to each other
  - what columns to choose from each table
- what to look out for
  - structure the data in a way that connects back to the organization. e.g. for analytics - model the data so it is understandable and valuable
  - for machine learning - model the data so it's useful for ml models
- Good Data Models:
- Reflect business goals and logic while incorporating business rules
- Ensure compliance with operational standards and legal requirements
- Outline the relationship between business processes
- Serve as a powerful communication tool, creating a shared language
- Bad Data Models:
- Don't reflect how the business operate
- Create more problems than they solve
- Provide stakeholders with inaccurate information and create confusion
- To Ensure a good data model:
- Identify business goals and stakeholder needs
- Define system requirements
- Choose tools and technologies
- Build, evaluate, iterate and evolve

## Conceptual, Logical, and Physical Data Models

### **Conceptual**

- Describes business entities, relationships, and attributes
- Reflect business logic and rules 
- Visualize with Entity-Relationship Diagram
- In the example:
  - || means 1-1 relationship
  - the symbol next to product code means 0-or-1-to- many
  - the symbol next to orderNumber means 1-to-many
  - The relationship can be different based on the direction 
  - The symbol relating to the direction is on the far end of the line
- in this diagram:
  - order detail can be associated with *one and only one product*
  - each product can be associated with *0 or many products*
  - each *order detail *can be associated with *one and only one order*
  - each *order* can be associated with *one or many order details*
![](/data-engineering-specialization-website/images/c7b5e1bd-7fbd-454b-854b-e16b560e738a.png)

### Logical Model

- details about the implementation of the conceptual model
- data types
- primary and foreign keys
### Physical Model

- Details about the implementation of the logical model in a specific DBMS
- Configuration details
- data storage approach
- partitioning details
- replication details
