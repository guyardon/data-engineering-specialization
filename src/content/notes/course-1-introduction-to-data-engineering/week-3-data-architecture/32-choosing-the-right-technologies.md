---
title: "3.2 Choosing the Right Technologies"
course: "Course 1: Introduction to Data Engineering"
courseSlug: "course-1-introduction-to-data-engineering"
courseOrder: 1
week: "Week 3: Data Architecture"
weekSlug: "week-3-data-architecture"
weekOrder: 4
order: 2
notionId: "18c969a7-aa01-80ab-b4fd-ee68b1385af5"
---



## 3.2.1 Choosing Tools and Technologies

Technology choices shape the entire data stack. Software solutions generally fall into three categories: **open source**, **managed open source**, and **proprietary**. The end goal should always drive the decision.

Key considerations include:

- **Location** — on-premises, cloud, or hybrid
- **Cost optimization** — total spend across the solution's lifecycle
- **Team size and capabilities** — what your team can realistically build and maintain


## 3.2.2 Location

Where your infrastructure lives has major implications for cost, control, and agility.

**On-premises** — the company owns and maintains all hardware and software, handling provisioning, maintenance, updates, and scaling in-house.

---

**Cloud** — a cloud provider owns and maintains hardware in data centers. You rent compute and storage resources without provisioning or maintaining any physical infrastructure.

---

**Hybrid** — some companies keep certain data systems on-prem due to regulations, security, or client privacy concerns while running others in the cloud.

This course focuses on building data systems in the cloud.


## 3.2.3 Monolith vs. Modular Systems

<img src="/data-engineering-specialization-website/images/diagrams/monolith-modular-dark.svg" alt="Monolith vs. Modular Systems" class="diagram diagram-dark" />
<img src="/data-engineering-specialization-website/images/diagrams/monolith-modular.svg" alt="Monolith vs. Modular Systems" class="diagram diagram-light" />

**Monolithic System**

A monolithic system is self-contained with a single codebase and tightly coupled components. It becomes increasingly hard to maintain over time, and at a certain point the entire architecture may need to be rewritten.

---

**Modular System**

A modular system is built from loosely coupled, self-contained services. Each micro-service is deployed independently, enabling interoperability, flexible and reversible decisions, and continuous improvement.

## 3.2.4 Cost Optimization and Business Value

<img src="/data-engineering-specialization-website/images/diagrams/cost-optimization-dark.svg" alt="Cost Optimization and Business Value" class="diagram diagram-dark" />
<img src="/data-engineering-specialization-website/images/diagrams/cost-optimization.svg" alt="Cost Optimization and Business Value" class="diagram diagram-light" />

Understanding costs is essential to making sound technology decisions.

**Total Cost of Ownership (TCO)** is the total estimated cost of a solution over its entire lifecycle, including:

- **Direct costs:** salaries, cloud bills, software subscriptions
- **Indirect costs (overhead):** network downtime, IT support, lost productivity

---

**Costs of Hardware/Software:**

- **Capital Expenses (CapEx)** — upfront payments for long-term fixed assets (common before the cloud era), which depreciate slowly over time
- **Operational Expenses (OpEx)** — day-to-day "pay-as-you-go" costs, made practical by cloud computing

---

**Total Opportunity Cost of Ownership (TOCO)** captures the cost of lost opportunities from choosing a particular tool. Switching technologies always has a cost, which is why building flexible systems matters. When evaluating components, distinguish between:

- **Immutable technologies** (unlikely to change soon): object storage, networking, `SQL`
- **Transitory technologies** (rapidly evolving): stream processing, orchestration, AI

**FinOps** ties it all together — minimize TCO and TOCO while maximizing revenue.

## 3.2.5 Build vs. Buy

Building a custom solution gives you exactly what you need, avoids licensing fees, and eliminates vendor dependency. However, for most cases this is not recommended unless no existing solution fits. There is no need to reinvent the wheel.

Existing solutions come in three flavors: **open source**, **commercial open-source**, and **proprietary**.

Key questions to ask:

- Does your team have the bandwidth and capabilities to implement and maintain an open-source solution?
- Could a managed or proprietary service free up a small team's time?
- What is the total cost to build versus buy and maintain?
- Does building in-house provide a genuine competitive advantage?
- Are you avoiding undifferentiated heavy lifting?



## 3.2.6 Server, Container, and Serverless Compute Options

<img src="/data-engineering-specialization-website/images/diagrams/compute-models-dark.svg" alt="Server, Container, and Serverless Compute Models" class="diagram diagram-dark" />
<img src="/data-engineering-specialization-website/images/diagrams/compute-models.svg" alt="Server, Container, and Serverless Compute Models" class="diagram diagram-light" />

Three compute models offer different trade-offs between control and convenience.

**Server** — you set up and manage the server (e.g., `Amazon EC2`), handling OS updates, package installation, patching, networking, scaling, and security yourself.

---

**Container** — a modular unit that packages application code and dependencies to run on a server. Containers are lightweight and portable; you manage the application layer while the infrastructure is handled separately.

---

**Serverless** — the cloud provider manages servers entirely behind the scenes, providing automatic scaling, availability, fault tolerance, and pay-as-you-go pricing. Serverless is ideal for small, discrete tasks executed on demand. It is generally not suited for heavy compute workloads or memory-intensive applications. Use it when it is more cost-effective than the alternatives.
