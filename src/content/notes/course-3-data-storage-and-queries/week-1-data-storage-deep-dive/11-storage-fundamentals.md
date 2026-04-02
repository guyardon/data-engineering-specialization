---
title: "1.1 Storage Fundamentals"
course: "Course 3: Data Storage and Queries"
courseSlug: "course-3-data-storage-and-queries"
courseOrder: 3
week: "Week 1: Data Storage Deep Dive"
weekSlug: "week-1-data-storage-deep-dive"
weekOrder: 1
order: 1
notionId: "1de969a7-aa01-8031-b2e1-cef9c6db8b8d"
---

## 1.1.1 Introduction and Storage Hierarchy

**Introduction**

Storage in data engineering spans multiple layers, from physical hardware up through high-level abstractions. Understanding this hierarchy is essential for making informed decisions about cost, performance, and scalability.


---

**Hierarchal View of Storage:**

- **Physical Components** — Magnetic Disks, SSDs, RAM
- **Processes** — CPU, Compression, Networking, Serialization
- **Storage Systems** — Databases, Object Stores, Graph Databases, Vector Databases
  - **OLTP** (Online Transactional Processing) — focused on low-latency read/write queries
  - **OLAP** (Online Analytical Processing) — focused on analytical operations like aggregation and summarization
- **Storage Abstractions** — Data Warehouses, Data Lakes, Data Lakehouses


---

**Course Overview**

**Week 1** covers serialization and compression, physical component characteristics, row vs. column databases, graph and vector databases, cloud storage paradigms (block, object, file), and storage cost-performance trade-offs.

**Week 2** focuses on choosing the right abstraction for storing data.

**Week 3** digs into how queries work, how storage choices affect query performance, and techniques for optimization.

## 1.1.2 Raw Ingredients of Storage Systems

**Raw Ingredients of Storage Systems**

Every storage system is built from a combination of persistent media, volatile memory, and supporting processes.

- **Persistent Storage Mediums**
  - **Magnetic disks** — rotating platters housed in HDDs. Data is addressed by circular tracks and sectors. A read/write head encodes binary data by flipping magnetic field directions. Latency depends on seek time and rotational delay.
  - **SSDs** — store data as electrical charge in flash memory cells. Significantly faster reads and writes than magnetic disks.

- **Distributed processing** — data transfer speed is ultimately limited by network performance.
- **Partitioning** — SSDs can be sliced into partitions for logical separation.

- **Volatile Memory**

|  | **RAM** | **CPU Cache** |  |
| --- | --- | --- | --- |
| Data Transfer Speed | up to 100 GB/sec | up to 1TB/sec | RAM 25X faster than SSD |
| Cost | $3 per GB | / | RAM 30-50 times more expensive than SSD!  |
| Use case | Store the code, and data that the code processes. Not that its volatile, and a power outage can cause data loss. | Located directly on the CPU chip. Useful for ultrafast data fetch (0.1 ns), and super high data transfer speed. Useful for storing browser cache (store downloaded web resources) or database cache (storing results of re-used queries) |  |

- **Processes required for Data Storage**
  - **Networking** — storage systems are typically distributed across many servers, improving read/write performance, durability, and availability.
  - **Serialization** — any data stored in a file, database, or sent over a network must be serialized into a portable format.

![](/data-engineering-specialization-website/images/e732b606-c11f-4fd8-abcc-e5b06758e71e.png)

![](/data-engineering-specialization-website/images/a3cbd75a-12c2-40f8-ad05-061ce03c7700.png)

![](/data-engineering-specialization-website/images/5d8a54ab-dd8c-44d5-bd98-70e5c2608623.png)

Parquet can be up to 100 times faster than CSV, making serialization format choice a major performance lever.

- **Compression**

Compression algorithms reduce redundancy to serialize data more efficiently. Smaller files mean faster queries and less I/O time when loading data from disk.

- **Lossless** — data can be reconstructed bit-for-bit (required for data engineering)
- **Lossy** — some data is permanently discarded (e.g., MP3, JPEG)

Common compression engines:

- **gzip, bzip2** — good for text-based formats (JSON, XML, CSV)
- **Snappy, Zstandard, LZFSE, LZ4** — newer generation, optimized for speed

Two useful encoding techniques for columnar data:

- **Run-length encoding** — repeated values stored as tuples of (value, start index, run length). For example, `[5,5,5,5,4,4,2,2,2,2,2]` becomes `(5,1,4), (4,5,2), (2,7,5)`.
- **Bit-vector encoding** — each distinct value gets a binary vector with a `1` at the indices where it appears.

![](/data-engineering-specialization-website/images/a6508f11-eae2-4537-a198-4c0248a11e68.png)

## 1.1.3 Cloud Storage Options

**Cloud Storage Options**

Cloud providers offer three main storage paradigms, each optimized for different access patterns.


---

**File Storage**

File storage organizes data into a directory tree, where each directory contains metadata (name, owner, permissions, last modified date). A typical path looks like `/home/username/filename.txt`. It is ideal for centralized access to files shared across multiple users or hosts. AWS offers **EFS** (Elastic File System), which handles networking, scaling, and configuration automatically. File storage is often built on top of block storage. The downside is slower read/write performance due to the overhead of maintaining the file hierarchy.


---

**Block Storage**

Block storage divides files into small, fixed-size blocks on disk (magnetic or SSD), each identified by a unique key in a lookup table. Individual blocks can be retrieved and modified efficiently, and blocks can be distributed across multiple disks for higher scalability and durability. This makes block storage ideal for **OLTP** systems that perform frequent, small read/write operations with low latency. It also provides persistent storage to virtual machines like EC2 instances. The default block store for EC2 is **EBS** (Elastic Block Store), which offers SSDs for latency-sensitive workloads and magnetic disks for infrequently accessed data.


---

**Object Storage**

Object storage treats files as **immutable** data objects in a **flat structure** — updating a file means rewriting the entire object. Objects live in a top-level logical container (e.g., an S3 bucket) and are addressed by key: `s3://bucket_name/my_file.json`. Object storage scales horizontally, with each storage node holding its own disk. Objects are distributed across nodes as **shards**, replicated for durability. While it is not suited for small transactional workloads, it excels as the storage layer for cloud data warehouses, data lakes, OLAP systems, and ML pipelines.

![](/data-engineering-specialization-website/images/26e7cc7e-9423-4f54-98e1-db84b58fc835.png)
