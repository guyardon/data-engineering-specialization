---
title: "2.3 Streaming Systems"
course: "Course 2: Source Systems, Data Ingestion and Pipelines"
courseSlug: "course-2-source-systems-data-ingestion-and-pipelines"
courseOrder: 2
week: "Week 2: Data Digestion"
weekSlug: "week-2-data-digestion"
weekOrder: 2
order: 3
notionId: "190969a7-aa01-80b5-b7ef-df594fb8212d"
---

## Streaming Systems

### Message Queues vs. Event Streaming Platforms

- Message Queue
- A buffer used to deliver messages asynchronously
- FIFO basis
- Event Streaming Platform
- Append only persistent log
- Event router distributes messages in the log to the subscribers
- It's possible to replay or re-process messages

### **Apache Kakfa**

- Open source event streaming platform
- Event producers:
- send or push messages over the network to a Kafka cluster
- Kafka cluster
- Contains one or more servers (called brokers)
- Message streams are split up into "topics"
- Retains messages to allow replaying or reprocessing messages as needed
- Topics
- A category that holds a collection of related events
- Analogy to a road to a city
- A topic is made up of partitions (logs)
- Partitions (logs):
- Ordered immutable sequences of messages
- Analogy to lanes on the highway
- It's the job of the producer to distribute the messages to partitions
- Partition Strategy:
  - Round robin strategy
  - Based on message key
- Can only be assigned to a single consumer
- Event Consumers
- read or pull messages from the Kafka cluster
- subscribe to one or more topics

### **Kinesis Data Streams**

- Analogous to Kafka cluster
- Message streams are split up into "streams" (analogous to topics in Kafka)
- Stream
- Made up of shards (analogous to partitions in Kafka)
- To determine the number of shards to configure when setting up the system - we need to determine the size and rate of read/write operations
- Read Operations
- Up to 5 operations per second
- Max total read rate: 2MB/s
- Write Operation
- Up to 1000 records per second per shard
- Max total write rate: 1MB/s
- Data Record
- Partition Key (used to determine shard)
  - e.g. use customer ID as partition key
- Sequence number
- Binary large object (BLOB)
- Shared vs. Enhanced Fan-Out
- Shared fan out is when consumers share a shard's read capacity
- Enhanced fan-out is when consumers are able to read at the full read capacity of the shard
- To consume/process data stored in Kinesis Data Streams:
- We can use AWS services such as:
  - AWS Lambda
  - Amazon Managed Service for Apache Flink
  - AWS Glue'
- We can also write our custom consumers using the Amazon Kinesis Client Library (KCL)
- We can connect consumers to other AWS services such as AWS Data Firehose to store data in S3

Kinesis in "on-demand" Mode

- automatically manage the scaling of shards up or down as needed
- Only charged for what you use
- More convenient from an operational perspective
Kinesis in "Provisioned" Mode

- Manually specify the number of shards
- Manually add more shards when needed
- A good fit if you have predictable traffic and/or want to control your costs more carefully
