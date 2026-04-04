---
title: "1.2 Normalization"
course: "Course 4: Data Modeling, Transformation, and Serving"
courseSlug: "course-4-data-modeling-transformation-and-serving"
courseOrder: 4
week: "Week 1: Data Modeling & Transformations for Analytics"
weekSlug: "week-1-data-modeling-transformations-for-analytics"
weekOrder: 1
order: 2
notionId: "1f5969a7-aa01-8098-b997-efefcc37a158"
---

## 1.2.1 Normalization Fundamentals

**Normalization** is a data modeling practice typically applied to relational databases to eliminate data redundancy and ensure referential integrity between tables. It was defined by Edgar Codd with two core objectives:

1. Free relations from undesirable insertion, update, and deletion dependencies
2. Reduce the need to restructure relations as new data types are introduced

Consider the difference: in **first normal form**, data lives in a single wide table — updating a customer name requires changing multiple rows, and adding a new column affects every row. In **third normal form**, changing a name means updating a single row in the customers table, and new attributes can be added through dedicated tables.

## 1.2.2 Normal Forms

| Normal Form | Requirements | What It Eliminates |
|---|---|---|
| **Denormalized** | No rules — all data in one table, may contain nested JSON | Nothing — significant redundancy |
| **1NF** | Each column holds a single value, unique primary key exists | Repeating groups and multi-valued columns |
| **2NF** | Meets 1NF + no partial dependencies (non-key columns depend on the full composite key) | Partial dependencies on composite keys |
| **3NF** | Meets 2NF + no transitive dependencies (non-key columns don't depend on other non-key columns) | Transitive dependencies — data is fully **normalized** |

---

**Denormalized Form**

All data sits in one table. Some columns may contain nested JSON. The table contains significant redundancy — the same customer name and address appear on every order row.

---

**1st Normal Form (1NF)**

Each column is unique and holds a single atomic value, and the table has a unique primary key. For example, `order_id` + `order_number` together form the composite primary key.

---

**2nd Normal Form (2NF)**

Builds on 1NF by removing **partial dependencies** — cases where a subset of non-key columns depends on only part of a composite key. However, 2NF can still contain **transitive dependencies** where a non-key column depends on another non-key column. For example, `price` and `name` depend on `sku` in order items, while `customer_name` and `address` depend on `customer_id` in orders.

---

**3rd Normal Form (3NF)**

Meets all 2NF requirements and eliminates transitive dependencies. At this stage, the data is considered **normalized**. Each non-key column depends only on the primary key.

---

**Choosing the Right Level**

The right degree of normalization depends on the use case — there is no one-size-fits-all solution:

| Approach | Advantages | Trade-offs |
|---|---|---|
| **More normalization** | Better data integrity, efficient writes, less redundancy | More joins needed for queries, slower reads |
| **More denormalization** | Faster reads, simpler queries, fewer joins | More redundancy, complex updates, risk of inconsistency |

<img src="/data-engineering-specialization-website/images/diagrams/normalization-steps-dark.svg" alt="Normalization progression from denormalized through 1NF, 2NF, to 3NF" class="diagram diagram-dark" style="max-height: 900px;" />
<img src="/data-engineering-specialization-website/images/diagrams/normalization-steps.svg" alt="Normalization progression from denormalized through 1NF, 2NF, to 3NF" class="diagram diagram-light" style="max-height: 900px;" />
