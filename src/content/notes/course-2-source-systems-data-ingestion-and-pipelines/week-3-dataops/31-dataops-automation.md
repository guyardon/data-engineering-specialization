---
title: "3.1 DataOps Automation"
course: "Course 2: Source Systems, Data Ingestion and Pipelines"
courseSlug: "course-2-source-systems-data-ingestion-and-pipelines"
courseOrder: 2
week: "Week 3: DataOps"
weekSlug: "week-3-dataops"
weekOrder: 3
order: 1
notionId: "1d3969a7-aa01-80e3-b264-c6789380bcaa"
---


## 3.1.1 DataOps Overview

**Introduction**

DataOps is a set of practices and cultural habits centered around building robust data systems and delivering high quality data products (DataOps: Data Engineering is analogous to DevOps: SW Engineering)

**3 Pillars of DataOps**

- Automation
- CI/CD (build → test → integrate → deploy)
- Infrastructure as Code
  - Code that acts to deploy the resources required to run your data pipeline (e.g Terraform, AWS CloudFormation)
- Observability and Monitoring
- Incident Response 


**DataOps Automation**

- CI/CD:
- Version control
  - changes in code using git
  - changes in data (reverting to previous versions if necessary)
- IaC
- version control over your entire infrastructure
- track changes in the code defining the infra, and revert to previous infrastructure if necessary


## 3.1.2 Infrastructure as Code with Terraform

**Infrastructure as Code (Terraform)**

- Easier than instead of manual clicking setup windows in cloud or writing bash scripts
- Example: AWS CloudFormation 
![](/data-engineering-specialization-website/images/96636718-daae-4027-8b66-66d7734aa8c8.png)

- Terraform Example
![](/data-engineering-specialization-website/images/ac9500e8-8e79-40cd-83f4-68b6f3d04f00.png)

![](/data-engineering-specialization-website/images/d04183f9-46bd-46e3-ab70-622047e826fe.png)

- **Terraform**
- Uses declaritive language 
- HCL (HashiCorp Configuration Language)
- Specifies the "end state" of the infrastructure
- No need to specify the steps that need to be taken (all happens under the hood)
- Highly idempotent (i.e. if we repeatedly execute the same HCL commands, we'll end up with the same end result)
- Bash:
- Procedural language (rather than declarative) 
- When using bash, we need to specify all the steps, and treat all conditions, error handling, etc. 
- Much more complex than using declarative configuration management.


**Terraform Workflow**

1. You write the config files to define your resources
2. Terraform prepares the workspace
1. Installs necessary files
2. Creates execution plan fo the resources it will create/update/destroy
3. You approve the plan
4. Terraform applies the proposed steps


## 3.1.3 Terraform Tutorials and Examples

**Terraform Basic Example**

Create EC2 Instance and launch it in the default VPC of your selected region.

- **Initial Setup**:
- Use any IDE
- Install Terraform in your environment
- Use AWS credentials to authenticate Terraform
- Create [main.tf](http://main.tf/) config file
- Structure into 5 sections
  - **Terraform settings**
  - **Providers **
    - (plugin/binary file to interact with external resource such as a cloud provider)
  - **Resources**
  - **Inputs**
  - **Outputs**
![](/data-engineering-specialization-website/images/0a5fdf8e-e75a-4101-bb88-2c5d4ab87608.png)

![](/data-engineering-specialization-website/images/e4f04d8a-1487-40d9-ac54-700f40f578af.png)

![](/data-engineering-specialization-website/images/03ae7301-5d2d-443c-9939-7726471e31bb.png)

- terraform init 
- (creates .terraform subdirectory)
- Initializes the backend and the plugin provider
- terraform plan
- creates an execution plan and prints to console
  - + means new resource
  - - means destroyed resource
  - ~ means updated resource
- terraform apply
- shows plan again and asks for approval
- We can see the created EC2 instance in the console


**Terraform Tutorial - Defining Variables and Outputs**

- We can specify variables that are dynamic instead of hardcoding them into the configuration
- Good for variables that can change
- Defining the variables:
![](/data-engineering-specialization-website/images/cede24ea-cb43-4de8-805f-7e11438432d9.png)

- Referencing the variables in the config (use var.[x] syntax):
![](/data-engineering-specialization-website/images/72b2fb77-22a7-4f83-add6-d7a2f4e29aa1.png)

- We can also move the variables to a different file (ending with .tfvars)
![](/data-engineering-specialization-website/images/5768039b-5738-4c01-8b13-8351446a5825.png)

**Outputs:**

- Any resource we create has attributes (we can see them in the documentation)
- We may want to export these attributes to:
- print them to console
- use them in other parts of infrastructure
- reference them in other terraform workspaces
- E.g. when creating an EC2 instance, we may want to export the public_dns 
![](/data-engineering-specialization-website/images/a75df990-a0bc-41c5-bdfe-8c7df2eea0ab.png)

- To access the outputs:
- terraform output to query all outputs
- terraform output [varname] to query a specific output
**Organizing Terraform Files**

- We can divide [main.tf](http://main.tf/) to [variables.tf](http://variables.tf/), outputs.tf, providers.tf
- Define resources in [main.tf](http://main.tf/) or a [resource_name].tf for a specific resource


**Terraform Data Sources**

- Data Sources are data blocks to reference resources created outside Terraform or in another Terraform workspace

**Example:**

Creating a public subnet inside the already created VPC we created in the previous example

![](/data-engineering-specialization-website/images/35475174-4416-4fab-94b2-5c7211009120.png)
