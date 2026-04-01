---
title: "4.2 Airflow UI and DAG Creation"
course: "Course 2: Source Systems, Data Ingestion and Pipelines"
courseSlug: "course-2-source-systems-data-ingestion-and-pipelines"
courseOrder: 2
week: "Week 4: Orchestration, Monitoring and Automating Your Data Pipelines"
weekSlug: "week-4-orchestration-monitoring-and-automating-your-data-pip"
weekOrder: 4
order: 2
notionId: "1d6969a7-aa01-80b2-9800-eaa4f638389a"
---

## Airflow - UI

- DAGS page
- list of all DAGS created in DAG directory
  - owner, schedule, last run, status, status of each task within a run
  - you can trigger a DAG, or delete it
  - clicking on a DAG
    - grid view
      - previous runs
      - details, graph, gantt, code, logs

## Airflow - Creating a DAG

- e.g. ETL Process
- extract job
- transform job
- load job
- airflow.DAG() context manager
- Operators:
- PythonOperator (airflow.operators.python)
  - execute a python script
- BashOperator
  - execute bash comands
- EmptyOperator
  - organize the tasks
- EmailOperator
  - send notifications via an email
- SensorOperator
  - Used to make jobs event driven
![](/data-engineering-specialization-website/images/3fe0e599-b0df-400c-880b-7fe5b3c28f0a.png)

Defining Tasks in AirFlow:

![](/data-engineering-specialization-website/images/d120f613-43ae-42d2-86ce-541ea129b514.png)

## Airflow - Xcoms

- Xcom is short for cross-communication
- Designed to pass small amounts of data between tasks (metadata, dates, single value metrics and single computations)
- xcom_push method pushes the variable value, key timestamp, dag id, task id to the metadata database
- xcom_pull to retrieve the variable in another task
- the methods are stored in the task instance, which is in the context dictionary provided to the task context['ti']
![](/data-engineering-specialization-website/images/06bae499-7323-497d-a810-1a0a2aff7781.png)

![](/data-engineering-specialization-website/images/9ca13642-39ab-48fe-b6eb-64c33c7d95a7.png)

- We can see Xcoms in the Airflow UI under Admin→Xcoms
- Xcoms are NOT designed to pass large objects such as dataframes, we need to save them to intermediate files (in S3 for example) and read them in another task.

## Airflow - Variables

- Useful instead of hard-coding values inside tasks
- We can either create variables int eh Airflow UI or create environment variables
- Via Airflow UI: Admin→Variables
![](/data-engineering-specialization-website/images/40c05b41-7290-413a-96d8-2a3aec7c22a9.png)

- To read them in the task itself:
![](/data-engineering-specialization-website/images/5c493deb-0221-4a73-8488-20246cba508b.png)

- Note that to return as dictionary instead of string, pass deserialize_json=True

When writing DAGs, there are some best practices that help ensure your code is efficient, readable, idempotent and reproducible (like with any code). Let's go through some of these basic practices.

| **Best practices** | **Explanation/Example of a bad code** |
| --- | --- |
| Keep tasks simple and atomic | When you prepare your pipeline for orchestration, you need to identify the tasks or steps of your pipeline. Keep your tasks simple such that each task represents one operation. You don't want to end up with one task that does everything, otherwise you'll lose visibility into your data pipeline and reduce the readability of your code, which does not support idempotency.  
For example, in an ETL or ELT process, you would need to create at least three tasks: extract, transform, load, instead of creating just one task that handles the entire process. |
| Avoid top-level code | In the following code,
**call_some_function()**
**perform_computation()**
**with DAG(dag_id="example_xcom", start_date=datetime(2024, 3, 13), schedule='@daily',catchup=False):**
**        task_1 = PythonOperator(task_id='extract',python_callable=extract_api)**
**        task_2 = PythonOperator(task_id='load_data',python_callable=load)**
**        task_1 &gt;&gt; task_2**
call_some_function() and perform_computation() are both high-level codes. In general any code that isn't part of your DAG or operator instantiations is considered to be top-level code. This type of code will be executed at the time when the DAG is parsed by the scheduler. On the other hand, any code that is part of an operator is executed when the task runs, not when the DAG is parsed. Top-level code can cause performance issues because the scheduler checks the DAG directory and parses the DAG files every 30 seconds. So it may not be efficient to execute the high-level code this frequently especially if the code makes some requests to an API or a database. |
| Use variables (user-created variables, Airflow [built-in variables and macros](https://airflow.apache.org/docs/apache-airflow/stable/templates-ref.html)) | **User-created variables: **Including hard-coded values directly in your code is generally not a good practice in software development. This is because they make your code less readable and more error-prone -- you may need to use the same value in multiple places and updating the same value in multiple places can be error-prone. The same principle also applies to when you write code to define your pipelines. Instead of including hard-coded values within your DAG or task definitions, you can store these values by creating variables in the Airflow UI or creating environmental variables and use these variables dynamically inside your code.
[Recommendations from Airflow documentation regarding using Variables](https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/variables.html): "Variables are global, and should only be used for overall configuration that covers the entire installation; to pass data from one Task/Operator to another, you should use XComs instead. We also recommend that you try to keep most of your settings and configuration in your DAG files, so it can be versioned using source control; Variables are really only for values that are truly runtime-dependent."
**Airflow built-in Variables: **You learned that Airflow has a set of built-in variables that contain information about the currently running DAG and its tasks, such as the logical date of the DAG run and task instance (for a list of such variables, check [here](https://airflow.apache.org/docs/apache-airflow/stable/templates-ref.html)). You learned that you can access these variables within a task function by passing the context dictionary as an argument to the function. You can also pass these variables directly to the PythonOperator using a syntax known as Jinja templating, which looks like this : "**{{ds}}**". You use double curly brackets and inside the brackets you specify the variable you'd like to access. In this example, ds represents the logical date of the DAG run. 
Let's see an example: Assume that your python_callable is a function that expects the name of a file. For example, this function loads some data to an s3 bucket and requires that you pass the file name.  And let's say you want to include the logical date in the file_name.
**def load_to_s3(file_name):    **
**    #code that loads data    **
**    print(file_name)**

So you can specify this information in the PythonOperator as follows:
**task_load_s3 = PythonOperator(task_id="load_to_d3",**
**         python_callable=load_to_s3,**
**         op_kwargs={'file_name': "data/created{{ds}}/file.csv"})** |
| Task groups | In the Airflow UI, you can group tasks using Task Groups to organize your DAGs and make them more readable. Inside the task group, you can define tasks and their dependencies using the bit-shift operators &lt;&lt;  and  &gt;&gt;.  You can create a Task Group using the  "with" statement, as shown in the following example.  

**from airflow.utils.task_group import TaskGroup  **
**with DAG(...):     **
**    start = DummyOperator(...)**
**    with TaskGroup('task_group')as task_group:**
**       task_a = PythonOperator(...)**
**       task_b = PythonOperator(...)**
**       task_a &gt;&gt; task_b**
**    end = DummyOperator(...)      **
**    start &gt;&gt; task_group &gt;&gt; end ** |
| Other practices (Airflow is an orchestrator not an executor) | • Heavy processing should be assumed by execution frameworks (e.g. Spark) not Airflow
• For large datasets, don't use XComs (push dataframes). Use intermediary data storage instead.
• Including code that is not part of your DAG or operator makes your DAG hard to maintain and read: consider keeping any extra code that is needed for your tasks in a separate file. |
