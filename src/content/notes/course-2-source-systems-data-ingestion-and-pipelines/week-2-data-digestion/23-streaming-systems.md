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

## 2.3.1 Streaming Concepts

Streaming systems come in two flavors, and the distinction matters for how you design your consumers.

---

**Message Queues vs. Event Streaming Platforms**

A **Message Queue** is a buffer that delivers messages asynchronously on a FIFO basis. Once a message is consumed, it's gone.

An **Event Streaming Platform** is an append-only persistent log where an event router distributes messages to subscribers. The key differentiator is that messages can be **replayed or re-processed** since they persist in the log.

<img src="/data-engineering-specialization/images/diagrams/streaming-concepts-dark.svg" alt="Message Queue vs Event Streaming Platform" class="diagram diagram-dark" />
<img src="/data-engineering-specialization/images/diagrams/streaming-concepts.svg" alt="Message Queue vs Event Streaming Platform" class="diagram diagram-light" />

## 2.3.2 Apache Kafka

<img class="tech-logo-aside logo-light" src="/data-engineering-specialization/images/logos/kafka.svg" alt="Apache Kafka" /><img class="tech-logo-aside logo-dark" src="/data-engineering-specialization/images/logos/kafka-dark.svg" alt="Apache Kafka" />

**Apache Kafka**

`Apache Kafka` is the most widely adopted open-source event streaming platform. Its architecture consists of three main layers.

---

**Event Producers** send or push messages over the network to a `Kafka` cluster, which contains one or more servers called **brokers**. The cluster retains messages to allow replaying or reprocessing as needed.

Message streams are organized into **topics** -- categories that hold collections of related events. Each topic is made up of **partitions (logs)**, which are ordered, immutable sequences of messages. Producers distribute messages to partitions using either a **round-robin strategy** or based on a **message key**. Each partition can only be assigned to a single consumer.

**Event Consumers** read or pull messages from the `Kafka` cluster and subscribe to one or more topics.

<img src="/data-engineering-specialization/images/diagrams/kafka-architecture-dark.svg" alt="Apache Kafka Architecture" class="diagram diagram-dark" />
<img src="/data-engineering-specialization/images/diagrams/kafka-architecture.svg" alt="Apache Kafka Architecture" class="diagram diagram-light" />

## 2.3.3 Kinesis Data Streams

`Kinesis Data Streams` is AWS's managed alternative to a `Kafka` cluster, with analogous concepts under different names.

Message streams are split into **streams** (analogous to `Kafka` topics), which are made up of **shards** (analogous to partitions). When setting up, you need to determine the number of shards based on read/write throughput:

- **Read Operations**: Up to 5 per second, max total read rate of 2 MB/s per shard.
- **Write Operations**: Up to 1,000 records per second per shard, max total write rate of 1 MB/s.

Each **Data Record** contains a **Partition Key** (determines the shard), a **Sequence Number**, and a **Binary Large Object (BLOB)**.

<img src="/data-engineering-specialization/images/diagrams/kinesis-data-streams-aws-dark.png" alt="Kinesis Data Streams Architecture" class="diagram diagram-dark" />
<img src="/data-engineering-specialization/images/diagrams/kinesis-data-streams-aws.png" alt="Kinesis Data Streams Architecture" class="diagram diagram-light" />

---

**Shared vs. Enhanced Fan-Out:** With shared fan-out, consumers share a shard's read capacity. Enhanced fan-out gives each consumer the full read capacity of the shard.

---

**Consuming data from `Kinesis Data Streams`** can be done with AWS services like `AWS Lambda`, `Amazon Managed Service for Apache Flink`, or `AWS Glue`. You can also write custom consumers using the `Amazon Kinesis Client Library (KCL)` or connect to `AWS Data Firehose` to store data in `S3`.

---

**On-Demand Mode** automatically scales shards up or down and charges only for what you use -- more convenient operationally. **Provisioned Mode** requires manually specifying and adjusting shard counts, making it a better fit for predictable traffic patterns or tighter cost control.
