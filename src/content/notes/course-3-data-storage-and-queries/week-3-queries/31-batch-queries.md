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

How data is stored and managed directly affects both query performance and the performance of the storage systems themselves. This week explores those relationships.

---

**Query Definition**

A **query** is a statement written in a specific query language to retrieve or act on data. Examples include SQL queries against an RDBMS, SQL-like queries against `Amazon S3`, and Cypher queries against a `Neo4j` graph database.

---

**Query Languages**

SQL and its relatives are **declarative** — you describe _what_ data you want, and the DBMS handles the execution steps. That abstraction does not mean you can ignore what happens behind the scenes, though. This week covers:

- SQL execution behind the scenes
- Techniques to improve query performance (e.g., database indexes)
- How aggregating queries behave differently on columnar vs. row storage
- Queries on streaming data

## 3.1.2 The Life of a Query

A batch query travels through several stages within the DBMS before returning results.

<img src="/data-engineering-specialization/images/diagrams/query-lifecycle-dark.svg" alt="Query lifecycle stages from transport through storage engine" class="diagram diagram-dark" style="max-height: 900px;" />
<img src="/data-engineering-specialization/images/diagrams/query-lifecycle.svg" alt="Query lifecycle stages from transport through storage engine" class="diagram diagram-light" style="max-height: 900px;" />

| Stage               | Component        | What Happens                                                                                                                                                                                 |
| ------------------- | ---------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **1. Transport**    | Network layer    | Client sends the SQL query over a network connection to the DBMS                                                                                                                             |
| **2. Parsing**      | Query parser     | Tokenizes the query, checks syntax, validates access permissions, compiles tokens to bytecode                                                                                                |
| **3. Optimization** | Query optimizer  | Evaluates candidate execution plans — considers operation types, index availability, data scan size — calculates the cost of each (I/O, computation, memory) and selects the least expensive |
| **4. Execution**    | Execution engine | Executes the chosen plan against the storage layer                                                                                                                                           |
| **5. Storage**      | Storage engine   | Reads/writes data blocks on disk and returns results back up the chain                                                                                                                       |
