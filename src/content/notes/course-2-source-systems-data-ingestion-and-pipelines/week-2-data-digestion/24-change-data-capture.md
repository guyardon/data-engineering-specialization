---
title: "2.4 Change Data Capture"
course: "Course 2: Source Systems, Data Ingestion and Pipelines"
courseSlug: "course-2-source-systems-data-ingestion-and-pipelines"
courseOrder: 2
week: "Week 2: Data Digestion"
weekSlug: "week-2-data-digestion"
weekOrder: 2
order: 4
notionId: "190969a7-aa01-80b5-b7ef-df594fb8212d"
---

## 2.4.1 CDC Fundamentals

**Change Data Capture (CDC)** is a method for extracting each change event (insert, update, delete) that occurs in a database and making it available for downstream systems. It solves the fundamental problem of keeping storage systems in sync with source data.


---

**Ways to Keep Storage Systems In Sync**

- **Full Snapshot / Full Load**: Delete all old data and re-extract every row from the source table. This ensures consistency but becomes processing- and memory-heavy at high volumes. Best suited for applications without frequent update requirements.
- **Incremental (Differential) Load**: Only load updates and changes since the last read, for example by using a `last_updated_at` column. This requires more complex logic but is far more efficient. When applied to databases, this process is called **Change Data Capture (CDC)**.

<img src="/data-engineering-specialization-website/images/diagrams/cdc-sync-methods-dark.svg" alt="Full Snapshot vs CDC Sync Methods" class="diagram diagram-dark" />
<img src="/data-engineering-specialization-website/images/diagrams/cdc-sync-methods.svg" alt="Full Snapshot vs CDC Sync Methods" class="diagram diagram-light" />

---

**Use Cases for CDC**

- **Database synchronization**: Keep a data warehouse updated with changes from a production `PostgreSQL` database, or replicate on-premises databases to the cloud.
- **Audit trails**: Capture historical changes for regulatory compliance, business insights, or auditing.
- **Microservices communication**: CDC captures changes from one service (e.g., purchases) and relays them to downstream services (e.g., shipment, customer notifications).

## 2.4.2 CDC Approaches and Implementation

CDC can be implemented using either a push or pull model, each with different latency characteristics.

**Push**: Logic in the source database captures changes and pushes them to the target system in near-real-time.

**Pull**: The target system continuously polls the source database for changes and pulls updates when they occur. Batching before pull requests can introduce lag.

---


---

**CDC Implementation Patterns**

- **Batch-oriented / Query-based CDC (pull-based)**: Queries the database for changes based on a `last_modified` column, then updates the target table. Can be slow since it requires scanning rows.
- **Continuous / Log-based CDC (pull-based)**: Reads the database's transaction log (where every create, update, and delete is recorded for failure recovery). Changes are sent to a streaming platform like `Apache Kafka` using tools such as `Debezium`. Advantages include real-time capture, no computational overhead on the source, and no need for extra columns.
- **Trigger-based CDC (push-based)**: A stored function configured to fire when a specific column changes, pushing updates to the CDC system. The downside is that too many triggers can degrade write performance on the source database.

---

**CDC Tools:**

- `Debezium`
- `AWS DMS`
- `Kafka` Connect API
- `Airbyte` log-based CDC

<img src="/data-engineering-specialization-website/images/diagrams/cdc-patterns-dark.svg" alt="CDC Implementation Patterns" class="diagram diagram-dark" style="max-height: 1200px;" />
<img src="/data-engineering-specialization-website/images/diagrams/cdc-patterns.svg" alt="CDC Implementation Patterns" class="diagram diagram-light" style="max-height: 1200px;" />

## 2.4.3 General Considerations for Choosing Ingestion Tools

Selecting the right ingestion tool requires evaluating both the data characteristics and your reliability requirements.


---

**Characteristics of the Data**

- **Data Type and Structure**: Structured, unstructured, or semi-structured.
- **Data Volume**: Consider payload size, network bandwidth constraints, and whether you need to split data into smaller sections. For streaming, ensure the tool handles your maximum expected message size (e.g., `Kinesis` supports 1 MB per message; `Kafka` defaults to 1 MB but can be configured to 20 MB+). Also consider whether data volume will grow over time.
- **Latency Requirements**: How fast and how often do you need to operate on the data?
- **Data Quality**: Does the data need post-processing before downstream use?
- **Changes in Schema**: If schema changes are expected (new columns, type changes, renames), use tools that automatically detect schema changes. Maintain good communication with upstream stakeholders.

---

**Reliability and Durability**

**Reliability** means ingestion systems perform their intended function properly. **Durability** means data isn't lost or corrupted. Evaluate the tradeoffs between the cost of losing data versus building an appropriate level of redundancy.

<img src="/data-engineering-specialization-website/images/diagrams/ingestion-considerations-dark.svg" alt="Ingestion Tool Selection Considerations" class="diagram diagram-dark" />
<img src="/data-engineering-specialization-website/images/diagrams/ingestion-considerations.svg" alt="Ingestion Tool Selection Considerations" class="diagram diagram-light" />
