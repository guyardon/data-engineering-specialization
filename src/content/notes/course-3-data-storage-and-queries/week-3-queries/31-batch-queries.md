---
title: "3.1 Batch Queries"
course: "Course 3: Data Storage and Queries"
courseSlug: "course-3-data-storage-and-queries"
courseOrder: 3
week: "Week 3: Queries"
weekSlug: "week-3-queries"
weekOrder: 3
order: 1
notionId: "1e7969a7-aa01-80f3-9892-df23d918832b"
---

## Overview

- Exploring how the way the data is stored and managed affects
-  the performance of querying the data
- the performance of the storage systems themselves
- **Query Definition**
- A statement that you write in a specific query language to retrieve or act on data. For example:
  - RDBMS: SQL queries
  - Amazon S3: SQL-like queries
  - neo4j Graph DB: Cypher queries
- **Query Languages**
- Declarative language
  - Describes waht data you want to retrieve
  - Execution steps are abstracted from you and handled by the DBMS
    - This doesn't mean we don't need to understand what happens behind the scenes!
- This Week:
- SQL execution behind the scenes
- Techniques to improve query performance (e.g. database index)
- Many SQL queries are applicable to other query languages
- Aggregating queries: columnar vs. row storage
- Queries on streaming data
## Batch Queries

### The Life of a Query

| **Database Management System Layer** | **Query Lifecycle Stage** | **Notes** |
| --- | --- | --- |
| Transport System | Query issued |  |
| Query Processor | Query Parsing + Planning | Query parser

- converts query to tokens
- checks proper syntax
- performs control checks
- converts tokens to bytecode

Query optimizer
- finds an optimal execution plan that uses resources efficiently
- Considers  types of oeprations, presernce of indexes, data scan size
- calculates cost: data transfer i/o cost, computatation and memory usage cost
- picks least expensive plan |
| Execution Engine | Query execution | executes the query |
| Storage Engine |  | stores the results |
