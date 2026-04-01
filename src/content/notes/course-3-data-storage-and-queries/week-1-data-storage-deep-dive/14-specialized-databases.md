---
title: "1.4 Specialized Databases"
course: "Course 3: Data Storage and Queries"
courseSlug: "course-3-data-storage-and-queries"
courseOrder: 3
week: "Week 1: Data Storage Deep Dive"
weekSlug: "week-1-data-storage-deep-dive"
weekOrder: 1
order: 4
notionId: "1de969a7-aa01-8031-b2e1-cef9c6db8b8d"
---


## 1.4.1 Graph Databases

**Graph Databases**

Graph databases model data as **nodes** (entities) connected by **edges** (relationships). While the same data could live in a relational database, graph databases treat relationships as first-class citizens, making it natural to traverse connections through graph queries rather than complex SQL joins.

Common use cases:

- Recommending products
- Modeling social networks
- Representing network and IT operations
- Tracing data lineage
- Simulating supply chain logistics
- Fraud detection
- Knowledge graphs

Popular graph databases include **Neo4j**, **ArangoDB**, and **Amazon Neptune**. Query languages for graphs include **Cypher**, **Gremlin**, and **SPARQL**.


## 1.4.2 Vector Databases

**Vector Databases**

Vector databases are optimized for **similarity search** — efficiently querying data based on semantic closeness rather than exact matches. Use cases include recommendation systems, anomaly detection, and text generation. Today, the most common application is storing and querying **vector embeddings**.

Similarity is measured using metrics like Euclidean distance or cosine distance. The core algorithm is **K-Nearest Neighbors (KNN)**, which is typically optimized via **Approximate Nearest Neighbors (ANN)** for performance at scale.


## 1.4.3 Neo4j Graph Database and Cypher Query Language

**Neo4j Graph Database & Cypher Query Language**

Neo4j uses the **Property Graph Model** to describe the structure of a graph: what types of nodes exist, how they relate, and what properties they carry.

- **Node Label** — the type of a node
- **Relationship Type** — the type of an edge
- **Node Properties** and **Relationship Properties** — key-value attributes

To create a graph database in Neo4j, you provide instructions describing the graph model (e.g., importing from a CSV file). The **Cypher** query language lets you query the graph using a pattern-matching syntax:

```sql
MATCH pattern RETURN result
MATCH (n) return n
MATCH (n) return count(n)
MATCH (n) return distinct labels(n)
Match (n: Order) return count(n)
Match (n: Order) return Properties(n) limit 1
Match ()-[r]->() return count(r)
Match ()-[r]->() return distinct type(r)
Match ()-[r:Orders]->() return AVG(r.quantity*r.unitPrice) as average_price
Match ()-[r:Orders]->()-[part:PART_OF]->(c: Category) return c.categoryName, AVG(r.quantity*r.unitPrice) as average_price
Match (p:Product)-[:PART_OF]->[c.Category] where c.categoryName = "Meat/Poultry" return p.ProductName, p.unitPrice
```

The syntax is intuitive: `()` denotes a node, `[]` denotes a relationship, and `(source)-[r]->(target)` denotes a directed path.
