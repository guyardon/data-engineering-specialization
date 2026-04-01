---
title: "3.3 Joins, Aggregations, and Redshift"
course: "Course 3: Data Storage and Queries"
courseSlug: "course-3-data-storage-and-queries"
courseOrder: 3
week: "Week 3: Queries"
weekSlug: "week-3-queries"
weekOrder: 3
order: 3
notionId: "1e7969a7-aa01-80f3-9892-df23d918832b"
---


## 3.3.1 Joins and Join Methods

**The Join Statement**

- one of the most time consuming query operations
- Example of inner join
- Combines data only from the rows that share a matching customer id from both tables
![](/data-engineering-specialization-website/images/9f861c1e-fd7b-4a70-a34e-e214962ff3a8.png)

**3 Common Methods for Implementing Join**

- **Method 1: Nested Loop Join O(n * m)**
- For each index in big table, scan entire joined table for the corresponding join index
- **Method 2: Index-based Nested Loop **
- (search on B-Tree) - O (n log m)
- For each index in big table, scan for indices in b-tree structure
- **Method 3: Hash-Join**
- uses a hash function to map rows from big table to joined table to buckets based on the value of the join attribute
- O (n * num_buckets), where maybe num_buckets &lt;&lt; m
![](/data-engineering-specialization-website/images/fd73b6a9-7fa8-430a-8e9a-60186ad8f1d6.png)

- More Efficient Queries
- Option 1 : Data needs to normalized in a way that will reduce the number of joins needed later on for analysis and serving. (example: use a fact table and dimension tables)
- Option 2: Use a one-big-table approach
  - No joins needed in downstream tasks

- Challenge: when there are are many-to-many relationships
  - e.g. "order" can be associated with many "payments" but ALSO "payment" can be associated with many "orders"
  - row explosion - when a query returns more rows that what is anticipated
    - check your query to see if it correctly describes what you intended to do
    - e.g. in the above example, add a table that correctly maps "payment" to "orderNumber"

## 3.3.2 Aggregate Queries

**Aggregate Queries**

- Used to compute summary value of a column (e.g. sum, average, max, min, and count of values)

```sql
SELECT MIN(price) from orders


**can either do a full table scan O(n)**

**or faster index-scan on b-tree if available O(log n)**
```

- We can also use GROUP BY in these types of queries which will return multiple rows for each group instead of aggregating the whole table
- partitioning can be done using a sorting algorithm or hash function
- you can use an index to group the rows
```sql
SELECT MIN(price) from orders GROUP BY country
```

- For large dataset, aggregating queries (analytical queries) is faster for columnar storage
- You only transfer the relevant columns from disk to memory, and not all rows


## 3.3.3 Amazon Redshift and Cloud Data Warehouse

**Amazon Redshift and Cloud Data Warehouse**

- Features of Amazon Redshift
- Columnar data storage
  - Stores data column-wise in disk
  - Faster for OLAP workloads/ analytical queries
- Massively parallel processing (MPP)
  - Leader node and multiple compute nodes
  - Each node is responsible for storing a portion of the data and processing queries on that data
  - Each compute node is partitioned into splices
    - Uses a portion of the compute nodes memory and disk space to process a portion of the data assigned to the node
  - Leader node
    - Parses the request
    - Forms an execution plan
    - Compiles code and sends workload to compute nodes
    - Gets results from compute nodes and returns the query result
  - Performance of query
    - Depends on number/ type of nodes
- Data compression
  - Redshift reads compressed data into memory and decompresses it as needed
  - More memory available, and faster queries

Other factors which affect query performance

- Distribution style
- defines how the data is divided across compute nodes
- Two different styles
  - uniform distribution across nodes, improves performance by utilizing resources efficiently by balancing worloads
  - minimize data movement across nodes, which reduces network traffic, reduce query cost, and improve performance
- Styles:
  - AUTO
    - assigns optimal distribution style
  - EVEN
    - round-robin distribution - most appropriate when there are no joins
  - KEY
    - distribute rows based on specific columns
  - ALL
    - full copy of the entire table is distributed to each node - useful for frequently joining smaller tables to a larger table, because it eliminates data shuffling
- Sort Key
- stores data on disk based on a sort key
- helps query optimizer determine optimal query plan, reducing the amount of data that needs to be scanned
- speeds up queries
- sort key for OLAP databases is analogous to how OLTP databases use indexes


## 3.3.4 Additional Query Strategies

**Additional Query Strategy**

- **Leverage Query Caching**
- Running a complex query frequently can be costly
- Many databases allow you to query results
- Query caching can reduce the load on your database and enhance the user experience
- **Prioritize Readability**
- Less likely to contain errors
- Simpler to debug
- Easier to collaborate on
- Use CTEs (temporary results set that you can reference in your query)
- **Vacuuming to Reduce Table Bloat**
- table bloat:
  - the data size on the disk exceeds the actual data size
  - this can happen due to the database keeping outdated blocks in disk storage
  - slow queries
  - suboptimal and inaccurate execution plans
  - inefficient indexes
- Vacuuming
  - removes the dead records
  - critical for relational databases such as PostgreSQL and MySQL
