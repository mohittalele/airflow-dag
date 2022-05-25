import logging
from pprint import pprint
import pendulum
from airflow import DAG
from airflow.decorators import task
import os
import hydra
from omegaconf import OmegaConf
from airflow.models import Variable

log = logging.getLogger(__name__)

with DAG(
        dag_id='omegaconf_airflow_test',
        schedule_interval=None,
        start_date=pendulum.datetime(2021, 1, 1, tz="UTC"),
        catchup=False,
        tags=['example'],
) as dag:
    # [START howto_operator_python]

    CONFIG_PATH = os.path.abspath(os.path.join(__file__, '..', 'environments'))
    env = Variable.get("ENV_VAR") + '.yaml'
    CONFIG_PATH_1 = os.path.abspath(os.path.join(__file__, '..', 'environments/', env))
    print("NEW CONFIG_PATH", CONFIG_PATH_1)
    omega_cfg_1 = OmegaConf.load(CONFIG_PATH_1)


    @task(task_id="omegaconf_test")
    def omegaconf_test(ds=None, **kwargs):
        """Print the Airflow context and ds variable from the context."""

        print("CONFIG_PATH :", CONFIG_PATH)
        print("CONFIG_PATH_1 :", CONFIG_PATH_1)

        print("------- omegaconf---------------")
        print(OmegaConf.to_yaml(omega_cfg_1))
        print("db.user :", omega_cfg_1.db.user)
        print("db.password :", omega_cfg_1.db.password)
        print("------- omegaconf---------------")

        pprint(kwargs)
        print(ds)
        return 'Whatever you return gets printed in the logs'


    @task(task_id="second_task_omegaconf_test")
    def second_task_omegaconf_test(ds=None, **kwargs):
        """Print the Airflow context and ds variable from the context."""

        print("CONFIG_PATH :", CONFIG_PATH)
        print("CONFIG_PATH_1 :", CONFIG_PATH_1)

        print("------- omegaconf---------------")
        print(OmegaConf.to_yaml(omega_cfg_1))
        print("db.user :", omega_cfg_1.db.user)
        print("db.password :", omega_cfg_1.db.password)
        print("db.driver :", omega_cfg_1.db.driver)
        print("------- omegaconf---------------")

        pprint(kwargs)
        print(ds)
        return 'This is second task'


    print_context_instance = omegaconf_test()
    second_task_omegaconf_test_instance = second_task_omegaconf_test()
    print_context_instance >> second_task_omegaconf_test_instance
