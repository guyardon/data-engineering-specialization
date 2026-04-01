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

## Normalization

- a data modeling practice typically applied to relational databases to remove the redundancy of data within a database and ensure referential integrity between tables
- defined by Edgar Codd, with objectives:
- to free the collection of relations from undesirable insertion, update and deletion dependencies
- to reduce the need for restructuring the collections of relations as new types of data are introduced
- In the example:
- first normal form:
  - sort of a one-big-table
  - to update a customer name, multiple rows need to be changed
  - to add a new column, all rows must be set
- In the third normal form
  - to change a name, change a single row in the customers table
  - to add a new column, add a new table mapping shipment ids, order ids, and ship details
![](/data-engineering-specialization-website/images/a08fb08d-89c7-4a9d-bd31-eb01cbdba83f.png)

### Denormalized Form

- data is in one table
- some columns contain nested json data
- contains redundant data
![](/data-engineering-specialization-website/images/9bd278fb-3329-4ec4-a02b-6b682d98f774.png)

### 1st Normal Form

- Each column must be unique, and have a single value
- Table must have a unique primary key
- In the example, order id + order number create unique primary key
### 2nd Normal Form

- the requirements of 1NF must be met
- partial dependencies must be removed
- a partial dependency is a subset of non-key columns that depend on some columns in the composite key
- Can still contain transitive dependency
- a non-key column depends on another non-key column
- in the example, 
  - in order items: price and name depends on sku
  - in orders: customername and address depend on customer id
![](/data-engineering-specialization-website/images/d501fe47-00c9-4669-bd22-21c5a7fec895.png)

### 3rd Normal Form

- meets all requirements from 2ND
- does not have transitive dependencies
- in this stage the data is considered "Normalized"
![](/data-engineering-specialization-website/images/a52ab7ca-11fa-4a66-b428-1ab80707d8b3.png)

- The degree of normalization depends on use case
- No one-size-fits all solution
- Sometimes denormalization has performance advantages since it doesn't require join operations between table
- normalize form can ensure better read and write operations and better data integrity
