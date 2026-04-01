---
title: "1.2 Connecting to Source Systems"
course: "Course 2: Source Systems, Data Ingestion and Pipelines"
courseSlug: "course-2-source-systems-data-ingestion-and-pipelines"
courseOrder: 2
week: "Week 1: Working with Source Systems"
weekSlug: "week-1-working-with-source-systems"
weekOrder: 1
order: 2
notionId: "190969a7-aa01-8092-8369-c7d9471a0a7a"
---

Lesson Plan:

- Ways of connecting to source systems
- IAM roles and permissions
- Basics of networking
- Lab Exercise
---

## 1.2.1 Connecting to Source Systems

boto3 - connecting to Amazon DynamoDB NoSWL Database via Python

mysql CLI - connecting to Amazon RDS MySQL database

To see the endpoint/port number on AWS console:

For e.g. Amazon RDS:

- Sidebar → Databases
- Connections and Security Tab
- Endpoint and Port # will appear

Programatic Way (more repeatable and traceable):

- CLI
- Python SDK (boto3)
- API Connectors (e.g. JDBC/ODBC API)
---

## 1.2.2 Connecting to an Amazon RDS Instance

To connect to an existing (e.g. MySQL) instance we need 3 things:

- Database hostname/endpoint (address or location of the databse server)
- Database port (the network port the MySQL server is running on)
- Database username & password

We can get this information via the AWS management console or from the CLI

Ways to Connect:

- AWS Cloudshell:
- browser based shell providing CLI access to AWS resources in the selected region
- We can search for cloudshell in the search box, or click the terminal icon at the bottom left hand side of the page
- *mysql --host=[hostname]*
*--port=[port number]*

*--user=[database user name]*

*--password=[database user password]*

- This command is specific to MySQL but there are equivalent commands for other databases
- to get the endpoint and port via CLI - use describe-db-instances command:
  - *aws rds describe-db-instances --filters "Name=engine,Values=mysql" --query "*[].[DBInstanceIdentifier,Endpoint.Address,Endpoint.Port,MasterUsername]"*
- After connecting to the database, we can interact with it using SQL queries from the command line
- to exit, we can type *exit *or \q

- Connecting through Python:
- install *pymsql* package, which allows you to establish connection to MySQL database via connect method
- To get credentials, use boto3:
![](/data-engineering-specialization-website/images/e34caa4a-4d77-4334-9f3a-c7311b7097d2.png)

![](/data-engineering-specialization-website/images/b5a7c960-3266-48f3-992f-1ed6b92b72d3.png)

- To connect, use pymysql.connect()
![](/data-engineering-specialization-website/images/bcefdf29-78ac-490c-b355-1b235e7e1de7.png)

---

## 1.2.3 Basics of IAM and Permissions

IAM - identity and access management

Security on the Cloud:

- Encryption methods
- IAM
- Networking Protocols

Half of all cloud data breaches are caused by human error for e.g.:

- confidential data on public S3 bucket
- access credentials on GitHub
- allowing admin access

IAM

- framework for managing permissions
- permissions define which actions an identity can perform on a specific set of resources
- to exercise principle of least privilege: IAM is used
- AWS IAM service - allows to configure IAM on AWS

AWS IAM:

- Use policies to grant permissions
- Heirarchy:
- Root user - has unrestricted access to all resources
- IAM user - has specific permissions to certain resources using username and password or access key
- IAM group - collection of users that inherit the same permission from the group policy
- IAM role - A user, application or service that has been granted temporary permissions
  - **Example 1:** Let’s say you run a code on an EC2 instance that needs to read from S3. By default, the EC2 instance does not have permission to read from S3. You can transfer your credentials to EC2, but this is not secure. A better approach is to create a role, attach the required policy to read from S3, and allow the EC2 instance to assume this role.
  - **Example 2:** Let’s say you run a Glue ETL job and want it to write the ingested and transformed data to S3. You can create a role with permissions to write to S3, then allow Glue ETL to assume this role.
---

## 1.2.4 Basics of Networking in the Cloud

Each cloud is made of of physical data centers that are spread out around the world

Heirarchy:

- Region
- Availability Zone A
  - 1 or more data centers
- Availability Zone B
  - 1 or more data centers 

Virtual private cloud (VPC) smaller networks that span multiple availability zones within a region. Provides more fine-grained control to who can access what resources.

- Public subnet - for internet-facing resources
- Private subnet - for internal resources
- Each subnet can have its own security rules (network access control list (ACL)) and routing configurations through the internet gateways

Data and resources are replicated across availability zones to ensure that your systems keep working even if a data center goes down.

Region considerations:

- Legal compliance
- Latency (the closer your end users are to the region, the lower the latency)
- Availability (the more availability zones - the more likely you are to recover from a disaster)
- Cost

## 1.2.5 AWS Networking Overview - VPCs and Subnets

Core networking concepts:

- Amazon VPCs
- subnets
- gateways
- route tables
- network access control lists (ACLs)
- security groups

Scenario: web application running on an EC2 instance that allows you to query a database running on RDS:

![](/data-engineering-specialization-website/images/d795bf77-fe26-4786-b6df-952c2c581c96.png)

We’ll build the networking components

Default VPC - exists in each availability zones - can be used for experimenting public facing resources. It’s best not to use this for any real work.

First - configure the VPC:

- Console → VPC → Create VPC
- VPC only
- Give name, private IP address range, and region (region can be changed from the top right hand side in the drop down).

IPv4 CIDR (classless inter-domain routing)

- range of private IP addresses can be used within the VPC
- any resources that will be deployed into this VPC will be assigned a private IP address from this range.
- e.g. 10.0.0.0/16
- [0-255].[0-255].[0-255].[0-255]/x
- Each number is 8 bits
- The last number specifies the host
- x - prefix length (how many bits are used for the network part of the address. 16 means first two numbers are used for the network part, 24 means the first 3 numbers are used for the network part.

Next - configure a subnet within a VPC:

- each subnet is associated in a specific Availability Zones
- In the VPC dashboard:
- Subnets → create subnet → select which VPC to use
- Give name, specify AZ, IPv4 CIDR block (e.g. 10.0.1.0/24)
- Add new subnet, specify a different AZ, IPv4 (e.g. 10.0.2.0/24)
- same process for private or public subnets.
- finally, click create
- At this point, no subnets have access to the outside internet

Next - configure internet connectivity and NAT gateways:

Considerations:

- applications running on EC2 instance (private subnet) sometimes need to download resources from the internet - we need to configure a NAT
- we need to configure an internet gateway (”door” to the internet)
- We need a way to submit requests to the application running on the EC2 instance - we need to configure the ALB

Internet Gateway:

- supports inbound and outbound traffic
- door to the outside internet from the public subnets

Network Address Translation Gateway (NAT)

- Allows resources in a private subnet to connect to the internet or other AWS services
- Prevents the internet from initiating connections with those resources
- Only allows outgoing traffic and protects the resources inside the private subnet.

ALB (application load balancer)

- Distributes incoming application traffic across multiple backend targets
- Handles the load and ensures the application remains responsive and available
- Keeps those EC2 instances private

To configure an internet gateway:

- In AWS search box - VPC
- Internet gateways → create internet gateway → actions → attach to VPC → select desired VPC → attach internet gateway

To configure a NAT gateway:

- One NAT Gateway for each AZ to connect the public VPC
- In AWS search box - VPC
- NAT gateways → create NAT gateway → give name→ select subnet → allocate elastic IP → create NAT gateway

Configuring Route Tables:

- Essential for directing network traffic within your VPC
- Default route table is automatically created, and allows internal communication within the VPC (but not to internet connectivity)
- For public subnets:
- Configure all internet bound traffic to internet gateway
- For private subnets:
- Configure internet traffic to the NAT gateway in the public subnet
- The public subnet will be connected to the private subnet, but resources in the private subnet will not be exposed to the internet

To do this on AWS:

- VPC dashboard → route tables → create route table → give a name → select VPC → create route table
- actions dropdown → edit subnet associations → select desired subnet → save associations
- In our example, we need 4 route tables (one to each subnet)
- Now we need to configure the routes
- Route tables → select the created public route table → routes → edit routes (there will be an existing default route for communication within the VPC) → add route → destination 0.0.0.0/0 (/0 prefix matches any ip address - the entire internet) → target dropdown → select the created internet gateway that was created.
- For private subnets the destination will be the same (public interent 0.0.0.0/0), but the target will be the NAT gateway that we created.

Network Access Control Lists (ACLs) and Security Groups:

- Security Groups:
- Instance level virtual firewalls, controlling both inbound and outbound traffic
- Specific rules for inbound rules (what type of traffic, and from where)
- Stateful, allow inbound traffic to an instance, the return traffic is automatically allowed, even if there are no outbound rules explicitly stating it (this allows HTTP requests).

E.g - security group chain

- Our ALB needs a security group allowing HTTP (port 80) and HTTPS (port 443) from the internet (0.0.0.0/0)
- Our EC2 instance hosting the web server should reference the security group used by the ALB (i.e. specify the source as the ALB’s security group). then we would give it its own security group.
- Our Amazon RDS instance references the EC2 security group as its source for its own security group.
![](/data-engineering-specialization-website/images/29944dd5-e008-4d6e-ace9-c5b61719e35b.png)

To set up a security group:

- VPC dashboard → security groups → create security group → give name → select vpc it belongs to → add inbound rule → HTTP → source 0.0.0.0/0. Do the same for HTTPS. Finally click create security group

Network Access Control Lists (ACLs)

- Provide an additional layer of security at the subnet layer
- stateless
- need to define inbound and outbound rules explicitly (more granular control over traffic)
- Useful for implementing security policies at the subnet level

---

**Summary of Networking on AWS:**

- VPCs and Subnets
- Give you a way to define a private network on AWS
- Route Tables
- Direct traffic within the VPC to the internet
- Public Subnets 
- pointing to the internet gateway (allowing resources within these subnets to access the internet)
- Private Subnets
- routes pointing to the NAT gateway, enabling instances to initiate outbound connections securely
- NAT gateway
- enabling instances to initiate outbound connections securely
- Note that in practice, what makes a subnet public or private is the route table
- Security Groups
- act as virtual firewalls at the instance level
- control both inbound and outbound traffic 
- stateful (i.e. if inbound traffic is allowed, so is outbound traffic)
- Network ACLs
- Provide an additional layer of security at the subnet layer
- stateless
- need to define inbound and outbound rules explicitly (more granular control over traffic)
- Useful for implementing security policies at the subnet level
![](/data-engineering-specialization-website/images/5040b5eb-c159-40ef-bbf5-1bdd3b97d914.png)


