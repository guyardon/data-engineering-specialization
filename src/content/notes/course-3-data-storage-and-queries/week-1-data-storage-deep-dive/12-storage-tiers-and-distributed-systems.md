---
title: "1.2 Storage Tiers and Distributed Systems"
course: "Course 3: Data Storage and Queries"
courseSlug: "course-3-data-storage-and-queries"
courseOrder: 3
week: "Week 1: Data Storage Deep Dive"
weekSlug: "week-1-data-storage-deep-dive"
weekOrder: 1
order: 2
notionId: "1de969a7-aa01-8031-b2e1-cef9c6db8b8d"
---

## Storage Tiers

![](/data-engineering-specialization-website/images/3663cb24-2c3e-469e-a23b-be24b8313bde.png)

![](/data-engineering-specialization-website/images/f27be8e6-58c4-4ce5-a420-ea04c0bc4c30.png)

## Distributed Storage Systems

**How distributed storage systems work:**

- Data is <u>distributed</u> and <u>replicated</u> across nodes (Magnetic disks or SSDs)
- Each node has processing capabilities to handle
- data mangement
- replication
- access control
- Groups of nodes are a cluster:
- higher fault tolerance and data durability
- high availability
- process many read/write operations in parallel
- fast data access
- More nodes can be added to a cluster (horizontal scaling)
- In a single machine we can only achieve vertical scaling by upgrading the storage capacity
- The total storage capacity is the sum of the storage in each individual node

**Many technologies rely on distributed storage architecture:**

**2 Ways to distribute data across nodes:**

**CAP Theorem**
