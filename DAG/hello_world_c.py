import airflow
from airflow import DAG
from airflow.operators.python import PythonOperator


def print_hello(dag_run=None):
    # task_params = context['dag_run'].conf['task_payload']
    print(f"Remotely received value of {dag_run.conf.get('job_params')} for key=job_params")
    # print('Hello world a with {}'.format({dag_run.conf.get('job_params')}))


with DAG(
        dag_id='hello_world_c',
        default_args={
            "owner": "airflow",
            'start_date': airflow.utils.dates.days_ago(1),
        },
        schedule_interval=None
) as dag:
    PythonOperator(
        task_id='hello_world_printer',
        python_callable=print_hello
    )
