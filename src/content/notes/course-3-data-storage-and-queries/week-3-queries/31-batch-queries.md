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

## 3.1.1 Query Fundamentals

**Overview**

How data is stored and managed directly affects both query performance and the performance of the storage systems themselves. This week explores those relationships.


---

**Query Definition**

A **query** is a statement written in a specific query language to retrieve or act on data. Examples include SQL queries against an RDBMS, SQL-like queries against Amazon S3, and Cypher queries against a Neo4j graph database.


---

**Query Languages**

SQL and its relatives are **declarative** — you describe *what* data you want, and the DBMS handles the execution steps. That abstraction does not mean you can ignore what happens behind the scenes, though. This week covers:

- SQL execution behind the scenes
- Techniques to improve query performance (e.g., database indexes)
- How aggregating queries behave differently on columnar vs. row storage
- Queries on streaming data

## 3.1.2 The Life of a Query

**Batch Queries**

A batch query travels through several stages within the DBMS before returning results.


---

**The Life of a Query**

| **Database Management System Layer** | **Query Lifecycle Stage** | **Notes** |
| --- | --- | --- |
| Transport System | Query issued |  |
| Query Processor | Query Parsing + Planning | The **query parser** converts the query to tokens, checks syntax, performs control checks, and compiles tokens to bytecode. The **query optimizer** then evaluates candidate execution plans — considering operation types, index availability, and data scan size — calculates the cost of each (I/O, computation, memory), and selects the least expensive plan. |
| Execution Engine | Query execution | Executes the chosen plan. |
| Storage Engine |  | Stores the results. |
