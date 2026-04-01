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

While normalized models focus on connecting data entities and reducing redundancy, the **star schema** (a dimensional data model) is designed for faster analytical queries and delivers data that is more understandable to business users.

**Fact Table**

A fact table contains quantitative business measurements that result from a business event or process. For example, a rideshare order event produces facts like trip duration, trip price, tip paid, and trip delays -- all unique to that event. Each row captures the facts of a particular event.

Fact tables are **immutable** (append-only) and typically **narrow and long** -- few columns but many rows. The **grain** defines the level of detail: all rides by all customers in one day, all rides by one customer in one day, or one ride by one customer (the **atomic grain**, which is the most detailed level at which data is captured).

**Dimension Tables**

Dimension tables provide the reference data, attributes, and relational context for the events in the fact table. They describe the **who, what, where, and when** of each event. Dimension tables are often **wide and short** -- many descriptive columns but fewer rows.


## 1.3.2 Fact-Dimension Relationships and Analytical Queries

**Relationship between Fact and Dimension Tables**

![](/data-engineering-specialization-website/images/a43dd950-04a8-4625-831b-f1f86c7beb9e.png)

Different fact tables from separate star schemas can connect to each other through a shared dimension table, called a **conformed dimension**. Fact tables link to dimension tables through **foreign keys**, and each dimension is identified by a **primary key**.
![](/data-engineering-specialization-website/images/c307c2ba-06fc-4dfe-8357-ca56da6e4e6c.png)

![](/data-engineering-specialization-website/images/bf7b521a-577a-4775-a9d9-c9d91059ec04.png)


**Using Star Schemas to Perform Analytical Queries**

Star schemas enable aggregate queries (sum, average, maximum, etc.) on fact measures, using dimension tables to filter or group the results.
![](/data-engineering-specialization-website/images/b1ecbedb-45aa-427f-83c3-697476ba56ef.png)

![](/data-engineering-specialization-website/images/97b7f8db-4bb3-4545-a51f-de63de50da5e.png)


## 1.3.3 Designing and Building a Star Schema

**From Normalized Model to Star Schema**

Data often starts in normalized form in relational databases but needs to be converted into star schemas for domain-specific data marts.

**4 Key Steps in Designing a Star Schema**

1. Select the business process
2. Declare the grain (atomic is best)
3. Identify the dimensions
4. Identify the facts

**Surrogate Keys**

Instead of using a natural column as the primary key (e.g. `store_id`), you can define a **surrogate key** -- a synthetic identifier generated independently of the source data. Common approaches include creating a sequence of integers or using a hash function (e.g. MD5) to generate a unique key. Most DBMSs like PostgreSQL and MySQL support hash-based surrogate keys.

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
