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

**DataOps** is a set of practices and cultural habits centered around building robust data systems and delivering high-quality data products. It is to data engineering what DevOps is to software engineering.

**3 Pillars of DataOps**

- **Automation**: CI/CD (build, test, integrate, deploy) and Infrastructure as Code (e.g., Terraform, AWS CloudFormation).
- **Observability and Monitoring**
- **Incident Response**

**DataOps Automation**

CI/CD brings version control to both code (via git) and data (enabling rollback to previous versions). Infrastructure as Code (IaC) extends version control to your entire infrastructure, letting you track changes in the code that defines your infra and revert to previous states if necessary.


## 3.1.2 Infrastructure as Code with Terraform

IaC replaces manual console clicking and fragile bash scripts with declarative configuration files that define your cloud resources.

- Example: AWS CloudFormation
![](/data-engineering-specialization-website/images/96636718-daae-4027-8b66-66d7734aa8c8.png)

- Terraform Example
![](/data-engineering-specialization-website/images/ac9500e8-8e79-40cd-83f4-68b6f3d04f00.png)

![](/data-engineering-specialization-website/images/d04183f9-46bd-46e3-ab70-622047e826fe.png)

**Terraform** uses **HCL (HashiCorp Configuration Language)**, a declarative language where you specify the desired end state of your infrastructure rather than the steps to get there. It is highly **idempotent** -- repeatedly executing the same HCL commands produces the same end result.

By contrast, **Bash** is procedural: you must specify every step, handle all conditions, and manage error handling yourself, making it far more complex for infrastructure management.

**Terraform Workflow**

1. Write config files to define your resources.
2. Terraform prepares the workspace -- installs necessary files and creates an execution plan for the resources it will create, update, or destroy.
3. You approve the plan.
4. Terraform applies the proposed steps.


## 3.1.3 Terraform Tutorials and Examples

**Terraform Basic Example**

This example creates an EC2 instance and launches it in the default VPC of your selected region.

**Initial Setup:**

- Use any IDE and install Terraform in your environment.
- Use AWS credentials to authenticate Terraform.
- Create a `main.tf` config file structured into 5 sections:
  - **Terraform settings**
  - **Providers** (plugin/binary file to interact with external resources such as a cloud provider)
  - **Resources**
  - **Inputs**
  - **Outputs**

![](/data-engineering-specialization-website/images/0a5fdf8e-e75a-4101-bb88-2c5d4ab87608.png)

![](/data-engineering-specialization-website/images/e4f04d8a-1487-40d9-ac54-700f40f578af.png)

![](/data-engineering-specialization-website/images/03ae7301-5d2d-443c-9939-7726471e31bb.png)

Core Terraform commands:

- `terraform init` -- creates `.terraform` subdirectory, initializes the backend and plugin provider.
- `terraform plan` -- creates an execution plan (`+` = new resource, `-` = destroyed, `~` = updated).
- `terraform apply` -- shows the plan again, asks for approval, then applies it.

**Terraform Tutorial - Defining Variables and Outputs**

Variables let you avoid hardcoding values that may change. Define them in your config and reference them using `var.[x]` syntax:

![](/data-engineering-specialization-website/images/cede24ea-cb43-4de8-805f-7e11438432d9.png)

![](/data-engineering-specialization-website/images/72b2fb77-22a7-4f83-add6-d7a2f4e29aa1.png)

Variables can also live in a separate file ending with `.tfvars`:

![](/data-engineering-specialization-website/images/5768039b-5738-4c01-8b13-8351446a5825.png)

**Outputs:**

Every resource you create has attributes (documented in the Terraform docs). You can export these to print them to the console, use them in other parts of your infrastructure, or reference them in other Terraform workspaces.

![](/data-engineering-specialization-website/images/a75df990-a0bc-41c5-bdfe-8c7df2eea0ab.png)

Access outputs with `terraform output` (all outputs) or `terraform output [varname]` (specific output).

**Organizing Terraform Files**

Split `main.tf` into `variables.tf`, `outputs.tf`, and `providers.tf`. Define resources in `main.tf` or dedicated `[resource_name].tf` files.

**Terraform Data Sources**

Data sources are `data` blocks that reference resources created outside Terraform or in another Terraform workspace.

**Example:** Creating a public subnet inside a VPC that was created in a previous example:

![](/data-engineering-specialization-website/images/35475174-4416-4fab-94b2-5c7211009120.png)
