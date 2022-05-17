import airflow
from airflow import DAG
from airflow.operators.python_operator import PythonOperator

dag = DAG(
    dag_id='hello_world_a',
    default_args={
        "owner": "airflow",
        'start_date': airflow.utils.dates.days_ago(1),
    },
    schedule_interval=None
)


def print_hello(**context):
    task_params = context['dag_run'].conf['task_payload']
    print('Hello world a with {}'.format(task_params))

PythonOperator(
    task_id='hello_world_printer',
    python_callable=print_hello,
    provide_context=True,
    dag=dag)