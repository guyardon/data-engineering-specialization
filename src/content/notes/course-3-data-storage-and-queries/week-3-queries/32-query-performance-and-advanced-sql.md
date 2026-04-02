---
title: "3.2 Query Performance and Advanced SQL"
course: "Course 3: Data Storage and Queries"
courseSlug: "course-3-data-storage-and-queries"
courseOrder: 3
week: "Week 3: Queries"
weekSlug: "week-3-queries"
weekOrder: 3
order: 2
notionId: "1e7969a7-aa01-80f3-9892-df23d918832b"
---

## 3.2.1 Understanding Query Performance

**Understanding Query Performance**

The **EXPLAIN** command reveals the execution plan the DBMS has chosen for a query — the sequence of steps, resource consumption, and performance statistics at each stage. It is the primary tool for diagnosing slow queries.

![](/data-engineering-specialization-website/images/451f5889-b5e5-4f22-af21-e817e978b524.png)

## 3.2.2 Advanced SQL Queries

**Advanced SQL Queries**

Beyond basic SELECT/FROM/WHERE, SQL offers several powerful constructs for shaping data: **SELECT DISTINCT**, **CASE** expressions, **SQL functions**, **boolean expressions**, **Common Table Expressions (CTEs)**, **subqueries**, and **window functions**.

```sql

# DATA Manipulation Operations
CREATE
INSERT INTO
UPDATE
DELETE


# COMMON SQL COMMANDS
SELECT
COUNT(), SUM(), AVG(), MIN(), MAX()
FROM
JOIN
WHERE
GROUP BY
ORDER BY
LIMIT
```

Simple Example:

```sql
SELECT DISTINCT
	fact_rental.staff_id,
	CONCAT(dim_staff.first_name, ' ', SUBSTR(dim_staff.last_name, 1, 1) AS staff_name,
	fact_rental.customer_id,
FROM fact_rental
JOIN dim_staff ON fact_rental.staff_id = dim_staff.staff_id;
```

**DISTINCT** returns only unique combinations of the selected columns. **CONCAT()** concatenates strings, and **SUBSTR()** extracts a substring — both are server-specific functions.

Another Example

```sql
SELECT
	fact_rental.customer_id,
	fact_rental.rental_id,
	(CASE
		WHEN payment_date < return_date THEN 1
		ELSE 0
	 END) AS on_time_payment
FROM fact_rental
JOIN dim_customer
	ON dim_customer.customer_id = fact_rental.customer_id
WHERE dim_customer.country IN ("United States", "Canada")
	AND (fact_rental.rental_date BETWEEN "2005-05-24" and "2005-07-26")
LIMIT 5;
```

This query uses **CASE-WHEN-THEN-ELSE-END** to create a computed column, **IN** to filter on a set of values, and **BETWEEN** for range filtering.

**Common Table Expressions (CTEs)** let you define temporary result sets that subsequent queries can reference. They start with `WITH <cte_name> AS (<query>)` and are especially useful for breaking complex queries into readable steps.

```sql
WITH staff_customer_pairs AS (
	SELECT DISTINCT
		fact_rental.staff_id,
		CONCAT(dim_staff.first_name, ' ', SUBSTR(dim_staff.last_name, 1, 1) AS staff_name,
		fact_rental.customer_id,
	FROM fact_rental
	JOIN dim_staff ON fact_rental.staff_id = dim_staff.staff_id;
)
SELECT staff_name, COUNT(customer_id)
FROM staff_customer_pairs
GROUP BY staff_name
```

CTEs can be chained — the output of one feeds into the next:

```sql
WITH customer_payment_info AS (
	SELECT
		fact_rental.customer_id,
		fact_rental.rental_id,
		(CASE
			WHEN payment_date < return_date THEN 1
			ELSE 0
		 END) AS on_time_payment
	FROM fact_rental
	JOIN dim_customer
		ON dim_customer.customer_id = fact_rental.customer_id
	WHERE dim_customer.country IN ("United States", "Canada")
		AND (fact_rental.rental_date BETWEEN "2005-05-24" and "2005-07-26")
), customer_percent_on_time_payment AS (
	SELECT
		customer_id,
		AVG(on_time_payment) AS percent_on_time_payment
	FROM customer_payment_info
	GROUP BY customer_id
)
SELECT MAX(percent_on_time_payment)
FROM customer_percent_on_time_payment
```

**Subqueries** embed a query inside another query, useful for simple filtering:

```sql
SELECT film_id, length
FROM dim_film
WHERE length > (SELECT AVG(length) from dim_film)
```

**Window Functions** apply aggregate or ranking functions over a sliding range of rows without collapsing them into a single output — each row remains separate.

```sql

# Subquery Template
SELECT column_name1,
ranking_function() OVER (
	PARTITION BY column_name1
	ORDER BY column_name3
) AS new_column
FROM table_name;


# example of ranking functions:
rank()
row_number()
```

Window Function Example

```sql

# lets start with a query
SELECT
fact_rental.customer_id,
dim_category.name,
avg(datediff(return_date, rental_date)) AS average_rental_days
FROM fact_rental
JOIN dim_category
ON fact_rental.category_id = dim_category.category_id
GROUP BY fact_rental.customer_id, dim_category.name
ORDER BY fact_rental.customer_id, average_rental_days DESC


# now convert the query to a CTE
WITH customer_info as (

# <previous query here>
)
SELECT
	customer_id,
	name,
	average_rental_days

# now comes the window function
rank() over (
	PARTITION BY customer_id
	ORDER BY average_rental_days DESC
)
AS rank_category
FROM customer_info
ORDER BY
	customer_id,
	rank category
```

## 3.2.3 Index Deep Dive

**Index Deep Dive**

An **index** is a separate data structure with its own disk space that contains references back to the actual table. The DBMS query optimizer checks whether an index exists and whether an index-based plan would be more efficient than a full scan.

Index data is stored in **blocks** linked together to maintain order — the physical location of these blocks on disk does not matter. This linked structure also makes it efficient to update the index when rows are inserted or deleted.

![](/data-engineering-specialization-website/images/82fb3668-2de5-44b0-87ea-2e1c6b34bdc9.png)

To retrieve indexed data, the DBMS traverses a **Balanced Search Tree (B-Tree)** where children are evenly distributed, giving O(log n) lookup time. If the indexed column contains non-unique values, the search may need to traverse a chain of leaf nodes horizontally — potentially as expensive as scanning the full tree. The query optimizer evaluates whether this trade-off is worthwhile.

The strategy: create indexes that improve performance of your most critical queries, but avoid overloading the database with too many indexes.

![](/data-engineering-specialization-website/images/530c0a6a-e128-4b8d-8ff4-80ac187ade10.png)

**Columnar Storage** applies the same ideas. On `Amazon Redshift`, you define a **sort key** on one or more columns — data is sorted by that key and stored on disk accordingly. On **Google BigQuery**, the equivalent is a **cluster key**.

Example:

```sql

# will perform index scan since employee_id

# is defined as the primary key for this table
EXPLAIN
SELECT first_name, last_name
FROM employees
WHERE employee_id = 123
```

```sql

# orderdetails table has a *composite* primary key

# (productcode, ordernumber)

# the index is created on the productcode column

# *since its defined first*

# because of the mismatch between the index

# and the primary key, the DBMS will perform

# a full table scan on orderdetails (seq scan)
EXPLAIN
SELECT productcode, priceeach
FROM orderdetails
WHERE ordernumber = 10101


# if we choose the *composite* primary key

# to be (ordernumber, productcode)

# since ordernumber is first, the DBMS

# will create an index on ordernumber (since its first)

# and filtering based on it will use the index.
```

## 3.2.4 Retrieving Only the Data You Need

**Retrieving Only the Data You Need**

Running `SELECT * FROM orders` forces large amounts of data to be transferred from disk to memory and can be expensive on pay-as-you-go cloud databases. Instead, use **pruning techniques** to exclude irrelevant data from being scanned.

**Row-based pruning** — filter rows using indexes or WHERE clauses:

```sql

# Use index/cluster key
CREATE INDEX rental_idx
ON payment (rental_id);


# Filter out rows with WHERE
SELECT * from payment
WHERE rental_id = 1;
```

**Column-based pruning** — select only the columns you need:

```sql
SELECT customer_id, rental_id
FROM payment;
```

**Partition pruning** — scan only specific partitions based on a partition key:

![](/data-engineering-specialization-website/images/deacfa3a-5f03-4d86-a5f0-d9a652b6a0f5.png)
