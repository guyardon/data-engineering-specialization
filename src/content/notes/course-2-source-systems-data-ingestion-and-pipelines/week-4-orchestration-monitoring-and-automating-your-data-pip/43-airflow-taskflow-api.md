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

The [Taskflow API](https://airflow.apache.org/docs/apache-airflow/stable/tutorial/taskflow.html) is `Airflow`'s modern, decorator-based approach to defining DAGs and tasks. It replaces the traditional pattern of instantiating a `DAG()` context manager and wrapping functions in `PythonOperator` with two simple decorators: `@dag` for the DAG definition and `@task` for individual tasks.

**Traditional Approach**

In the traditional approach, you need to keep track of three names for every task: the `task_id` string, the Python callable, and the task variable name. The DAG is created with a context manager:

```python
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

def extract_data():
    print("Done with the extraction task")

def transform_data():
    print("Done with the transformation task")

def load_data():
    print("Done with the loading task")

# DAG created via context manager
with DAG(
    dag_id="my_first_dag",
    description="ETL pipeline",
    tags=["data_engineering_team"],
    schedule="@daily",
    start_date=datetime(2024, 12, 1),
    catchup=False,
):
    # each task requires a task_id, a python_callable, and a variable name
    task_1 = PythonOperator(task_id="extract", python_callable=extract_data)
    task_2 = PythonOperator(task_id="transform", python_callable=transform_data)
    task_3 = PythonOperator(task_id="load", python_callable=load_data)

    task_1 >> task_2 >> task_3
```

**Taskflow Approach**

With the Taskflow API, the `@dag` decorator replaces the context manager and the `@task` decorator replaces `PythonOperator`. The function name automatically becomes the `task_id`, so there's only one name to track per task:

```python
from datetime import datetime
from airflow.decorators import dag, task

@dag(
    description="ETL pipeline",
    tags=["data_engineering_team"],
    schedule="@daily",
    start_date=datetime(2024, 12, 1),
    catchup=False,
)
def my_first_dag():
    # @task implicitly wraps each function in a PythonOperator
    # the function name becomes the task_id automatically
    @task
    def extract_data():
        print("Done with the extraction task")

    @task
    def transform_data():
        print("Done with the transformation task")

    @task
    def load_data():
        print("Done with the loading task")

    # dependencies use function calls -- the decorator returns a DAG node,
    # not the function's return value
    extract_data() >> transform_data() >> load_data()

# calling the DAG function registers it with Airflow (does not execute it)
my_first_dag()
```

---

**Passing Data Between Tasks**

The Taskflow API simplifies XCom usage. Instead of manually calling `xcom_push` and `xcom_pull`, you simply **return a value** from one task and **pass it as an argument** to another. `Airflow` handles the XCom push/pull behind the scenes:

```python
from datetime import datetime
from airflow.decorators import dag, task

@dag(
    start_date=datetime(2024, 3, 13),
    description="XCom with Taskflow",
    tags=["data_engineering_team"],
    schedule="@daily",
    catchup=False,
)
def example_xcom_taskapi():

    @task
    def extract_from_api():
        # returning a value automatically pushes it to XCom
        ratio_senior_jobs = 0.65
        return ratio_senior_jobs

    @task
    def print_data(geo_ratios: dict):
        # the value is received as a normal function argument
        print(geo_ratios)

    # pass the return value of extract_from_api() directly to print_data()
    # Airflow wires the XCom connection and sets the dependency automatically
    data = extract_from_api()
    print_data(data)

example_xcom_taskapi()
```

## 4.3.2 Taskflow API vs. Traditional Paradigm

The two examples below implement the **same branching DAG** -- one using the traditional approach, the other using the Taskflow API. The DAG extracts job data from an API, computes a ratio, and branches based on whether the ratio exceeds 0.5.

**Traditional Paradigm**

```python
from airflow import DAG
from airflow.operators.python import PythonOperator, BranchPythonOperator
from airflow.operators.empty import EmptyOperator
from datetime import datetime

def extract_from_api(**context):
    """Extract job data and push the senior ratio to XCom."""
    import requests

    response = requests.get(
        "https://jobicy.com/api/v2/remote-jobs",
        params={
            "count": 40, "geo": "usa",
            "industry": "engineering", "tag": "data engineer",
        },
    ).json()

    count = sum(1 for job in response["jobs"] if job["jobLevel"] == "Senior")
    ratio = count / len(response["jobs"])

    # manually push the value to XCom via the task instance
    context["ti"].xcom_push(key="ratio_us", value=ratio)


def check_ratio(**context):
    """Branch based on the ratio -- returns the task_id to execute next."""
    ratio = float(context["ti"].xcom_pull(key="ratio_us", task_ids="extract_data"))
    if ratio > 0.5:
        return "print_greater"      # must match a downstream task_id
    return "print_less"


def print_case_greater(**context):
    ratio = context["ti"].xcom_pull(key="ratio_us", task_ids="extract_data")
    print(f"The ratio is greater than half: {ratio}")


def print_case_less(**context):
    ratio = context["ti"].xcom_pull(key="ratio_us", task_ids="extract_data")
    print(f"The ratio is less than half: {ratio}")


with DAG(
    dag_id="branching",
    start_date=datetime(2024, 3, 13),
    schedule="@daily",
    catchup=False,
):
    # each task maps a task_id to a python_callable
    task_1 = PythonOperator(task_id="extract_data", python_callable=extract_from_api)
    task_2 = BranchPythonOperator(task_id="check_ratio", python_callable=check_ratio)
    task_3 = PythonOperator(task_id="print_greater", python_callable=print_case_greater)
    task_4 = PythonOperator(task_id="print_less", python_callable=print_case_less)

    # EmptyOperator with trigger_rule ensures it runs after either branch completes
    task_5 = EmptyOperator(
        task_id="do_nothing",
        trigger_rule="none_failed_min_one_success",
    )

    task_1 >> task_2 >> [task_3, task_4] >> task_5
```

**Taskflow Paradigm**

```python
from datetime import datetime
from airflow.decorators import dag, task

@dag(start_date=datetime(2024, 3, 13), schedule="@daily", catchup=False)
def example_branching():

    @task
    def extract_from_api():
        """Return value is automatically pushed to XCom -- no manual push needed."""
        import requests

        response = requests.get(
            "https://jobicy.com/api/v2/remote-jobs",
            params={
                "count": 40, "geo": "usa",
                "industry": "engineering", "tag": "data engineer",
            },
        ).json()

        count = sum(1 for job in response["jobs"] if job["jobLevel"] == "Senior")
        return count / len(response["jobs"])

    @task.branch()
    def check_ratio(ti=None):
        """@task.branch() replaces BranchPythonOperator."""
        ratio = float(ti.xcom_pull(task_ids="extract_from_api"))
        if ratio > 0.5:
            return "print_case_greater"     # function name = task_id
        return "print_case_less"

    @task
    def print_case_greater(ti=None):
        ratio = ti.xcom_pull(task_ids="extract_from_api")
        print(f"The ratio is greater than half: {ratio}")

    @task
    def print_case_less(ti=None):
        ratio = ti.xcom_pull(task_ids="extract_from_api")
        print(f"The ratio is less than half: {ratio}")

    @task(trigger_rule="none_failed_min_one_success")
    def join():
        """Replaces EmptyOperator -- runs after either branch completes."""
        pass

    # function calls return DAG nodes, not actual return values
    extract_from_api() >> check_ratio() >> [print_case_greater(), print_case_less()] >> join()

# register the DAG with Airflow
example_branching()
```

---

**Comparison**

| Aspect | Traditional | Taskflow API |
|---|---|---|
| DAG definition | `with DAG()` context manager | `@dag` decorator on a function |
| Task definition | `PythonOperator(task_id=..., python_callable=...)` | `@task` decorator -- function name becomes `task_id` |
| Branching | `BranchPythonOperator` | `@task.branch()` |
| Join/no-op task | `EmptyOperator` | `@task` with `pass` body |
| XCom push | `context["ti"].xcom_push(key=..., value=...)` | `return value` from the task function |
| XCom pull | `context["ti"].xcom_pull(key=..., task_ids=...)` | Pass return value as argument, or use `ti.xcom_pull()` |
| Dependency syntax | `task_variable >> task_variable` | `task_function() >> task_function()` |
| Names to track per task | 3 (task_id, callable, variable) | 1 (function name) |
| DAG registration | Automatic via context manager | Call the decorated function (e.g., `my_dag()`) |
| When to use | Mixed operator types, complex provider integrations | Pure Python tasks with data passing between them |
