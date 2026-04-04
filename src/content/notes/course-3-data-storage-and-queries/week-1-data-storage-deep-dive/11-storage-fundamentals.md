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

Storage in data engineering spans multiple layers, from physical hardware up through high-level abstractions. Understanding this hierarchy is essential for making informed decisions about cost, performance, and scalability.

<img src="/data-engineering-specialization-website/images/diagrams/storage-hierarchy-dark.svg" alt="Storage hierarchy from physical components to abstractions" class="diagram diagram-dark" style="max-height: 900px;" />
<img src="/data-engineering-specialization-website/images/diagrams/storage-hierarchy.svg" alt="Storage hierarchy from physical components to abstractions" class="diagram diagram-light" style="max-height: 900px;" />

| Layer | Components | Role |
|---|---|---|
| **Physical Components** | Magnetic disks, SSDs, RAM, CPU cache | The raw hardware that stores and retrieves bits |
| **Processes** | Serialization, compression, networking, CPU | Transform data between formats and move it between systems |
| **Storage Systems** | OLTP databases, OLAP databases, object stores, graph/vector DBs | Organize and manage data for specific access patterns |
| **Storage Abstractions** | Data warehouses, data lakes, data lakehouses | High-level paradigms built on top of storage systems |

---

**Course Overview**

**Week 1** covers serialization and compression, physical component characteristics, row vs. column databases, graph and vector databases, cloud storage paradigms (block, object, file), and storage cost-performance trade-offs.

**Week 2** focuses on choosing the right abstraction for storing data.

**Week 3** digs into how queries work, how storage choices affect query performance, and techniques for optimization.

## 1.1.2 Raw Ingredients of Storage Systems

Every storage system is built from a combination of **persistent media**, **volatile memory**, and supporting **processes**.

**Persistent Storage**

| Medium | How it works | Characteristics |
|---|---|---|
| **Magnetic disks (HDD)** | Rotating platters with a read/write head that encodes binary data by flipping magnetic field directions | Data addressed by circular tracks and sectors. Latency depends on seek time and rotational delay. Cheapest per GB. |
| **SSDs** | Store data as electrical charge in flash memory cells | Significantly faster reads and writes than HDDs. Can be partitioned for logical separation. |

**Volatile Memory**

| | RAM | CPU Cache |
|---|---|---|
| **Transfer speed** | Up to 100 GB/s (25x faster than SSD) | Up to 1 TB/s |
| **Cost** | ~$3/GB (30-50x more expensive than SSD) | Built into the CPU chip |
| **Use case** | Stores code and data being actively processed. Volatile -- power loss means data loss. | Ultrafast data fetch (~0.1 ns). Used for browser cache, database query result cache. |

**Supporting Processes**

- **Networking** -- storage systems are typically distributed across many servers, improving read/write performance, durability, and availability.
- **Serialization** -- any data stored in a file, database, or sent over a network must be serialized into a portable format.

---

**Serialization**

Serialization transforms in-memory data structures (optimized for CPU) into a disk format (binary bytes) for persistent storage. De-serialization reverses the process.

<img src="/data-engineering-specialization-website/images/diagrams/serialization-flow-dark.svg" alt="Serialization and compression flow from in-memory to storage" class="diagram diagram-dark" style="max-height: 900px;" />
<img src="/data-engineering-specialization-website/images/diagrams/serialization-flow.svg" alt="Serialization and compression flow from in-memory to storage" class="diagram diagram-light" style="max-height: 900px;" />

Data can be serialized in **row-based** or **column-based** order. In row-based serialization, each row is stored as a contiguous sequence of bytes. In column-based serialization, all values of a single column are stored together.

**Serialization Formats**

| Format | Type | Layout | Key characteristics |
|---|---|---|---|
| **CSV** | Text | Row-based | Human-readable, no defined schema, error-prone. Adding rows/columns requires manual handling. |
| **XML** | Text | Row-based | Extensible markup language. Legacy format, slow to serialize and de-serialize. |
| **JSON** | Text | Row-based | Plain-text object serialization. The standard for data exchange over APIs. |
| **Parquet** | Binary | Column-based | Optimized for analytical queries and big data processing. Up to 100x faster than CSV. |
| **Avro** | Binary | Row-based | Schema-defined structure with schema evolution support. Good for streaming and write-heavy workloads. |

---

**Compression**

Compression algorithms reduce redundancy to make serialized data smaller. Smaller files mean faster queries and less I/O time when loading data from disk.

| Type | Behavior | Use case |
|---|---|---|
| **Lossless** | Data can be reconstructed bit-for-bit | Required for data engineering (gzip, bzip2, Snappy, Zstandard, LZ4) |
| **Lossy** | Some data is permanently discarded | Media files (MP3, JPEG) -- not used in data pipelines |

**Columnar Encoding Techniques**

Two encoding techniques are particularly effective for columnar data with repeated values:

- **Run-length encoding** -- repeated values stored as `(value, start_index, run_length)` tuples. For example, `[5,5,5,5,4,4,2,2,2,2,2]` becomes `(5,1,4), (4,5,2), (2,7,5)`.

- **Bit-vector encoding** -- each distinct value gets a binary vector with a `1` at every index where that value appears.

## 1.1.3 Cloud Storage Options

Cloud providers offer three main storage paradigms, each optimized for different access patterns.

| | File Storage | Block Storage | Object Storage |
|---|---|---|---|
| **Structure** | Directory tree with metadata (name, owner, permissions) | Fixed-size blocks on disk, each with a unique key | Flat structure -- immutable objects in a top-level container |
| **Access pattern** | Path-based: `/home/user/file.txt` | Key-based block lookup table | Key-based: `s3://bucket/file.json` |
| **Best for** | Centralized file sharing across users/hosts | OLTP systems with frequent, small read/write ops | Data lakes, OLAP, ML pipelines, cloud warehouses |
| **Scaling** | Built on top of block storage | Blocks distributed across multiple disks | Horizontal -- each node holds its own disk, objects sharded and replicated |
| **AWS service** | `EFS` (Elastic File System) | `EBS` (Elastic Block Store) | `S3` (Simple Storage Service) |
| **Tradeoff** | Easy to manage, slower due to file hierarchy overhead | Low latency, persistent VM storage (EC2) | Not suited for small transactional workloads, immutable (update = full rewrite) |
