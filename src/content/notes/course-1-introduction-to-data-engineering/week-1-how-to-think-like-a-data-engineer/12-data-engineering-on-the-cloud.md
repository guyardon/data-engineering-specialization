---
title: "1.2 Data Engineering on the Cloud"
course: "Course 1: Introduction to Data Engineering"
courseSlug: "course-1-introduction-to-data-engineering"
courseOrder: 1
week: "Week 1: How to Think Like a Data Engineer"
weekSlug: "week-1-how-to-think-like-a-data-engineer"
weekOrder: 1
order: 2
notionId: "144969a7-aa01-80aa-8aa6-f29d8bdc1634"
---



## 1.2.1 Intro to AWS Cloud

- On-demand delivery of IT resources with pay-as-you-go pricing
- IT Resources:
- **Compute** (places to run code)
  - Virtual machines, container hosting services, serverless functions
- **Storage **(places to store data)
  - Amazon Simple Storage (S3), Amazon Elastic Block Storage (EBS), database services
- **Networking **(connect other resources to each other)
  - Amazon Virtual Private Cloud (VPC)

**Advantages of Building on Cloud**

- Cloud resources are scalable and elastic
- No need to worry about the exact storage capacity needed
- No need to manage scaling operations

**AWS Regions**

- Geographically distributed collections of data centers where AWS services are available
- Each region comprises multiple availability zones
- These data centers are interconnected for enhanced reliability and performance
- The main purpose of having more than one availability zone within a region is to allow you to host your applications and data resources in multiple AZs for high availability and fault-tolerance. If one availability zone becomes unavailable due to power outage or natural disaster, your work will not be impacted.

![](/data-engineering-specialization-website/images/e92af9ac-d59c-4e9b-9858-35b497cbca9f.png)

![](/data-engineering-specialization-website/images/af4eadb3-4888-465e-8b83-5a754e24ccbc.png)



## 1.2.2 Intro to AWS Core Services

**Compute**

- Amazon Elastic Compute Cloud (EC2)
- A service that provides virtual machines (VMs) on AWS
- Allows you to run any operating system and application
- EC2 can be used for:
- Development machines for programming
- Running web servers, containers, or machine learning workloads
**Networking**

- Amazon Virtual Private Cloud (VPC)
- A private network you create to host your resources
- VPCs are isolated from other networks
- You can choose their size
- Partition space into smaller networks called subnets
**Storage**

- Object Storage (e.g., Amazon Simple Storage Service, S3)
- Primarily used for storing unstructured data
- Block Storage (e.g., Amazon Elastic Block Storage, EBS)
- Used for database storage, virtual machine file systems, and other low-latency environments
- File Storage (e.g., Amazon Elastic File System, EFS)
- Data is organized into files and directories, similar to your computer
- Relational Database Service (RDS)
- Amazon Redshift
- A data warehouse service for storing, transforming, and serving data to end users
**Security**

- Shared Responsibility Model
- AWS is responsible for security of the cloud
- The customer is responsible for security in the cloud


## 1.2.3 Compute - Amazon Elastic Compute Cloud (EC2)

![](/data-engineering-specialization-website/images/28cf98b18.png)

One of the basic services provided on the cloud is compute service, which means that AWS provides you with the compute resources needed to run your applications. An example of a compute service is *Amazon EC2* (Elastic Compute Cloud), which represents a *virtual server* or *virtual machine* (the two terms are used interchangeably).

**What is a server? How is a virtual server different from a regular server?**

A *server *is like a computer or a set of computers that hosts and runs your applications. It consists of physical hardware (CPU, RAM, storage, networking components), an operating system installed on top of the hardware, and finally the applications that run on top of the operating system.

When you run your application on the cloud, your application doesn't interact directly with the actual hardware. Instead, it interacts with virtual hardware, which is a software representation of the actual hardware that can emulate its behavior. So on top of the virtual hardware, an operating system can be installed to run your application. The virtual hardware, operating system and application are known as the components of a virtual machine or virtual server (a software representation or emulation of an actual server).

The benefit of this virtualization or abstraction is that you can create more than one virtual machine that shares the same underlying physical resources. This helps achieve efficient and cost-effective use of resources. The sharing of these resources is done through a software component called the *hypervisor*, which enables the sharing of the underlying hardware. The hypervisor distributes the underlying physical computing resources, such as CPU and memory, to individual virtual machines as required.

**Amazon EC2**

In AWS, these virtual machines or virtual servers are called Amazon Elastic Compute Cloud or Amazon EC2. EC2 is one of the primary building blocks that you may directly use to run your applications or indirectly use by interacting with other services built on top of EC2 instances.

“Elastic” in EC2 means that you can acquire the necessary compute and memory resources that you need for your work. When you run your applications on EC2 instances, you can configure as many instances as you need, and you only pay for what you use. When you no longer need an instance, you can stop or terminate it. You can also pick the size of an EC2 instance, where size corresponds to the amount of compute, memory, and network capabilities for a given instance. It’s easy to resize based on your needs.

EC2 instances are grouped into several types, such as general purpose, compute optimized, memory optimized, storage optimized, and accelerated computing, which you can choose based on your use case.

AWS uses a specific naming convention for the instance types. For example, *t3a.micro *breaks down as follows:

- t: family name
- 3: generation
- a: optional capabilities
- micro: size
AWS offers a few different pay-as-you-go purchasing options for EC2 instances. By default, you can choose to set up and launch *on-demand* EC2 instances that give you compute capacity with no long-term commitments. If you want to save on cost, you can opt for EC2 *spot instances*, which are unused EC2 computing resources in the AWS cloud available at a discount compared to on-demand prices.



## 1.2.4 Networking - Virtual Private Cloud (VPC) & Subnets

Networking is another building block for hosting your work on the cloud.

### What is a network?

A network is simply a collection of devices connected together, where each connection can be a request sent from one device to another or a response to a request. When you create and use resources on AWS, you want these resources to communicate with each other and possibly with the outside internet. Enabling the communication between resources and with the outside world requires an understanding of some basic cloud networking concepts. This includes understanding what an IP address is and how to create a network for your resources on AWS using VPC (Virtual Private Cloud) and subnets.

### What is an IP address?

In a given network, each device is assigned an IP (Internet Protocol) address, which is a series of digits that uniquely identifies each device within the network. These addresses ensure that responses and requests are sent to the correct device.

There are many types of IP addresses. IPv4 is the most widely integrated version of the IP address system.  An IPv4 address is a 32-bit integer that can be expressed in hexadecimal notation in the form of x.x.x.x. In decimal notation, each x is an 8-bit number that can take a value between 0 and 255. For example, 192.101.0.2 is a valid IPv4 address.

Another related term you will encounter when working on the cloud is CIDR (Classless Inter-Domain Routing) notation. A CIDR notation represents a range of IP addresses that could be assigned to devices within a particular network. CIDR is used to provision the required number of IP addresses for a particular network and reduce wastage of IP addresses. The following is an example of CIDR notation:

192.101.0.0/24

This notation means that the first 24 bits are fixed and the last 8 bits can be any bits. In other words, 192.101.0.0/24 represents all IP addresses between 192.101.0.0 and 192.101.0.255.

### What is a VPC?

A VPC (Virtual Private Cloud) is an isolated private network where you can launch your AWS resources. A VPC exists inside a region, which can contain more than one VPC, and a VPC spans multiple availability zones inside the region. VPC is a way to isolate your resources (for example EC2) from the outside world. Think of it as a box or a wall that protects and organizes your resources. Resources within the same VPC can communicate with each other. By default, there’s no communication between resources from different VPCs or with the internet unless you allow it to happen by properly configuring the VPC.

When you create a VPC, you need to specify the range of IP addresses or the CIDR block for the network, which determines the size of the network. Each resource created inside the VPC will be assigned an IP address from the specified range. When you launch resources such as EC2, you need to make sure they’re launched inside a VPC.

### What is a subnet?

Inside your VPC, you may need some resources to be public and others to be private. You can achieve this by creating subnets within your VPC. Subnets provide you with more detailed control over access to your resources. Each VPC consists of subnets created inside availability zones. You can create a public subnet if you want to allow for outside traffic to access your resources, and you can create a private subnet if you don’t want to allow for outside traffic to access your resources.

You can think of a subnet as a smaller network inside your base network. Each subnet is assigned a CIDR block, which must be a subset of the VPC CIDR block. Resources in multiple subnets of the same VPC can communicate because they are part of the same VPC.

![](/data-engineering-specialization-website/images/f457c01b-baa3-4d22-b3ef-6ab7515527c6.png)

