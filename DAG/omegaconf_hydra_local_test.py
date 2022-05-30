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
    print("type of object res  :", type(res))
    print("db.additional_key :", res.db.additional_key)
    print("db.additional_key :", res.db.UDID)
    print("res.db = ", res.db)
    print("db.vyper_setting.tagger.output_bucket_path", res.db.vyper_settings.tagger.output_bucket_path)
    print("db.vyper_setting.slang_word_tagger.output_bucket_path",
          res.db.vyper_settings.slang_word_tagger.output_bucket_path)
    object_path = "dag-input/airflow-dag/validation-data/yoda.jpg"
    OmegaConf.update(res, "db.vyper_settings.tagger.airflow_file_path", "outputs/copied_" + os.path.basename(object_path))
    print("db.vyper_settings.tagger.airflow_file_path = ", res.db.vyper_settings.tagger.airflow_file_path)

if __name__ == "__main__":
    import json

    jsonStr = '{"EventName":"s3:ObjectAccessed:Head","Key":"dag-input/POC_architecture-Vyper_POC_option1.jpg","Records":[{"eventVersion":"2.0","eventSource":"minio:s3","awsRegion":"","eventTime":"2022-05-20T16:15:11.096Z","eventName":"s3:ObjectAccessed:Head","userIdentity":{"principalId":"zjtqz8Q0pIhArAv4SzMr"},"requestParameters":{"principalId":"zjtqz8Q0pIhArAv4SzMr","region":"","sourceIPAddress":"172.17.0.6"},"responseElements":{"content-length":"108836","x-amz-request-id":"16F0DC52B9057406","x-minio-deployment-id":"17d0d6c4-617a-41c5-96e6-743e8a3e102b","x-minio-origin-endpoint":"http://172.17.0.6:9000"},"s3":{"s3SchemaVersion":"1.0","configurationId":"Config","bucket":{"name":"dag-input","ownerIdentity":{"principalId":"zjtqz8Q0pIhArAv4SzMr"},"arn":"arn:aws:s3:::dag-input"},"object":{"key":"POC_architecture-Vyper_POC_option1.jpg","size":108836,"eTag":"f6529d47dcc300a546b53a58d3253e9f","contentType":"image/jpeg","userMetadata":{"content-type":"image/jpeg"},"sequencer":"16F0DC52B91FEC32"}},"source":{"host":"172.17.0.6","port":"","userAgent":"MinIO (linux; amd64) minio-go/v7.0.24"}}]}'
    pythonObj = json.loads(jsonStr)
    print("key name = ", pythonObj['Records'][0]['s3']['object']['key'])
    print("bucket name = ", pythonObj['Records'][0]['s3']['bucket']['name'])
    my_app()
