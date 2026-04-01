---
title: "1.1 How to Think Like a Data Engineer"
course: "Course 1: Introduction to Data Engineering"
courseSlug: "course-1-introduction-to-data-engineering"
courseOrder: 1
week: "Week 1: How to Think Like a Data Engineer"
weekSlug: "week-1-how-to-think-like-a-data-engineer"
weekOrder: 1
order: 1
notionId: "144969a7-aa01-805a-8d43-f23e81e41cd5"
---



## 1.1.1 The Data Engineering Lifecycle

**Data Engineering Definition** (from Fundamentals of Data Engineering):

*Data engineering is the development, implementation, and maintenance of systems and processes that take in raw data and produce high quality consistent information that supports downstream use cases, such as analysis and machine learning. Data engineering is the intersection of security, data management, DataOps, data architecture, orchestration, and software engineering. *

![](/data-engineering-specialization-website/images/74eac90a-63fd-4888-a527-be16a27f3703.png)

**Data Pipeline Definition**

*The combination of architecture, systems, and processes that move data through the data engineering lifecycle.*

**The Job of the Data Engineer**

At its core, the data engineer's job is to get raw data from somewhere, transform it into something useful, and make it available to downstream consumers.



## 1.1.2 The History of Data and Data Engineering

Data engineering didn't appear overnight — it evolved alongside decades of database and computing innovation.

- **1960s:** First computerized databases
- **1970s:** Relational databases emerge; IBM develops SQL
- **1980s:** Data warehouses developed to support analytics
- **1990s:** Data modeling for Business Intelligence (BI); dot-com boom drives web-first companies and backend systems (servers, databases, storage)
- **2000s:** Big Data era begins, led by large tech companies
- **Late 2000s–2010s:** Big Data tools proliferate
- **Today:** "Big Data Engineers" have evolved into "Data Engineers"

Today's data engineer builds powerful, scalable systems using existing tools — with a focus on achieving business goals rather than inventing infrastructure from scratch.


## 1.1.3 The Data Engineer Among Other Stakeholders

Data engineers sit between the teams that produce data and the teams that consume it.

**Upstream Stakeholders:**

- Software engineers and other teams generating the data

**Downstream stakeholders:**

- Analysts, data scientists, ML engineers, and business users consuming the data

Communication with **upstream** stakeholders matters for understanding the data you're ingesting and catching anything that might disrupt the pipeline. Communication with **downstream** stakeholders matters for understanding how the data you serve relates to their goals and where it adds business value.


## 1.1.4 Business Value

The most important question for a data engineer: how does your work add value to the organization? Don't get hung up on every new technology — focus on what drives business outcomes.

Value can take many forms:

- Revenue growth
- Successful product launches
- Cost reduction
- Helping stakeholders achieve their goals (analysts, ML engineers, marketing teams)


## 1.1.5 Gathering System Requirements

Once you understand the business need, translate it into system requirements. These fall into two categories:

- **Functional requirements** — what the system should be able to do
- **Non-functional requirements** — how the system accomplishes what it needs to do (performance, reliability, scalability)

Cost and security constraints should be factored in from the start.



## 1.1.6 Translating Stakeholder Needs into Specific Requirements

Turning vague stakeholder needs into concrete requirements takes structured discovery:

- Learn what existing data systems or solutions are in place
- Identify pain points or problems with current solutions
- Understand what actions stakeholders plan to take with the data
- Identify other stakeholders you need to talk to if gaps remain


## 1.1.7 Thinking Like a Data Engineer

Putting it all together, here is a repeatable framework for approaching any data engineering problem:

1. **Identify business goals and stakeholder needs**
   1. Explore existing systems and stakeholder requirements
   2. Ask stakeholders about their intended actions with the data product
2. **Define system requirements**
   1. Functional requirements (the "what")
   2. Non-functional requirements (the "how")
   3. Document conclusions
3. **Choose tools and technologies**
   1. Identify tools and technologies to meet non-functional requirements
   2. Perform cost/benefit analysis to choose between comparable options
   3. Prototype your system to align with stakeholder needs
4. **Build, evaluate, iterate, and evolve** the data system
