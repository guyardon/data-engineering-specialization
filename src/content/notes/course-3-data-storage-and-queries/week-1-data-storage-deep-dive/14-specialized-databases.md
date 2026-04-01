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

- Nodes represent data items
- Edges represent connections between the data items
- Models complex connections between data entities
- We can also store the same data in relational databases, but in graph databases, "relationships are first class citizens".
- We an traverse the graph structure to query relationships
- Its more complicated to query a relational database to query relationships
- Use cases:
- recommending products
- modeling social networks
- representing network and IT operations
- tracing data lineage
- simulating supply chain logistics
- fraud detection
- knowledge graph
- Examples:
- neo4j
- ArangoDB
- Amazon Neptune
- Example of Graph Query Languages:
- Cypher
- Gremlin
- SparQL


## 1.4.2 Vector Databases

**Vector Databases**

- Enable efficiently query data based on semantic similarities
- Called "Similarity Search"
- Use cases:
- recommendation systems
- anomaly detection
- text generation
- Today, the most common use case is vector embeddings
- Similarity search by various metrics such as Euclidean Distnace, cosine distance, etc.
- Popular algorithm
- K Nearest Neighbours
- Optimized via A-NN (approximate)
- Vector databases support ANN


## 1.4.3 Neo4j Graph Database and Cypher Query Language

**Neo4j Graph Database & Cypher Query Language**

- Relationship between data is modeled using the Property Graph Model
- Describes what type of nodes are in the graph and how these nodes can be related (edge types)
- Node Label: type of node
- Relationship type: edge type
- Node Properties
- Relationship properties
- Creating a graph database in Neo4j:
- Instructions describing the graph model (e.g. from a csv file)
- Cypher query language allows to query from the graph
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

- Denote node with ()
- Denote relationship with []
- Denote path with (source node)-[r]→(target node)
