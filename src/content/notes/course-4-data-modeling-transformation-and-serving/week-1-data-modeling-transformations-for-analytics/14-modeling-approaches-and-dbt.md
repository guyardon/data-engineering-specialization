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

**Inman vs. Kimball Data Modeling Approaches for Data Warehouses**

- The data warehouse was created with the goal of separating the source system from the analytical system
- Data Warehouse Definition:
- A subject-oriented, integrated, non-volatile, and invariant collection of data in support of management's decisions
- The data warehouse contains granular corporate data. Data in the data warehouse is able to be used for many purposes, including sitting and waiting for future requirements which are unknown today


**Inman Modeling Approach**

- store data in the data warehouse in highly normalized 3rd normal form
- provide additional data marts, normalized for specific departments (e.g. in star schemas)
![](/data-engineering-specialization-website/images/365d1881-2ead-431f-a81b-338ce0a55c71.png)


**Kimball Data Modeling Approach**

- serve data that's structured as star schemas directly in the data warehouse
- This allows faster modeling and iteration, but more redundancy
![](/data-engineering-specialization-website/images/3d7abbcc-bd15-45d0-afd7-2f9869953fef.png)


**What to Choose**

- Choose Inman if:
- Data quality is your highest priority
- The analysis requirements are not defined
- Choose Kimball if:
- Quick insights are your highest priority
- Rapid implementation and iteration


## 1.4.2 Data Vault Modeling Approach

**Data Vault Modeling Approach**

- Inmon/Kimball focus on the structure of business logic in the data warehouse
- Data Vault focuses on separating the structural aspects of data (business entities and how they're related to each other)
- Uses seperate tables to represent core business concepts, the relationships between theose concepts, and the descriptive attributes
- Allows flexible, agile and scalable data warehouse structure by keeping the data as closely aligned to the business as possible, even while the business and data are changing
- 3 Layers
- Staging Layer
- Enterprise Data Warehouse Layer
- Information Delivery Layer
- No notion of good, bad or conformed data in a data vault
- Only change the structure in which data is stored
- Allows you to trace the data back to its source
- Helps you avoid restructuring the data when business requirements change

**3 Types of Tables in a Data Vault:**

- Hub: Stores a unique list of business keys
- Business key
- Hash key 
  - calculated as the hash of the business key)
  - used as the Hub primary key
- Load date
  - date which the business key was first loaded
- Record source
  - the source of the business key
- Link: Connects two or more hubs
- Link table connects two or more hubs
- e.g. to connect order and customer hubs, we can use an "order_customer" link table
- Each link must contain:
  - primary and business key from parent hub
  - load date of a row
  - source for the record
  - the primary key is the hash of the business key of the parent hub
- Satellite: Contains attributes that provide context for hubs and links
- Much contain the record source
- Primary key should consist of a hash key of the parent hub and load date
![](/data-engineering-specialization-website/images/6845e8b4-6d09-46b5-b722-4e19a19b3e7f.png)


## 1.4.3 One Big Table and Summary

**One Big Table Modeling Approach**

**Background**

- Inman/Kimball models were developed when data warehouses were expensive, on-premisis, and resource constrained, tightly coupled compute and storage

**One Big Table**

- Wide table (many columns - can be thousands)
- Can be nested, contain various data types
- Highly denormalized
- No need for complex joins
- Supports fast analytical queries

**Why is it Popular**

- Low cost of cloud storage
- Nested data allows for flexible schemas
- Columnar storage helps optimize the storage and processing
- Wide tables are sparse
- Columnar database - reading nulls is free

**Cons**

- You might lose business logic in analytics
- You need complex data structures to store nested data
- Can have poorer update and aggregation performance

**When to Use:**

- A lot of data that needs more flexibility that a traditional data modeling approach might provide


**Summary of Modeling Approaches**

![](/data-engineering-specialization-website/images/2541140f-1fad-477e-9d6f-3da0ced3e7dd.png)

![](/data-engineering-specialization-website/images/01a3268b-5540-4a7b-a579-4726665dd15f.png)


## 1.4.4 DBT

**DBT**

- Warps SQL statemens that create fact/dimension tables with a create statement
- Helps document and validate data within the data warehouse
- dbt core
- open source command line tool
- communicate with your databases through adapters (e.g. dbt-postgres)
- dbt cloud
- runs dbt core in a hosted environment with a browser based interface
