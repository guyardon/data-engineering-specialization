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

Types of software solutions:

- Open source
- Managed open source
- Proprietary

Keep in mind the end goal!

Considerations:

- Location
- On-prem
- Cloud
- Hybird
- Other considerations
- Cost optimization
- Team’s size and capabilities


## 3.2.2 Location

On premises

- Company owns and maintains the hardware and software solutions for their data stack
- Provisioning
- Maintaining
- Updating
- Scaling

Cloud

- The cloud owns and maintains the hardware in data centers
- You rent the compute and storage resources
- You don’t need to maintain or provision any hardware

Hybrid

- Some companies choose to (or are required to) keep some of the data systems on-prem
- Regulations, security, client privacy concerns

In these courses - the focus is building a data system on the cloud.


## 3.2.3 Monolith vs. Modular Systems

**Monolithic System**

- Self contained
- Single codebase
- May have tightly coupled components
- Hard to maintain
- At a certain point, the entire architecture may be rewritten

**Modular System**

- Built with loosely coupled systems
- Application is broken down into self-contained areas of concern
- Micro-services enable modular systems
- Each service is deployed as a single unit
- Interoperability
- Flexible and reversible decisions
- Continuous improvement

## 3.2.4 Cost Optimization and Business Value

- Total cost of ownership (TCO)
- Total estimated cost of a solution or project or initiative over its entire lifecycle, including direct and indirect costs
  - Direct Costs:
    - Salaries
    - Cloud Bills
    - Software subscriptions
  - Indirect costs (overhead):
    - Network downtime
    - IT Support
    - Loss of productivity
**Costs of Hardware/Software:**

  - Capital Expenses (CapEx)
    - Upfront payments for long term fixed assets
      - (Before the cloud era)
    - Slowly depreciates over time
  - Operational Expenses (OpEx)
    - Expense associated with running the day-to-day operations (”pay-as-you-go”)
    - Wasn’t really an option before the cloud
- Total opportunity cost of ownership (TOCO)
- The cost of lost opportunities that you incur in choosing a particular tool or technology
- There will always be a cost of changing components to newer technologies - therefore it is important to build flexible systems.
- It’s important to recognize the components that are likely to change:
  - Immutable technologies (likely aren’t going away anytime soon):
    - Object storage
    - Networking
    - SQL
  - Transitory technologies (data stack that are rapidly evolving):
    - Stream processing
    - Orchestration
    - AI

FinOps

- Minimize TCO and TOCO
- Maximize revenues

## 3.2.5 Build vs. Buy

- Customized solutions by building it yourself

Benefits:

- Get exactly the solution you need
- Avoid licensing fees
- Avoid being at the mercy of a vendor

For most cases - this is not recommended, unless there is no existing solution out there. No need to reinvent the wheel.

Using existing solutions

- open source
- commercial open-source
- proprietary non-open source

Considerations:

- Does you team have the bandwidth and capabilities to implement an open source solution?
- Are you a small team? Could using a managed or proprietary service free up your time?
- How much are you saving?
- What is the total cost to build or maintain a system
- Do you get some advantage by building your own custom solutions
- Are you avoiding undifferentiated heavy lifting?



## 3.2.6 Server, Container, and Serverless Compute Options

Computing Options:

Server

- You set up and manage the server (e.g. Amazon EC2 system)
- Update the OS
- Install/update packages
- Patch software
- Networking, scaling and security

Container:

- Modular unit that packages code and dependencies to run on a server
- Lightweight and portable
- You set up the application code and dependencies

Serverless

- Serverless means you don’t need to set up or maintain the servers, they remain behind the scenes.
- Automatic scalling
- Availability and fault tolerance
- Pay-as-you-go
- Benefits:
- Execute small chucks of code on as-needed basis
- Run services on as-needed basis
- Pay-as-you-go.
- When to use?
- When its more cost-effective
- Good for small and discrete tasks, but not for heavy compute applications or those that require memory power.

