---
title: "2.1 Data Ingestion Patterns"
course: "Course 2: Source Systems, Data Ingestion and Pipelines"
courseSlug: "course-2-source-systems-data-ingestion-and-pipelines"
courseOrder: 2
week: "Week 2: Data Digestion"
weekSlug: "week-2-data-digestion"
weekOrder: 2
order: 1
notionId: "190969a7-aa01-80b5-b7ef-df594fb8212d"
---

## **Introduction**

Data ingestion is the process of acquiring raw data from various sources. This week covers different ingestion patterns, batch and streaming ingestion requirements, and key AWS tools for data ingestion.

![](/data-engineering-specialization-website/images/93a1c497-3f13-4e25-8e7b-d9d87b6f5643.png)

---

## **Week Overview**

- Batch & Streaming Ingestion Patterns
- Requirements for Batch Ingestion from a REST API
- Requirements for Streaming Ingestion
---

## **1.1.1 Data Ingestion on a Continuum**

### **Unbounded vs. Bounded Data**

- **Unbounded Data:** Continuous stream of events (stream ingestion)
- **Bounded Data:** Data ingested in chunks (batch ingestion)
- Time-based ingestion
- Size-based ingestion
![](/data-engineering-specialization-website/images/5733cc62-1f85-4e29-8062-7037f4bcb069.png)

### **Ways to Ingest Data**

### **Using Connectors:**

- JDBC/IDBC API
- Supports time/size-based ingestion
### **Using Ingestion Tools:**

- **AWS Glue ETL** – Automates regular data ingestion
### **Using APIs:**

- Protocol-based ingestion
- Considerations:
- Ingestion limits per request
- API call frequency
- Complexity due to reliance on documentation, data owners, and custom API connection code
### **Ingesting Data from Files**

- **Manual File Download**
- **Secure File Transfer:**
- SFTP (Secure File Transfer Protocol)
- SCP (Secure Copy Protocol)
### **Ingesting Data from Streaming Systems**

- **Message Queues**
- **Streaming Platforms**
---

## **Popular AWS Data Ingestion Tools**

### **AWS Glue ETL**

- Ingests, transforms, and loads data from AWS sources (RDS, S3, Redshift)
- Uses Apache Spark for distributed processing
- Serverless and automated scaling
### **Amazon EMR**

- Managed cluster platform for big data processing (Hadoop, Spark)
- Supports large-scale transformations and ingestion
- Available in serverless and provisioned modes
### **AWS Glue ETL vs. Amazon EMR**

| Feature | AWS Glue ETL | Amazon EMR |
| --- | --- | --- |
| **Ease of Use** | Serverless, minimal setup | Requires configuration |
| **Scaling** | Automated scaling | Custom resource allocation |

### **AWS DMS (Data Migration Service)**

- Moves data between databases without transformation
- Supports migrations between different database engines
- Available in serverless and provisioned modes
### **Other AWS Ingestion Services**

- **AWS Snow Family:** Physical transfer appliances (Snowball, Snowcone) for large-scale migration
- **AWS Transfer Family:** Secure file transfers to/from Amazon S3 using SFTP, FTP
### **Third-Party Ingestion Tools**

- **Airbyte, Matillion, Fivetran** – Cloud-based ETL tools
---

## **Streaming Ingestion Tools**

- **Amazon Kinesis Data Streams**
- **Amazon Managed Streaming for Apache Kafka (MSK)**
Both enable real-time data ingestion, processing, and analytics.

---

## **Key Considerations: Batch vs. Streaming Ingestion**

- **Use Case:** Real-time ingestion is useful if it provides tangible business value.
- **Machine Learning:** Batch for model training; streaming for real-time predictions.
- **Dashboards & Reporting:** Decide between real-time and batch updates.
- **Latency:** Consider millisecond updates vs. micro-batching.
- **Cost:** Streaming is more complex and expensive.
- **System Readiness:** Can both source and destination systems handle real-time data?
- **Reliability & Availability:** Streaming requires high availability.
💡 **Recommendation:** Use real-time streaming only if the business case justifies the trade-offs.
