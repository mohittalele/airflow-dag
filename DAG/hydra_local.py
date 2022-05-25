# import hydra
# from airflow.decorators import dag, task
# import pendulum
#
#
# @dag(
#     dag_id="hydra",
#     schedule_interval=None,
#     start_date=pendulum.datetime(2021, 1, 1, tz="UTC"),
#     catchup=False)
# def dag():
#
#     @hydra.main(version_base=None, config_path=".", config_name="prod")
#     @task(task_id="print_config")
#     def print_config(cfg):
#         print("db.user :", cfg.db.user)
#         print("db.password :", cfg.db.user)
#
#     print_config_instance = print_config()
#
# hydra_trials = dag()

from omegaconf import DictConfig, OmegaConf
import hydra
import os

CONFIG_PATH = os.path.abspath(os.path.join(__file__, '..', 'environments'))
print("CONFIG_PATH :", CONFIG_PATH)
env = 'prod.yaml'
CONFIG_PATH_1 = os.path.abspath(os.path.join(__file__, '..', 'environments/', env))
print("NEW CONFIG_PATH", CONFIG_PATH_1)


@hydra.main(version_base=None, config_path=CONFIG_PATH, config_name="dev")
def my_app(cfg: DictConfig):
    print(OmegaConf.to_yaml(cfg))
    OmegaConf.save(config=cfg, f='cfg.yaml')
    print(OmegaConf)
    print("db.user :", cfg.db.user)
    print("db.password :", cfg.db.password)

    print("------- omegaconf---------------")
    omega_cfg_1 = OmegaConf.load(CONFIG_PATH_1)
    print(OmegaConf.to_yaml(omega_cfg_1))
    print("db.user :", omega_cfg_1.db.user)
    print("db.password :", omega_cfg_1.db.password)


if __name__ == "__main__":
    my_app()
