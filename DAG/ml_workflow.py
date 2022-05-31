import time
import airflow
from airflow import DAG
from airflow.operators.python import PythonOperator
import os


def load_config():
    from omegaconf import OmegaConf
    import time
    config_path_default = os.path.abspath(os.path.join(__file__, '..', 'environments/default.yaml'))
    config_path_dev = os.path.abspath(os.path.join(__file__, '..', 'environments/dev', 'dev.yaml'))
    omega_cfg_dev = OmegaConf.load(config_path_dev)
    omega_cfg_default = OmegaConf.load(config_path_default)

    return OmegaConf.merge(omega_cfg_default, omega_cfg_dev)


def print_config():
    from omegaconf import OmegaConf
    import time
    print("Sleeping the task for 2 minutes")
    # time.sleep(120.0)
    print(OmegaConf.to_yaml(res))
    print("res.db.jobs = ", res.db.jobs)
    print("res.db.vyper_settings = ", res.db.vyper_settings)
    print("res.db = ", res.db)
    print("db.vyper_setting.tagger.output_bucket_path = ", res.db.vyper_settings.tagger.output_bucket_path)
    print("db.vyper_setting.slang_word_tagger.output_bucket_path = ",
          res.db.vyper_settings.slang_word_tagger.output_bucket_path)
    print("Sleeping the task for 5 minutes")
    # time.sleep(300.0)
    print("db.vyper_setting.tagger.output_bucket_path = ", res.db.vyper_settings.tagger.output_bucket_path)
    print("db.vyper_setting.slang_word_tagger.output_bucket_path = ",
          res.db.vyper_settings.slang_word_tagger.output_bucket_path)


def copy_object(dag_run=None):
    # Omegaconf object updated in this func scope are not persistent

    import json
    from omegaconf import OmegaConf
    from minio import Minio
    print(f"Remotely received value of {dag_run.conf.get('message')} for key=message")
    print(type(dag_run.conf.get('message')))
    json_obj = json.loads(dag_run.conf.get('message'))
    print("minio key - uploaded folder and key = ", json_obj['Key'])
    # print('Hello world a with {}'.format({dag_run.conf.get('job_params')}))
    client = Minio(
        "minio.airflow.svc.cluster.local:9000",
        access_key="ruxiu105QkeBjUXVOq4j",
        secret_key="UfvrsBtgZpwOqwiht239C5c3lJM4vWnLQcdMCuB8",
        secure=False,
    )
    res.db.UDID = os.path.splitext(json_obj['Key'])[0].split('/')[-1]
    object_path = json_obj['Key'].partition("dag-input/")[2]
    airflow_file_path = "outputs/copied_" + os.path.basename(object_path)
    print("object path of copied file = ", object_path)
    print(" Trying to copy file", json_obj['Key'], "from S3 bucket")
    client.fget_object(
        "dag-input", json_obj['Key'].partition("dag-input/")[2], airflow_file_path
    )
    print("downloaded file saved in ", airflow_file_path)
    print_config()


def upload_object(dag_run=None):
    from minio import Minio
    from omegaconf import OmegaConf
    import json
    json_obj = json.loads(dag_run.conf.get('message'))
    object_path = json_obj['Key'].partition("dag-input/")[2]
    airflow_file_path = "outputs/copied_" + os.path.basename(object_path)
    res.db.UDID = os.path.splitext(json_obj['Key'])[0].split('/')[-1]
    print(OmegaConf.to_yaml(res))
    client = Minio(
        "minio.airflow.svc.cluster.local:9000",
        access_key="ruxiu105QkeBjUXVOq4j",
        secret_key="UfvrsBtgZpwOqwiht239C5c3lJM4vWnLQcdMCuB8",
        secure=False,
    )
    client.fput_object(
        "dag-input",
        res.db.vyper_settings.tagger.output_bucket_path + "/" + os.path.basename(airflow_file_path),
        airflow_file_path
    )

    print("Successfully uploaded data to minio - path is :  ",
          res.db.vyper_settings.tagger.output_bucket_path + "/"
          + os.path.basename(airflow_file_path))


with DAG(
        dag_id='ml_workflow',
        default_args={
            "owner": "airflow",
            'start_date': airflow.utils.dates.days_ago(1),
        },
        schedule_interval=None
) as dag:
    res = load_config()

    # res.db.date = time.strftime("%Y%m%d-%H%M%S")
    res.db.date = time.strftime("%Y%m%d")

    copy_object = PythonOperator(
        task_id='copy_object',
        python_callable=copy_object
    )

    upload_object = PythonOperator(
        task_id="upload_object",
        python_callable=upload_object
    )

    copy_object >> upload_object
