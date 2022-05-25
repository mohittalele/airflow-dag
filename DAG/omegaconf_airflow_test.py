import logging
import shutil
import time
from pprint import pprint

import pendulum

from airflow import DAG
from airflow.decorators import task
import os
import hydra
from omegaconf import OmegaConf

log = logging.getLogger(__name__)

with DAG(
        dag_id='example_python_operator',
        schedule_interval=None,
        start_date=pendulum.datetime(2021, 1, 1, tz="UTC"),
        catchup=False,
        tags=['example'],
) as dag:
    # [START howto_operator_python]

    CONFIG_PATH = os.path.abspath(os.path.join(__file__, '..', 'environments'))
    env = 'prod.yaml'
    CONFIG_PATH_1 = os.path.abspath(os.path.join(__file__, '..', 'environments/', env))
    print("NEW CONFIG_PATH", CONFIG_PATH_1)


    @task(task_id="omegaconf_airflow_test")
    def print_context( ds=None, **kwargs):
        """Print the Airflow context and ds variable from the context."""

        print("CONFIG_PATH :", CONFIG_PATH)
        print("CONFIG_PATH_1 :", CONFIG_PATH_1)

        print("------- omegaconf---------------")
        omega_cfg_1 = OmegaConf.load(CONFIG_PATH_1)
        print(OmegaConf.to_yaml(omega_cfg_1))
        print("db.user :", omega_cfg_1.db.user)
        print("db.password :", omega_cfg_1.db.password)
        print("------- omegaconf---------------")

        print("current work dir :", os.getcwd())
        print("------- omegaconf---------------")
        pprint(kwargs)
        print(ds)
        return omega_cfg_1


    run_this = print_context()
