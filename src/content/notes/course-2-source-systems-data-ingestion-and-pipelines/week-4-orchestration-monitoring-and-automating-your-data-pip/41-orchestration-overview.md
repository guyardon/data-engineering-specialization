---
title: "4.1 Orchestration Overview"
course: "Course 2: Source Systems, Data Ingestion and Pipelines"
courseSlug: "course-2-source-systems-data-ingestion-and-pipelines"
courseOrder: 2
week: "Week 4: Orchestration, Monitoring and Automating Your Data Pipelines"
weekSlug: "week-4-orchestration-monitoring-and-automating-your-data-pip"
weekOrder: 4
order: 1
notionId: "1d6969a7-aa01-80b2-9800-eaa4f638389a"
---

## Orchestration Overview

- Evolution of orchestration tools
- Basic details of orchestration
- Details of Apache AirFlow

### Before Orchestration

- Back in the day, people used cron
- CLI utility introduced in the 70s
- Used to execute a particular command at a specified date and time
![](/data-engineering-specialization-website/images/79b47862-62ef-4146-8c7e-63559a9fab02.png)

- Scheduling data pipelines with Cron - "Pure Scheduling Approach"

![](/data-engineering-specialization-website/images/44c8d528-192b-4c66-aa68-629ed7d0645f.png)

- Problem with this setup:
- If one task fails, the entire pipeline fails
- No built in monitoring or alerts
- Hard to know what went wrong
- When is this useful
- Scheduling simple repetitive tasks with no downstream use cases
- Prototyping phase

### Evolution of Orchestration Tools

- late 2000's: Dataswarm (facebook)
- 2010's: Apache oozie (limited to hadoop clusters)
- 2014: Airflow (airbnb)
- 2019: Apache Airflow
- Today: Prefect, dagster, mage
- Prefect: more scalable orchestration solutions
- dagster/mage: built in capabilites for data quality testing

### Airflow Advantages

- Written in Python
- Open source project and very active
- Available as a managed service on AWS and GCP

### Airflow Challenges

- Scalability challenge
- Ensuring data integrity
- No support for streaming pipelines

### Orchestration Basics

- Pros:
- Set up dependencies
- Monitor tasks
- Get alerts
- Create fallback plans
- Cons
- More operational overhead than simple Cron scheduling

### AirFlow Basics

- Directed Acyclic Graph (DAG)
- Graph representation where:
  - Nodes are jobs
  - Edges are the flow of data
- Data flows in one direction (directed)
- No circles or cycles (acyclic)
- Build dependencies between tasks
- Dag is defined in Python
- Airflow UI
- Visualize DAG defined in code
- Trigger DAG to run
- Monitor the progress of tasks
- Troubleshoot any issues
- Conditions:
- time-based
- event-based
  - e.g. presence of a file in an S3 bucket
- Monitoring, logging and alerts 
- Set up data quality checks
- Verify schema
- Check for null values
- data in a specified range
![](/data-engineering-specialization-website/images/e45da6e7-ee3a-4543-8750-f28b1e09e3f1.png)

![](/data-engineering-specialization-website/images/6084c439-bb7d-42ea-8636-c01c1c486f9d.png)

![](/data-engineering-specialization-website/images/fd33ecda-3321-4f35-812f-e81ab12dd8ef.png)

![](/data-engineering-specialization-website/images/45902bc4-5075-4911-adf7-f45968cddda6.png)

### Airflow - Core Components

- Underlying architecture
- Store python scripts defining DAGs in DAG directory
- Use user interface to visualize and trigger DAG manually
- Use Scheduler to monitor your DAGs
  - Pushes tasks to queue
  - Checks which tasks are ready to be triggered 
- Task Status:
  - scheduled
  - queued
  - running
  - success
  - failed
- State of DAG and status of tasks stored in metadata database, which the web server uses to display to the user
![](/data-engineering-specialization-website/images/d4a74df7-60e4-48c4-8138-c02c5d3925ca.png)

![](/data-engineering-specialization-website/images/37656b48-f29c-4e36-b600-d98299353c81.png)
