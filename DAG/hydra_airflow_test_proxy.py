import logging
import shutil
import time
from pprint import pprint

import pendulum

from airflow import DAG
from airflow.decorators import task
import os
log = logging.getLogger(__name__)

with DAG(
    dag_id='example_python_operator',
    schedule_interval=None,
    start_date=pendulum.datetime(2021, 1, 1, tz="UTC"),
    catchup=False,
    tags=['example'],
) as dag:
    # [START howto_operator_python]
    @task(task_id="print_the_context")
    def print_context(ds=None, **kwargs):
        """Print the Airflow context and ds variable from the context."""
        print(os.getcwd())
        pprint(kwargs)
        print(ds)
        return 'Whatever you return gets printed in the logs'

    run_this = print_context()