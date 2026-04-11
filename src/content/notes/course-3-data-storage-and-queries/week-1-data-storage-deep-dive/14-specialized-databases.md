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

Graph databases model data as **nodes** (entities) connected by **edges** (relationships). While the same data could live in a relational database, graph databases treat relationships as first-class citizens, making it natural to traverse connections through graph queries rather than complex SQL joins.

| Use case               | Example                                     |
| ---------------------- | ------------------------------------------- |
| Recommendation systems | "Customers who bought X also bought Y"      |
| Social networks        | Friendship graphs, follower relationships   |
| Data lineage           | Tracing how data flows through pipelines    |
| Fraud detection        | Identifying suspicious transaction patterns |
| Knowledge graphs       | Connecting entities and their relationships |
| Network/IT operations  | Mapping infrastructure dependencies         |
| Supply chain logistics | Simulating logistics flows                  |

Popular graph databases include `Neo4j`, `ArangoDB`, and `Amazon Neptune`. Query languages include **Cypher**, **Gremlin**, and **SPARQL**.

<img src="/data-engineering-specialization/images/diagrams/graph-database-dark.svg" alt="Graph database schematic showing nodes, edges, and properties" class="diagram diagram-dark" />
<img src="/data-engineering-specialization/images/diagrams/graph-database.svg" alt="Graph database schematic showing nodes, edges, and properties" class="diagram diagram-light" />

## 1.4.2 Vector Databases

Vector databases are optimized for **similarity search** -- efficiently querying data based on semantic closeness rather than exact matches.

| Aspect                 | Details                                                                                        |
| ---------------------- | ---------------------------------------------------------------------------------------------- |
| **Core concept**       | Store and query **vector embeddings** -- numerical representations of data                     |
| **Similarity metrics** | Euclidean distance, cosine distance                                                            |
| **Core algorithm**     | **K-Nearest Neighbors (KNN)**, optimized via **Approximate Nearest Neighbors (ANN)** for scale |
| **Use cases**          | Recommendation systems, anomaly detection, text generation, semantic search                    |

<img src="/data-engineering-specialization/images/diagrams/vector-database-dark.svg" alt="Vector database schematic showing embedding, vector space, and KNN search" class="diagram diagram-dark" style="max-height: 900px;" />
<img src="/data-engineering-specialization/images/diagrams/vector-database.svg" alt="Vector database schematic showing embedding, vector space, and KNN search" class="diagram diagram-light" style="max-height: 900px;" />

## 1.4.3 Neo4j and the Cypher Query Language

<div class="tech-logos">
  <div class="tech-logo">
    <img src="/data-engineering-specialization/images/logos/neo4j.svg" alt="Neo4j" class="logo-light" /><img src="/data-engineering-specialization/images/logos/neo4j-dark.svg" alt="Neo4j" class="logo-dark" />
    <span>Neo4j</span>
  </div>
</div>

`Neo4j` uses the **Property Graph Model** to describe graph structure:

| Concept                     | Description                                                        |
| --------------------------- | ------------------------------------------------------------------ |
| **Node label**              | The type/category of a node (e.g., `Product`, `Order`, `Category`) |
| **Relationship type**       | The type of an edge (e.g., `ORDERS`, `PART_OF`)                    |
| **Node properties**         | Key-value attributes on nodes (e.g., `name`, `unitPrice`)          |
| **Relationship properties** | Key-value attributes on edges (e.g., `quantity`, `unitPrice`)      |

---

**Cypher Query Language**

`Cypher` uses an intuitive pattern-matching syntax: `()` denotes a node, `[]` denotes a relationship, and `-->` denotes a directed edge.

```cypher
-- return all nodes in the graph
MATCH (n) RETURN n

-- count all nodes
MATCH (n) RETURN count(n)

-- list all distinct node labels (types)
MATCH (n) RETURN DISTINCT labels(n)

-- count all Order nodes
MATCH (n:Order) RETURN count(n)

-- inspect properties of a single Order
MATCH (n:Order) RETURN properties(n) LIMIT 1

-- count all relationships
MATCH ()-[r]->() RETURN count(r)

-- list all distinct relationship types
MATCH ()-[r]->() RETURN DISTINCT type(r)
```

**Traversing relationships** -- Cypher's real power is in pattern matching across connected nodes:

```cypher
-- average order value across all orders
MATCH ()-[r:Orders]->()
RETURN AVG(r.quantity * r.unitPrice) AS average_price

-- average order value per product category
MATCH ()-[r:Orders]->()-[:PART_OF]->(c:Category)
RETURN c.categoryName, AVG(r.quantity * r.unitPrice) AS average_price

-- find all meat/poultry products with their prices
MATCH (p:Product)-[:PART_OF]->(c:Category)
WHERE c.categoryName = "Meat/Poultry"
RETURN p.productName, p.unitPrice
```
