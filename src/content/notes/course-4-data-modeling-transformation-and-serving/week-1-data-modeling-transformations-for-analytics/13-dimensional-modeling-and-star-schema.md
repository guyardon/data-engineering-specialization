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

While normalized models focus on connecting data entities and reducing redundancy, the **star schema** (a dimensional data model) is designed for faster analytical queries and delivers data that is more understandable to business users.

---

**Fact Tables**

A fact table contains **quantitative business measurements** that result from a business event or process. For example, a rideshare order event produces facts like trip duration, price, tip, and delays — all unique to that event.

| Property | Description |
|---|---|
| **Shape** | Narrow and long — few columns but many rows |
| **Mutability** | Immutable (append-only) |
| **Grain** | The level of detail — atomic grain (one event per row) is the most detailed and recommended |

---

**Dimension Tables**

Dimension tables provide the reference data, attributes, and relational context for the events in the fact table. They describe the **who, what, where, and when** of each event. Dimension tables are typically **wide and short** — many descriptive columns but fewer rows.

<img src="/data-engineering-specialization-website/images/diagrams/star-schema-dark.svg" alt="Star schema with central fact table connected to dimension tables" class="diagram diagram-dark" />
<img src="/data-engineering-specialization-website/images/diagrams/star-schema.svg" alt="Star schema with central fact table connected to dimension tables" class="diagram diagram-light" />

## 1.3.2 Fact-Dimension Relationships and Analytical Queries

Fact tables link to dimension tables through **foreign keys**, and each dimension is identified by a **primary key**. Different fact tables from separate star schemas can connect through a shared dimension table, called a **conformed dimension**.

---

**Analytical Queries with Star Schemas**

Star schemas enable aggregate queries (`SUM`, `AVG`, `MAX`, etc.) on fact measures, using dimension tables to filter or group the results. The simple structure means most queries only need one join per dimension — no complex multi-table chains.

## 1.3.3 Designing and Building a Star Schema

Data often starts in normalized form in relational databases but needs to be converted into star schemas for domain-specific data marts.

**4 Key Steps in Designing a Star Schema:**

1. **Select the business process** — identify the operational activity to model (e.g., sales, orders)
2. **Declare the grain** — define the level of detail each fact row represents (atomic is best)
3. **Identify the dimensions** — determine the descriptive context for each event (who, what, where, when)
4. **Identify the facts** — determine the numeric measurements to capture

---

**Surrogate Keys**

Instead of using a natural column as the primary key (e.g., `store_id`), you can define a **surrogate key** — a synthetic identifier generated independently of the source data. Common approaches include auto-incrementing integers or hash functions (e.g., `MD5`).

---

**SQL to Create a Star Schema from Normalized Form**

```sql
-- Create stores dimension with surrogate key
SELECT
    MD5(store_id) AS store_key,
    store_id,
    store_name,
    store_city,
    store_zipcode
FROM stores;

-- Create items dimension with surrogate key
SELECT
    MD5(sku) AS item_key,
    sku,
    name,
    brand
FROM items;

-- Create date dimension from a generated series
SELECT
    date_key,
    EXTRACT(DOW FROM date_key)     AS day_of_week,
    EXTRACT(MONTH FROM date_key)   AS month,
    EXTRACT(QUARTER FROM date_key) AS quarter,
    EXTRACT(YEAR FROM date_key)    AS year
FROM generate_series(
    '2020-01-01'::date,
    '2025-01-01'::date,
    '1 day'::interval
) AS date_key;

-- Create fact table with composite surrogate key and foreign keys
SELECT
    -- Primary key (surrogate, from composite natural key)
    MD5(CONCAT(oi.order_id, oi.item_line_number)) AS fact_order_key,
    -- Natural keys for reference
    oi.order_id,
    oi.item_line_number,
    -- Foreign keys to dimensions
    MD5(o.store_id)     AS store_key,
    MD5(oi.item_sku)    AS item_key,
    o.order_date        AS date_key,
    -- Facts (numeric measurements)
    oi.item_quantity,
    i.price AS item_price
FROM order_items oi
JOIN orders o ON o.order_id = oi.order_id
JOIN items i ON i.sku = oi.item_sku;
```
