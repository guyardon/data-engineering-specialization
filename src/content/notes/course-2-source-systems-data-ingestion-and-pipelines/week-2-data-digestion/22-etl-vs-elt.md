---
title: "2.2 ETL vs. ELT and REST APIs"
course: "Course 2: Source Systems, Data Ingestion and Pipelines"
courseSlug: "course-2-source-systems-data-ingestion-and-pipelines"
courseOrder: 2
week: "Week 2: Data Digestion"
weekSlug: "week-2-data-digestion"
weekOrder: 2
order: 2
notionId: "190969a7-aa01-80b5-b7ef-df594fb8212d"
---

## **1.1.2 ETL vs. ELT**

![](/data-engineering-specialization-website/images/b3d34b42-a540-4f17-ab01-e20c5386ee3e.png)

### **ETL (Extract-Transform-Load)**

- Extracts raw data from the source
- Transforms data in a staging area
- Loads transformed data into the target destination
### **ELT (Extract-Load-Transform)**

- Loads raw data into a cloud data warehouse (e.g., Redshift, Snowflake)
- Transforms data within the warehouse
- Allows flexible transformations later
### **Advantages of ELT**

- Faster implementation and data availability
- More flexibility in transformations
- Suitable for semi-structured/unstructured data (e.g., JSON, text, images)
### **Downsides of ELT**

- Risk of an "EL pipeline" (no transformation, leading to a data swamp)
### **Comparison of ETL vs. ELT**

| Feature | ETL | ELT |
| --- | --- | --- |
| **History** | Developed in the 80s/90s when storage was expensive | Gained popularity in the cloud era |
| **Transformation Timing** | Before loading | After loading |
| **Load Time** | Longer | Faster |
| **Flexibility** | Structured data only | Structured, semi-structured, and unstructured data |
| **Scalability** | Manual effort required for scaling | Uses cloud warehouse power for large-scale processing |
| **Data Quality** | Ensures data quality before loading | Requires transformations after loading |

---

## **1.1.3 REST API**

### **API Mandate**

- Jeff Bezos enforced API-based communication within Amazon, leading to the foundation of AWS.
### **What is an API?**

- A set of rules and specifications for programmatic communication between applications.
### **API Features**

- Metadata
- Documentation
- Authentication
- Error Handling
### **REST API (Representational State Transfer)**

- Uses HTTP as a communication protocol
- Most common API type
### **HTTP Request Types**

| Method | Purpose |
| --- | --- |
| **GET** | Retrieve a resource |
| **POST** | Create a resource |
| **PUT** | Update/replace a resource |
| **DELETE** | Remove a resource |
