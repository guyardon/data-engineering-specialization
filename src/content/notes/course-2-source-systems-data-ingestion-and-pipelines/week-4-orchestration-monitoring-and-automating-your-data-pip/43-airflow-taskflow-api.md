---
title: "4.3 Airflow Taskflow API"
course: "Course 2: Source Systems, Data Ingestion and Pipelines"
courseSlug: "course-2-source-systems-data-ingestion-and-pipelines"
courseOrder: 2
week: "Week 4: Orchestration, Monitoring and Automating Your Data Pipelines"
weekSlug: "week-4-orchestration-monitoring-and-automating-your-data-pip"
weekOrder: 4
order: 3
notionId: "1d6969a7-aa01-80b2-9800-eaa4f638389a"
---


## 4.3.1 Taskflow API Basics

**Airflow Taskflow API**

- Instead of instantiating a DAG object in a context manager, you use decorators @dag to wrap the dag definition and @task  to wrap the tasks
- You don't need to keep track of the task_id, the name of the python function, the name of the task variable like when using the DAG context manager with PythonOperators
![](/data-engineering-specialization-website/images/eccc4e22-5920-4f48-a8b1-370544df42ef.png)

![](/data-engineering-specialization-website/images/c2f92260-22c2-476a-b580-929e6a9b9c52.png)

![](/data-engineering-specialization-website/images/267cedf2-9f1b-436e-ae49-f49778ca6852.png)

- To pass Xcoms, we can either use the context dictionary with the xcom_push and xcom_pull from the task instance in the context dictionary OR
- return values from tasks and pass them to other tasks
![](/data-engineering-specialization-website/images/497f224c-4544-4e27-a589-2dafdda12422.png)


## 4.3.2 Taskflow API vs. Traditional Paradigm

**AirFlow Task API Example vs. Traditional Paradigm**

```python
from airflow import DAG
from airflow.operators.python import PythonOperator, BranchPythonOperator
from airflow.operators.empty import EmptyOperator
from datetime import datetime
from tasks_module import extract_from_api, check_ratio, print_case_greater_half, print_case_less_half

def extract_from_api(**context):
   import requests
   number_posts = 40
   location = "usa"
   url_link = "https://jobicy.com/api/v2/remote-jobs"
   response = requests.get(url_link, params={"count": number_posts, 
                                             "geo": location, 
                                             "industry": "engineering",
                                             "tag": "data engineer"}).json()
   count = 0
   for job in response['jobs']:
       if job['jobLevel'] == 'Senior':
           count += 1
   ratio = count / len(response['jobs'])
   context['ti'].xcom_push(key='ratio_us', value=ratio)

def check_ratio(**context):
   if float(context['ti'].xcom_pull(key='ratio_us', task_ids='extract_data'))>0.5:
       return 'print_greater' #task_id of the greater than case
   return 'print_less' #task_id of the less than case

def print_case_greater_half(**context):
   print("The ratio is greater than half: " + str(context['ti'].xcom_pull(key= 'ratio_us', task_ids='extract_data')))

def print_case_less_half(**context):
   print("The ratio is less than half: " + str(context['ti'].xcom_pull(key= 'ratio_us', task_ids='extract_data')))

with DAG(dag_id="branching", start_date=datetime(2024, 3, 13), schedule='@daily', catchup=False):
    task_1 = PythonOperator(task_id='extract_data', python_callable=extract_from_api)
    task_2 = BranchPythonOperator(task_id='check_ratio', python_callable=check_ratio)
    task_3 = PythonOperator(task_id='print_greater', python_callable=print_case_greater_half)
    task_4 = PythonOperator(task_id='print_less', python_callable=print_case_less_half)
    task_5 = EmptyOperator(task_id='do_nothing', trigger_rule = 'none_failed_min_one_success')
    
    task_1 >> task_2 >> [task_3, task_4] >> task_5
```

- Note the use of context manager
- Note the BranchPythonOperator which is used before branching to multiple tasks
- Note that Xcoms are set in the context['ti'] (task instance) key using the xcom_push method and retrieved using the xcom_pull method.
- Note that the task that is passed to the BranchPythonOperator returns the downstream task based on a condition.
- Note the Empty operator at the end, which is triggered with *none_failed_min_one_success (*All upstream tasks have not `failed` or `upstream_failed`, and at least one upstream task has succeeded). This is because we want this task to execute regardless of which previous task was executed, otherwise it will be skipped.
- Note this syntax:  task_1 &gt;&gt; task_2 &gt;&gt; [task_3, task_4] &gt;&gt; task_5
```python
from airflow import DAG
from datetime import datetime
from airflow.decorators import dag, task

@ dag(start_date=datetime(2024, 3, 13),schedule='@daily', catchup=False)
def example_branching():
    @task
    def extract_from_api():
        import requests
        number_posts = 40
        location = "usa"
        url_link = "https://jobicy.com/api/v2/remote-jobs"
        response = requests.get(url_link, 
                    params={"count": number_posts,  
                            "geo": location, 
                            "industry": "engineering",
                            "tag": "data engineer"}).json()
        count = 0
        for job in response['jobs']:
            if job['jobLevel'] == 'Senior':
                count += 1
        ratio = count / len(response['jobs'])
        return ratio

    @task.branch()
    def check_ratio(ti=None):
        if float(ti.xcom_pull(task_ids='extract_from_api')) > 0.5:
            return 'print_case_greater_half' # task_id of the greater than case
        return 'print_case_less_half'  # task_id of the less than case

    @task
    def print_case_greater_half(ti=None):
        print( "The ratio is greater than half: " +
                str(ti.xcom_pull(key='ratio_us', task_ids='extract_data')))

    @task
    def print_case_less_half(ti=None):
        print("The ratio is less than half: " +
                str(ti.xcom_pull(key='ratio_us', task_ids='extract_data')))

    @task(trigger_rule='none_failed_min_one_success')
    def empty_task():
        pass
    
    extract_from_api() >> check_ratio() >> [print_case_greater_half(), print_case_less_half()] >> empty_task()

example_branching()
```

- The DAG is defined as a function, decorated with @airflow.decorators.dag
- Each task is defined in side the dag function, and decorated with @airflow.decorators.task or @airflow.decorators.task.branch
- Note that the task that is decorated with @airflow.decorators.task.branch  returns the downstream task based on a condition.
- Note that instead of the task instance object is now passed to the tasks themselves (ti) which can then be called using xcom_pull. 
- In Airflow, when a task (decorated with `@task` or `PythonOperator`) **returns a value**, it is **automatically pushed to XCom**. This behavior eliminates the need to explicitly call `xcom_push`.
- The `task_instance` (ti) object is only needed when a task interacts with **XComs** (e.g., using `xcom_pull`) or requires runtime metadata (like execution date, DAG run info, etc.).
- The relationship between tasks is defined like this: 
- extract_from_api() &gt;&gt; check_ratio() &gt;&gt; [print_case_greater_half(), print_case_less_half()] &gt;&gt; empty_task()
- Note that each task is "called". In fact, it calls the decorator, which returns a DAG Node object, it doesn't actually execute the task. The bit shift operator is overloaded to set downstream and upstream tasks for each task.
- The DAG is "called" after defining it. This calls the decorator @dag which registers the DAG with AirFlow. it doesn't execute the DAG.
