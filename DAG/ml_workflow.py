import time
import airflow
from airflow import DAG
from airflow.operators.python import PythonOperator


def load_config():
    from omegaconf import OmegaConf
    import time
    import os

    config_path_default = os.path.abspath(os.path.join(__file__, '..', 'environments/default.yaml'))
    config_path_dev = os.path.abspath(os.path.join(__file__, '..', 'environments/dev', 'dev.yaml'))
    omega_cfg_dev = OmegaConf.load(config_path_dev)
    omega_cfg_default = OmegaConf.load(config_path_default)

    return OmegaConf.merge(omega_cfg_default, omega_cfg_dev)


def print_config():
    from omegaconf import OmegaConf
    import time
    time.sleep(120.0)
    print(OmegaConf.to_yaml(res))
    print("res.db.jobs = ", res.db.jobs)
    print("res.db.vyper_settings = ", res.db.vyper_settings)
    print("res.db = ", res.db)
    print("db.vyper_setting.tagger.output_bucket_path", res.db.vyper_settings.tagger.output_bucket_path)
    print("db.vyper_setting.slang_word_tagger.output_bucket_path",
          res.db.vyper_settings.slang_word_tagger.output_bucket_path)
    print("Sleeping the task for 5 minutes")
    time.sleep(300.0)
    print("db.vyper_setting.tagger.output_bucket_path", res.db.vyper_settings.tagger.output_bucket_path)
    print("db.vyper_setting.slang_word_tagger.output_bucket_path",
          res.db.vyper_settings.slang_word_tagger.output_bucket_path)


def print_hello(dag_run=None):
    import json
    # task_params = context['dag_run'].conf['task_payload']
    print(f"Remotely received value of {dag_run.conf.get('message')} for key=message")
    print(type(dag_run.conf.get('message')))
    json_obj = json.loads(dag_run.conf.get('message'))
    print("minio key - uploaded folder and key = ", json_obj['key'])
    # print('Hello world a with {}'.format({dag_run.conf.get('job_params')}))

    print_config()


with DAG(
        dag_id='ml_workflow',
        default_args={
            "owner": "airflow",
            'start_date': airflow.utils.dates.days_ago(1),
        },
        schedule_interval=None
) as dag:
    res = load_config()
    res.db.UDID = "ml_workflow"
    res.db.date = time.strftime("%Y%m%d-%H%M%S")
    PythonOperator(
        task_id='hello_world_printer',
        python_callable=print_hello
    )
