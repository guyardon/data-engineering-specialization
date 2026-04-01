---
title: "1.3 Dimensional Modeling and Star Schema"
course: "Course 4: Data Modeling, Transformation, and Serving"
courseSlug: "course-4-data-modeling-transformation-and-serving"
courseOrder: 4
week: "Week 1: Data Modeling & Transformations for Analytics"
weekSlug: "week-1-data-modeling-transformations-for-analytics"
weekOrder: 1
order: 3
notionId: "1f5969a7-aa01-8098-b997-efefcc37a158"
---


## 1.3.1 Star Schema Fundamentals

**Dimensional Modeling - Star Schema**

- Normalized models focus on connecting data entities and modeling the relationships to reduce data redundancy
- Star schema (dimensional data model) focuses on:
- structuring the data for faster analytical queries
- delivers data that is more understandable to business users

**Fact Table**

- contains quantitative business measurements that result from a business event or process
- e.g. business event: order a ride share
  - facts: trip duration, trip price, tip paid, trip delays, etc.
  - these are all unique to the business event
- Each row contains the facts fo a particular event
- Immutable (append only)
- Typically narrow and long (not a lot of columns, but may rows)
- Grain:
- all rides by all customers in one day
- all rides by one customer on one day
- one ride by one customer (atomic grain)
- Atomic grain:
  - most detailed level at which data is capture by a given event

**Dimension Tables**

- Provide the reference data, attributes, and relational context for the event sin the fact table
- Describe the events' who, what, where, and when
- often have many columns (wide and short), i.e. lots of descriptive columns but fewer rows


## 1.3.2 Fact-Dimension Relationships and Analytical Queries

**Relationship between Fact and Dimension Tables**

![](/data-engineering-specialization-website/images/a43dd950-04a8-4625-831b-f1f86c7beb9e.png)

- different fact tables of different star schemas can be connected to each other via a dimension table (called a conformed dimension)
- fact tables are connected to dimension tables through **Foreign Keys**
- each dimension is defined by a **Primary Key**
![](/data-engineering-specialization-website/images/c307c2ba-06fc-4dfe-8357-ca56da6e4e6c.png)

![](/data-engineering-specialization-website/images/bf7b521a-577a-4775-a9d9-c9d91059ec04.png)


**Using Star Schemas to Perform Analytical Queries**

- apply aggregate queries to find sum, average, maximum, etc. of a fact measure in the fact table
- use a dimension table to filter or group the facts
![](/data-engineering-specialization-website/images/b1ecbedb-45aa-427f-83c3-697476ba56ef.png)

![](/data-engineering-specialization-website/images/97b7f8db-4bb3-4545-a51f-de63de50da5e.png)


## 1.3.3 Designing and Building a Star Schema

**From Normalized Model to Star Schema**

- Data can be in normalized form in a relational databases, but may be needed to be converted to star schemas for data specific marts


**4 Key Steps in Designing a Star Schema**

- Select the business process
- Declare the grain (best - atomic)
- Identify the dimensions
- Identify the facts


**Surrogate Keys**

- Sometimes, instead of defining one of the columns as a primary key (e.g. in a stores table, the store_id), we may want to define a new "surrogate key".
- e.g. the store id is a string
- we can do MD5(store_id) to create a surrogate key
- Several ways to do this:
- Create a sequence of integers and assign one integer to each store
- Use a hash function to generate a unique surrogate key
  - supported by many DBMSs like PostgreSQL and MySQL
  - Example: MD5


**SQL Statements to Create a Star Schema from Normalized Form**

![](/data-engineering-specialization-website/images/80a1eb46-5b4a-449f-9d4b-6958c5464219.png)

```sql

**create a stores dimension from the stores table**

**in the normalized form**
SELECT
	MD5(store_id) as store_key,
	store_id,
	store_name,
	store_city,
	store_zipcode,
FROM stores;


**do the same for items dimension**
SELECT
	MD5(sku) as item_key,
	sku,
	name,
	brand
FROM items;


**create a date dimension**
SELECT
	date_key,
	EXTRACT(DAY FROM date_key) AS day_of_week
	EXTRACT(MONTH FROM date_key) AS month
	EXTRACT(quarter FROM date_key) AS quarter
	EXTRACT(year FROM date_key) AS year
FROM
	generate_series('2020-01-01'::date,
									'2025-01-01'::date,
									'1 day'::interval) AS date_key


**create a fact table**

**create a surrogate key by combining two columns and hashing them**
SELECT

**primary key (surrogate, composite)**
	MD5(CONCAT(OrderItems.order_id,
						 OrderItems.item_line_number))
	AS fact_order_key

**for reference, include these**
	OrderItems.order_id,
	OrderItems.item_line_number,

**foreign keys**
	MD5(Orders.store_id) as store_key
	MD5(OrderItems.items_sku) as item_key,
	Orders.order_date AS date_key

**facts**
	OrderItems.item_quantity,
	Items.price AS item_price
FROM OrderItems
JOIN
	Orders ON
	Orders.order_id = OrderItems.order_id
JOIN
	Items ON
	Items.sku = OrderItems.item_sku
```
