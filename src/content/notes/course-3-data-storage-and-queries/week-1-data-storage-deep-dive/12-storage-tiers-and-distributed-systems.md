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

Cloud providers organize storage into tiers that trade off **access speed** against **cost**. Frequently accessed data lives in hot tiers with low latency, while rarely accessed or archival data moves to cold tiers at a fraction of the price.

|                      | Hot Storage                | Warm Storage                     | Cold Storage                 |
| -------------------- | -------------------------- | -------------------------------- | ---------------------------- |
| **Access frequency** | Very frequent              | Less frequent                    | Infrequent / archive         |
| **Example use case** | Product recommendation app | Regular reports and analyses     | Compliance archives, backups |
| **Storage medium**   | SSD & memory               | Magnetic disks or hybrid systems | Low-cost magnetic disks      |
| **Storage cost**     | High                       | Medium                           | Low                          |
| **Retrieval cost**   | Low                        | Medium                           | High                         |

---

**AWS S3 Storage Classes**

`AWS S3` maps the hot/warm/cold model to specific storage classes, each with different pricing and retrieval characteristics:

<img src="/data-engineering-specialization/images/diagrams/storage-tiers-dark.svg" alt="AWS S3 storage tiers from hot to cold" class="diagram diagram-dark" style="max-height: 900px;" />
<img src="/data-engineering-specialization/images/diagrams/storage-tiers.svg" alt="AWS S3 storage tiers from hot to cold" class="diagram diagram-light" style="max-height: 900px;" />

| Tier | S3 Class                        | Notes                                   |
| ---- | ------------------------------- | --------------------------------------- |
| Hot  | `S3 Express One Zone`           | Single-AZ, lowest latency               |
| Hot  | `S3 Standard`                   | Multi-AZ, general purpose               |
| Warm | `S3 Standard-IA`                | Infrequent access, multi-AZ             |
| Warm | `S3 One Zone-IA`                | Infrequent access, single-AZ (cheaper)  |
| Cold | `S3 Glacier Instant Retrieval`  | Archive with millisecond retrieval      |
| Cold | `S3 Glacier Flexible Retrieval` | Archive with minutes-to-hours retrieval |
| Cold | `S3 Glacier Deep Archive`       | Lowest cost, 12-48 hour retrieval       |

## 1.2.2 Distributed Storage Systems

Distributed storage systems spread data across multiple **nodes** (magnetic disks or SSDs), replicating it for fault tolerance.

**How Distributed Storage Works**

Each node has its own processing capabilities to handle data management, replication, and access control. A group of nodes forms a **cluster**, which provides:

- **Fault tolerance** -- data survives individual node failures
- **High availability** -- the system remains accessible during maintenance or outages
- **Parallel I/O** -- reads and writes spread across nodes for higher throughput
- **Horizontal scaling** -- add more nodes rather than upgrading a single machine

The total storage capacity is the sum of storage across all individual nodes. Many technologies rely on distributed storage, including `HDFS`, `S3`, `Cassandra`, and `Kafka`.

---

**Data Distribution Strategies**

There are two primary strategies for distributing data across nodes:

| Strategy                    | How it works                                  | Tradeoff                                                                        |
| --------------------------- | --------------------------------------------- | ------------------------------------------------------------------------------- |
| **Replication**             | Copy the same data to multiple nodes          | Higher durability and read throughput, but more storage cost and write overhead |
| **Partitioning (sharding)** | Split data into disjoint subsets across nodes | Better write scalability, but queries spanning partitions are more complex      |

<img src="/data-engineering-specialization/images/diagrams/replication-vs-partitioning-dark.svg" alt="Replication vs partitioning data distribution strategies" class="diagram diagram-dark" />
<img src="/data-engineering-specialization/images/diagrams/replication-vs-partitioning.svg" alt="Replication vs partitioning data distribution strategies" class="diagram diagram-light" />

---

**CAP Theorem**

The **CAP theorem** states that a distributed system can guarantee at most **two** of three properties simultaneously:

| Property                | Meaning                                                                 |
| ----------------------- | ----------------------------------------------------------------------- |
| **Consistency**         | Every read returns the most recent write                                |
| **Availability**        | Every request receives a response (even if not the latest data)         |
| **Partition tolerance** | The system continues operating despite network partitions between nodes |

In practice, network partitions are unavoidable in distributed systems, so the real choice is between **consistency** (CP systems like `HBase`, `MongoDB`) and **availability** (AP systems like `Cassandra`, `DynamoDB`).

<img src="/data-engineering-specialization/images/diagrams/cap-theorem-dark.svg" alt="CAP theorem triangle showing consistency, availability, and partition tolerance tradeoffs" class="diagram diagram-dark" />
<img src="/data-engineering-specialization/images/diagrams/cap-theorem.svg" alt="CAP theorem triangle showing consistency, availability, and partition tolerance tradeoffs" class="diagram diagram-light" />
