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
import time


CONFIG_PATH = os.path.abspath(os.path.join(__file__, '..', 'environments/prod'))
print("CONFIG_PATH :", CONFIG_PATH)
CONFIG_PATH_prod = os.path.abspath(os.path.join(__file__, '..', 'environments/prod', 'prod.yaml'))
print("NEW CONFIG_PATH_1", CONFIG_PATH_prod)
CONFIG_PATH_dev = os.path.abspath(os.path.join(__file__, '..', 'environments/dev', 'dev.yaml'))
print("NEW CONFIG_PATH_2 : ", CONFIG_PATH_dev)
CONFIG_PATH_default = os.path.abspath(os.path.join(__file__, '..', 'environments/default.yaml'))


@hydra.main(version_base=None, config_path=CONFIG_PATH, config_name="prod")
def my_app(cfg: DictConfig):
    print("------- Hydra Conf---------------")
    print(OmegaConf.to_yaml(cfg))
    print(OmegaConf)
    print("db.user :", cfg.db.user)
    print("db.password :", cfg.db.password)
    print("------- Hydra Conf End---------------")

    print("------- omegaconf---------------")
    omega_cfg_prod = OmegaConf.load(CONFIG_PATH_prod)
    omega_cfg_dev = OmegaConf.load(CONFIG_PATH_dev)
    omega_cfg_default = OmegaConf.load(CONFIG_PATH_default)
    res = OmegaConf.merge(omega_cfg_default, omega_cfg_dev)
    res.db.UDID = "ABCDEF"
    res.db.date = time.strftime("%Y%m%d-%H%M%S")

    print(OmegaConf.to_yaml(res))
    print("db.user :", res.db.user)
    print("db.password :", res.db.password)
    print("db.driver :", type(res.db.driver))
    print("db.additional_key :", res.db.additional_key)
    print("db.additional_key :", res.db.UDID)

if __name__ == "__main__":
    my_app()
