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

**Normalization**

Normalization is a data modeling practice typically applied to relational databases to eliminate data redundancy and ensure referential integrity between tables. It was defined by Edgar Codd with two core objectives: freeing relations from undesirable insertion, update, and deletion dependencies, and reducing the need to restructure relations as new data types are introduced.

Consider the difference between first and third normal form. In first normal form, data lives in a single wide table -- updating a customer name requires changing multiple rows, and adding a new column affects every row. In third normal form, changing a name means updating a single row in the customers table, and new attributes can be added through dedicated tables.
![](/data-engineering-specialization-website/images/a08fb08d-89c7-4a9d-bd31-eb01cbdba83f.png)

## 1.2.2 Normal Forms

**Denormalized Form**

In denormalized form, all data sits in one table. Some columns may contain nested JSON data, and the table contains significant redundancy.
![](/data-engineering-specialization-website/images/9bd278fb-3329-4ec4-a02b-6b682d98f774.png)


---

**1st Normal Form**

First normal form requires that each column is unique and holds a single value, and the table has a unique primary key. In the example, `order_id` + `order_number` together form the composite primary key.


---

**2nd Normal Form**

Second normal form builds on 1NF by removing **partial dependencies** -- cases where a subset of non-key columns depends on only some columns in a composite key. However, 2NF can still contain **transitive dependencies**, where a non-key column depends on another non-key column. In the example, `price` and `name` depend on `sku` in order items, while `customername` and `address` depend on `customer_id` in orders.
![](/data-engineering-specialization-website/images/d501fe47-00c9-4669-bd22-21c5a7fec895.png)


---

**3rd Normal Form**

Third normal form meets all 2NF requirements and eliminates transitive dependencies. At this stage, the data is considered **normalized**.
![](/data-engineering-specialization-website/images/a52ab7ca-11fa-4a66-b428-1ab80707d8b3.png)

The right degree of normalization depends on the use case -- there is no one-size-fits-all solution. Denormalization can offer performance advantages by avoiding joins, while normalized form ensures better read/write operations and stronger data integrity.
