---
title: "4.1 Serving Data and Analytics"
course: "Course 4: Data Modeling, Transformation, and Serving"
courseSlug: "course-4-data-modeling-transformation-and-serving"
courseOrder: 4
week: "Week 4: Serving Data and Analytics for Machine Learning"
weekSlug: "week-4-serving-data-and-analytics-for-machine-learning"
weekOrder: 4
order: 1
notionId: "20a969a7-aa01-800d-8146-c81f183ff15e"
---

## 4.1.1 Serving Data for Analytics and ML

The final stage of the data engineering lifecycle is **serving** - delivering processed data to downstream consumers for analytics and machine learning.

---

**Analytical Use Cases**

| Use Case                  | Description                                                                            |
| ------------------------- | -------------------------------------------------------------------------------------- |
| **Business Intelligence** | Dashboards and reports for strategic decision-making                                   |
| **Operational Analytics** | Monitoring data to inform immediate action, served within required latency constraints |
| **Embedded Analytics**    | Client-facing data products or dashboards                                              |

---

**Machine Learning Use Cases**

The primary end users are data scientists and ML engineers. The data engineer's role is to acquire, transform, and deliver the data necessary for model training.

---

**Ways to Serve Data**

| Method                | Description                                                                                            |
| --------------------- | ------------------------------------------------------------------------------------------------------ |
| **Table**             | Physical storage of data - queries read directly from disk/memory                                      |
| **View**              | A saved SQL query that runs on demand - always returns fresh results but recomputes every time         |
| **Materialized View** | A pre-computed snapshot of a query result stored physically - fast reads but requires periodic refresh |

---

**How Data Scientists Accept Data**

| Delivery Method                 | Details                                                                                                                      |
| ------------------------------- | ---------------------------------------------------------------------------------------------------------------------------- |
| **As files**                    | Text files for language modeling, Parquet/CSV for tabular ML, image formats for computer vision - common for ad hoc requests |
| **From databases / warehouses** | Access via SQL queries with schema enforcement, fine-grained permissions, and high query performance                         |
| **From streaming systems**      | Real-time data delivery for low-latency analytics across both historical and current data                                    |

---

**Semantic Layer**

A **semantic layer** documents definitions, derives business metrics, and creates a common language for data across the organization. It ensures correctness, consistency, and trustworthiness through clear data definitions (column names) and data logic (formulas for deriving metrics).

## 4.1.2 Views and Materialized Views

| Property        | View                                              | Materialized View                               |
| --------------- | ------------------------------------------------- | ----------------------------------------------- |
| **Storage**     | No physical storage - query runs on demand        | Pre-computed result stored on disk              |
| **Freshness**   | Always up-to-date (recomputes on every query)     | Stale until refreshed (manual or scheduled)     |
| **Performance** | Slower for complex queries (recomputes each time) | Fast reads - serves pre-computed results        |
| **Use case**    | Simple transformations, access control layers     | Expensive aggregations queried frequently       |
| **Maintenance** | None - just a saved SQL definition                | Requires refresh strategy (incremental or full) |

<img src="/data-engineering-specialization/images/diagrams/views-vs-materialized-dark.svg" alt="View recomputes SQL on every query vs materialized view reads cached result" class="diagram diagram-dark" style="max-height: 900px;" />
<img src="/data-engineering-specialization/images/diagrams/views-vs-materialized.svg" alt="View recomputes SQL on every query vs materialized view reads cached result" class="diagram diagram-light" style="max-height: 900px;" />

```sql
-- Create a view: recomputes on every query
CREATE VIEW daily_sales AS
SELECT order_date, SUM(amount) AS total
FROM fact_orders
GROUP BY order_date;

-- Create a materialized view: pre-computed, needs refresh
CREATE MATERIALIZED VIEW daily_sales_mv AS
SELECT order_date, SUM(amount) AS total
FROM fact_orders
GROUP BY order_date;

-- Refresh the materialized view when underlying data changes
REFRESH MATERIALIZED VIEW daily_sales_mv;
```
