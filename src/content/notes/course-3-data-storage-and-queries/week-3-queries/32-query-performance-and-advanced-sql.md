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

## Understanding Query Performance

- EXPLAIN command
- Sequence of steps to execute the query
- resource consumption
- performance statistics in each query stage
![](/data-engineering-specialization-website/images/451f5889-b5e5-4f22-af21-e817e978b524.png)

## Advanced SQL Queries

- SELECT DISTINCT
- CASE
- SQL functions
- SQL Booelan Expressions
- Common Table Expressions (CTEs)
- Subqueries
- SQL Window Functions
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

- DISTINCT returns only distinct rows (combination of staff_id, staff_name, and customer_id)
- CONCAT() is a function that concatenates strings
- SUBSTR() extracts the first letter of the first word
- These functions depend on the SQL server being used

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

- Note the Use of CASE-WHEN-THEN-ELSE-END
- Note the use of WHERE and IN
- Note the use of BETWEEN

If we want to perform a query, which produces a table as a result, and then want to perform additional queries on the result of the previous queries, we can use CTEs to define temporary results.

- CTEs start with WITH &lt;cte_name&gt; AS ( &lt;query&gt;)
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

Another example, using 2 chained CTEs

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

Subquery Example

```sql
SELECT film_id, length
FROM dim_film
WHERE length > (SELECT AVG(length) from dim_film)
```

Window Functions

- Allows you to apply an aggregate or ranking function over a particular window or range of rows
- Does not group rows into a single output row: each row remains seperate.
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

## Index Deep Dive

- An index is a separate data structure that has its own disk space and contains information that refers to the actual table
- DBMS's query optimizer checks whether an index is present and if using an index-based plan to execute a query will be more efficient
- Data in indexes is not stored in a table, but rather in blocks, which are linked together which maintains together the order
- The physical location of the blocks does not matter
- The structure facilitates the update of the index when data is inserted or deleted
![](/data-engineering-specialization-website/images/82fb3668-2de5-44b0-87ea-2e1c6b34bdc9.png)

- To retrieve data that has an index structure:
- The Balanced Search Tree (B-Tree) needs to be traversed
  - Number of children nodes are evenly distributed
  - Traversing the tree takes O(log n) time
- If the database does not contain unique elements, once the database finds the leaf node, it needs to traverse horizontally across a chain of leaf nodes to retrieve all rows with a desired index value
  - Can be as expensive as traversing the entire tree
  - Query optimizer checks whether this operation is efficient or not
- Strategy:
- create index structure that will improve the performance of the most performance-sensitive queries
- do not overload the database with many indexes
![](/data-engineering-specialization-website/images/530c0a6a-e128-4b8d-8ff4-80ac187ade10.png)

- Columnar Storage
- The ideas also exist for column-orientated relational databases
- On Amazon RedShift, we can define a sort key on one or more columns
  - sorts the data according to the sort key
  - then stores the sorted data on disk
- On Google BigQuery this is called a cluster key

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

## **Retrieving Only the Data You Need**

- SELECT * FROM order
- Large amounts of data needs to be transferred from disk to memory
- Select * can be expensive for pay-as-you go databases on the cloud
- Instead, use a pruning technique
- Exclude irrelevant data from being scanned in your query
- e.g. row based pruning
```sql
# Use index/cluster key
CREATE INDEX rental_idx
ON payment (rental_id);

# Filter out rows with WHERE
SELECT * from payment
WHERE rental_id = 1;
```

- e.g. column based pruning
```sql
SELECT customer_id, rental_id
FROM payment;
```

- e.g. Partition pruning (scan specific partitions based on a partition key)
![](/data-engineering-specialization-website/images/deacfa3a-5f03-4d86-a5f0-d9a652b6a0f5.png)
