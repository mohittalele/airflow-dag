from omegaconf import OmegaConf
import hydra
from airflow.decorators import dag, task
import pendulum


@dag(schedule_interval='None', start_date=pendulum.datetime(2021, 1, 1, tz="UTC"), catchup=False)
def dag():
    @task(task_id="print_config")
    @hydra.main(version_base=None, config_path="../config", config_name="prod")
    def print_config(cfg):

        print(OmegaConf.to_yaml(cfg))
        print(OmegaConf.to_yaml(cfg))
        print("db.user :", cfg.db.user)
        print("db.password :", cfg.db.user)


dag = dag()

from omegaconf import DictConfig, OmegaConf
import hydra


@hydra.main(version_base=None, config_path="../config", config_name="prod")
def my_app(cfg):
    print(OmegaConf.to_yaml(cfg))
    print("db.user :", cfg.db.user)
    print("db.password :", cfg.db.user)


if __name__ == "__main__":
    my_app()
