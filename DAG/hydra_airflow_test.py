from typing import Any, Dict

import httpx
import pendulum
from airflow.decorators import dag, task
from airflow.models.baseoperator import BaseOperator
from airflow.operators.email import EmailOperator
from airflow.utils.context import Context
import hydra
from omegaconf import DictConfig, OmegaConf


class GetRequestOperator(BaseOperator):
    """Custom operator to send GET request to provided url"""

    def __init__(self, *, url: str, **kwargs):
        super().__init__(**kwargs)
        self.url = url

    def execute(self, context: Context):
        return httpx.get(self.url).json()


# [START dag_decorator_usage]
@dag(
    schedule_interval=None,
    start_date=pendulum.datetime(2021, 1, 1, tz="UTC"),
    catchup=False,
    tags=['example'],
)
def example_dag_decorator(email: str = 'example@example.com'):
    """
    DAG to send server IP to email.

    :param email: Email to send IP to. Defaults to example@example.com.
    """
    get_ip = GetRequestOperator(task_id='get_ip', url="http://httpbin.org/get")

    @hydra.main(version_base=None, config_path="environments/", config_name="dev")
    def get_conf(cfg: DictConfig) -> DictConfig:
        print(OmegaConf.to_yaml(cfg))
        print("db.user :", cfg.db.user)
        print("db.password :", cfg.db.user)
        return cfg

    @task(multiple_outputs=True)
    def prepare_email(raw_json: Dict[str, Any], cfg: DictConfig) -> Dict[str, str]:
        external_ip = raw_json['origin']
        print(OmegaConf.to_yaml(cfg))
        print("db.user :", cfg.db.user)
        print("db.password :", cfg.db.user)
        return {
            'subject': f'Server connected from {external_ip}',
            'body': f'Seems like today your server executing Airflow is connected from IP {external_ip}<br>',
        }

    email_info = prepare_email(get_ip.output, get_conf.output)

    EmailOperator(
        task_id='send_email', to=email, subject=email_info['subject'], html_content=email_info['body']
    )


dag = example_dag_decorator()
