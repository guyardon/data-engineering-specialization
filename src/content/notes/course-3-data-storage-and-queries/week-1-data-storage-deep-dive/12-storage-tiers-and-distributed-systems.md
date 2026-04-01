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


## 1.2.1 Storage Tiers

**Storage Tiers**

Cloud providers organize storage into tiers that trade off access speed against cost. Frequently accessed data lives in hot tiers with low latency, while rarely accessed or archival data moves to cold tiers at a fraction of the price.

![](/data-engineering-specialization-website/images/3663cb24-2c3e-469e-a23b-be24b8313bde.png)

![](/data-engineering-specialization-website/images/f27be8e6-58c4-4ce5-a420-ea04c0bc4c30.png)


## 1.2.2 Distributed Storage Systems

**Distributed Storage Systems**

Distributed storage systems spread data across multiple nodes (magnetic disks or SSDs), replicating it for fault tolerance.

**How distributed storage systems work:**

Each node has its own processing capabilities to handle data management, replication, and access control. A group of nodes forms a **cluster**, which provides higher fault tolerance, high availability, parallel read/write operations, and fast data access. Clusters support **horizontal scaling** — you add more nodes rather than upgrading a single machine's capacity. The total storage capacity is the sum of storage across all individual nodes.

**Many technologies rely on distributed storage architecture.**

**2 Ways to distribute data across nodes:**

**CAP Theorem**
