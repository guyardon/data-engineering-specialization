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


**Hierarchal View of Storage:**

- **Physical Components**
- Magnetic Disks
- SSD (Solid State Drives)
- RAM
- **Processes**
- CPU
- Compression
- Networking
- Serialization
- **Storage Systems**
- Databases
- Object Stores
- Graph Databases
- Vector Databases 
- OLTP (Online Transactional Processing Systems)
  - Focus on performing read/write queries with low latency
- OLAP (Online Analytical Processing Systems)
  - Focus on applying analytical activities on data (eg. aggregation, summarization)
- **Storage Abstractions**
- Data Warehouses
- Datalakes
- Data Lakehouses


**Course Overview**

**Week 1:**

- Serialization/compression
- Characteristics of physical components
- Data storage in databases 
- row vs column databases
- graph and vector databases
- Cloud storage paradigms
- block, object, file storage
- Trade-offs between storage cost and performance

**Week 2**

- How to choose the appropriate abstractions for storing data

**Week 3**

- How queries work
- How different storage solutions affect query performance
- Techniques for improving query performance


## 1.1.2 Raw Ingredients of Storage Systems

**Raw Ingredients of Storage Systems**

- **Persistent Storage Mediums**
- Magnetic disks
  - Rotating platters stored in HHDs (hard disk drives)
  - Circular tracks and sectors = Address
  - Read/write head
    - Write: encode binary data by changing the magnetic field to point in a particular direction (to store 1) and opposite direction (to store 1)
    - Write: converts magnetic field into binary data
  - Latency
    - depends on seek time and rotational latency
- SSD
  - Data stored as electrical charge in flash memory
    - 1/0 based on charge cell
  - Read and write data much faster than magnetic disks

- Distributed processing
  - Data transfer speed limited by network performance
- Partitioning
  - Slicing SSDs into partitions

- **Volatile Memory**
- RAM
- CPU Cache
|  | **RAM** | **CPU Cache** |  |
| --- | --- | --- | --- |
| Data Transfer Speed | up to 100 GB/sec | up to 1TB/sec | RAM 25X faster than SSD |
| Cost | $3 per GB | / | RAM 30-50 times more expensive than SSD!  |
| Use case | Store the code, and data that the code processes. Not that its volatile, and a power outage can cause data loss. | Located directly on the CPU chip. Useful for ultrafast data fetch (0.1 ns), and super high data transfer speed. Useful for storing browser cache (store downloaded web resources) or database cache (storing results of re-used queries) |  |

- **Processes required for Data Storage**
- Networking
  - Storage systems are typically distributed across many servers
    - improved read/write performance
    - improved data durability and availability
- Serialization
  - Data stored in a file/database or sent over a network is serialized
![](/data-engineering-specialization-website/images/e732b606-c11f-4fd8-abcc-e5b06758e71e.png)

![](/data-engineering-specialization-website/images/a3cbd75a-12c2-40f8-ad05-061ce03c7700.png)

![](/data-engineering-specialization-website/images/5d8a54ab-dd8c-44d5-bd98-70e5c2608623.png)

- Parquet can be 100 times faster than CSV!
- **Compression**
- Uses algorithms to reduce redundancy and repetition to serialize data more efficiently
- compressed data is smaller than the original size
- improves query performance
- reduces I/O time needed to load data
- Types of compression
  - Lossless: data can be reconstructed bit-by-bit
  - Lossy: some data is lost (e.g. mp3, jpeg)
- Compression engines:
  - gzip, bzip2
    - good for text based data formats (e.g. json, xml, csv, etc)
  - New generation of compression algorithms:
    - Snappy, Zstandard, LZFSE, LZ4
- Example of compression
  - Run length encoding
    - useful for columnar compression
    - repeated values in columns are stored as tuples: (value, start index, run length)
      - e.g. column which has [5, 5, 5, 5, 4, 4, 2, 2, 2, 2, 2] will be stored as (5, 1, 4), (4, 5, 2), (2, 7, 5)
  - Bit vector encoding
    - repeated values in columns are stored as binary vector, with a 1 corresponding to the index where the value is located.
![](/data-engineering-specialization-website/images/a6508f11-eae2-4537-a198-4c0248a11e68.png)


## 1.1.3 Cloud Storage Options

**Cloud Storage Options**

**File Storage**

- organizes files into irectory tree
- each directory contains metadata such as name, owner, last modified date, permissions, pointer to the actual identities
- e.g. /home/username/filename.txt
- User Cases:
- centralized access to files that need to be easily shared with multiple users/host machines
- e.g. EFS (Amazon Elastic File System)
  - provides access to shared files over a network
  - networking, scaling, configuration are handled by the cloud vendor
- often built on top of block storage
- Cons:
- slow read/write performance due to keeping track of file heirarchy

**Block Storage**

- divides files into small fixed-size blocks of data stored on a disk (magnetic or SSD)
- each block has a unique identifier (stored in a lookup table)
- you can efficiently retrieve and modify data in individual blocks
- you can distribute blocks of data across multiple storage disks
  - Higher scalability
  - stronger data durability
- Ideal for data with frequent access and modifications
- Enables OLTP systems to perform small and frequent read/write operations with low latency
- Provides persistent storage to virtual machines (e.g. EC2 instances)
- Default storage for EC2:
- EBS (Amazon Elastic Block Store)
  - SSD for latency sensitive workloads
  - Magnetic disks to store infrequently accessed data

**Object Storage**

- Stores files as <u>immutable</u> files as data objects in a <u>flat structure</u>
- To update the file you have to re-write the entire object
- Objects are organized in a top level *logical container *(e.g. an S3 bucket)
- Each object is assigned a key
- s3://bucket_name/my_file.json
- my_file.json is the key here, where bucket_name is the bucket name
- Can scale horizontally and support performant paralell operations
- each storage node contains its own disk
- objects are distributed across these nodes
- each node holds *shards* of objects, which are <u>replicated</u> across nodes for durability
- Not good at small transactional workloads
- Good for storage layer of cloud data warehouses or data lakes
- Good for storing data needed for OLAP systems, or ML pipelines.

![](/data-engineering-specialization-website/images/26e7cc7e-9423-4f54-98e1-db84b58fc835.png)

