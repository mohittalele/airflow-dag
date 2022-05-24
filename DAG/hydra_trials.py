from omegaconf import OmegaConf
import hydra
from airflow.decorators import dag, task
import pendulum


@dag(
    dag_id="hydra_trials",
    schedule_interval=None,
    start_date=pendulum.datetime(2021, 1, 1, tz="UTC"),
    catchup=False)
def dag():

    # @hydra.main(version_base=None, config_path="../config", config_name="prod")
    @task(task_id="print_config")
    def print_config(cfg):

        print(OmegaConf.to_yaml(cfg))
        print(OmegaConf.to_yaml(cfg))
        print("db.user :", cfg.db.user)
        print("db.password :", cfg.db.user)


hydra_trials = dag()

# from omegaconf import DictConfig, OmegaConf
# import hydra
#
#
# @hydra.main(version_base=None, config_path="../config", config_name="prod")
# def my_app(cfg):
#     print(OmegaConf.to_yaml(cfg))
#     print("db.user :", cfg.db.user)
#     print("db.password :", cfg.db.user)
#
#
# if __name__ == "__main__":
#     my_app()