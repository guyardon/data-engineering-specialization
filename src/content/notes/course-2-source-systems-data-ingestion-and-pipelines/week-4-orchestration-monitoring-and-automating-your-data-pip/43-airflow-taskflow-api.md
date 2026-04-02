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

The **Taskflow API** is `Airflow`'s modern, decorator-based approach to defining DAGs and tasks. Instead of instantiating a DAG object in a context manager, you use `@dag` to wrap the DAG definition and `@task` to wrap individual tasks. This eliminates the need to manually track task IDs, function names, and task variable names.

![](/data-engineering-specialization-website/images/eccc4e22-5920-4f48-a8b1-370544df42ef.png)

![](/data-engineering-specialization-website/images/c2f92260-22c2-476a-b580-929e6a9b9c52.png)

![](/data-engineering-specialization-website/images/267cedf2-9f1b-436e-ae49-f49778ca6852.png)

For passing data between tasks, you have two options: use the context dictionary with `xcom_push` and `xcom_pull` from the task instance, or simply **return values from tasks and pass them as arguments to other tasks** -- the cleaner Taskflow approach.

![](/data-engineering-specialization-website/images/497f224c-4544-4e27-a589-2dafdda12422.png)

## 4.3.2 Taskflow API vs. Traditional Paradigm

The two examples below implement the same branching DAG -- one using the traditional context manager with PythonOperators, the other using the Taskflow API. Comparing them highlights how much boilerplate the Taskflow API eliminates.


---

**Traditional Paradigm:**

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

Key points in the traditional approach:

- Uses the `DAG()` context manager.
- **BranchPythonOperator** returns the task ID of the downstream task to execute based on a condition.
- XComs are pushed and pulled via `context['ti']`.
- The final **EmptyOperator** uses `trigger_rule='none_failed_min_one_success'` so it executes regardless of which branch ran.

---

**Taskflow API:**

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

Key differences in the Taskflow approach:

- The DAG is defined as a function decorated with `@dag`.
- Each task is a function inside the DAG function, decorated with `@task` or `@task.branch()`.
- The `task_instance` (`ti`) object is passed directly to tasks that need XCom access or runtime metadata.
- When a `@task`-decorated function **returns a value**, it is **automatically pushed to XCom** -- no explicit `xcom_push` needed.
- Task relationships use the same `>>` syntax, but each task is "called" (e.g., `extract_from_api()`). This calls the decorator, which returns a DAG Node object rather than executing the task. The bit-shift operator is overloaded to set upstream/downstream relationships.
- Calling the DAG function (e.g., `example_branching()`) triggers the `@dag` decorator to register the DAG with `Airflow` -- it does not execute the DAG.
