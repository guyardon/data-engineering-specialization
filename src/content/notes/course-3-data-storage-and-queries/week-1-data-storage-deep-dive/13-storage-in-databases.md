---
title: "1.3 Storage in Databases"
course: "Course 3: Data Storage and Queries"
courseSlug: "course-3-data-storage-and-queries"
courseOrder: 3
week: "Week 1: Data Storage Deep Dive"
weekSlug: "week-1-data-storage-deep-dive"
weekOrder: 1
order: 3
notionId: "1de969a7-aa01-8031-b2e1-cef9c6db8b8d"
---


## 1.3.1 Database Management Systems

**Introduction**


**Database Management System (DBMS)**

- the software layer for database systems
- both for relational databases or nonrelational databases such as graph databases
- DBMS architecture
- **transport system**
- **query processor**
- **execution engine**
- **storage engine**
  - serialization
  - arrangement of data on disk
  - indexing
    - a data structure that helps you efficiently locate data
    - instead of scanning all rows O(n), we perform binary search O(log n)
  - modern storage engines
    - improved performance on SSDs
    - handle modern data types and structures
    - columnar support for analytical applications

**In-Memory Storage Systems**

- Fast, low latency
- volatile
- use cases: caching, real-time, gaming
- e.g. Key-value stores
- Memcached
  - key value store to cache database query results or API calls
  - used when its acceptable for data to be lost
- Redis
  - key-value store that supports more complex data types
  - supports high performance applications that can tolerate minor data loss


## 1.3.2 Row vs. Column Storage

**Row vs. Column Storage**

- row oriented storage → each row in a table stored as a consecutive sequence of bytes in memory
- good for OLTP (fast read/write, low latency)
- bad for analytical queries (we have to iterate over all columns across rows, when we are are only interested in a single column
- Example:
  - 1 million rows, 30 columns, 100 bytes per entry
  - data transfer speed: 200 mb/s
  - How long would it take to perform the following query:
```sql
SELECT SUM(price)
FROM my_table
```

  - Solution:
    - We would have to iterate over the entire table for row oriented storage to load from disk to RAM
    - 1m x 30 x 100bytes = 3000x1m bytes = 3000 MB
    - transfer time = 3000 MB / 200 MB/s = 15 sec!
- If there were 1 billion rows
  - In row-storage: this would be over 4 hours, not scalable
  - In column storage this would take 8 minutes
    - solution:
    - 1b x 100bytes = 1G x 100 bytes = 1000 M x 100 bytes = 100,000 MB
    - 100,000 MB / 200 MB/s = 500 sec = 8.33 minutes
- column storage
- excellent for OLAP (analytical queries)
- terrible for transactional workloads
