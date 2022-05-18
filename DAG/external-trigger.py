import json

from airflow import utils
from airflow.models import DAG
# from airflow.operators.dagrun_operator import TriggerDagRunOperator
from airflow.operators.trigger_dagrun import TriggerDagRunOperator
from airflow.operators.dummy import DummyOperator
from airflow.operators.python import BranchPythonOperator

dag = DAG(
    dag_id='external_trigger',
    default_args={
        "owner": "airflow",
        'start_date': utils.dates.days_ago(1),
    },
    schedule_interval='*/1 * * * *',
)


def consume_message(**kwargs):
    import subprocess
    subprocess.run(["pip", "install", "pika"])
    import pika
    credentials = pika.PlainCredentials('user', 'MbtnNcY7DXPMX0je')
    connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq',
                                                                   5672,
                                                                   '/',
                                                                   credentials))
    channel = connection.channel()
    channel.queue_declare(queue='external_airflow_triggers', durable=True)

    method_frame, header_frame, body = channel.basic_get(queue='external_airflow_triggers')
    if body:
        json_params = json.loads(body)
        kwargs['ti'].xcom_push(key='job_params', value=json.dumps(json_params['params']))
        channel.basic_ack(delivery_tag=method_frame.delivery_tag)
        connection.close()
        print("Got message ? {}".format(body))
        return json_params['task']
    else:
        return 'task_trash'


router = BranchPythonOperator(
    task_id='router',
    python_callable=consume_message,
    dag=dag,
    provide_context=True,
    depends_on_past=True
)

def trigger_dag_with_context(context, dag_run_obj):

    ti = context['task_instance']
    job_params = ti.xcom_pull(key='job_params', task_ids='router')
    dag_run_obj.payload = {'task_payload': job_params}
    return dag_run_obj

#
# def group(number, **kwargs):
#     # load the values if needed in the command you plan to execute
#     dyn_value = "{{ task_instance.xcom_pull(task_ids='push_func') }}"
#     return TriggerDagRunOperator(
#         trigger_dag_id='JOB_NAME_{}'.format(number),
#         bash_command='script.sh {} {}'.format(dyn_value, number),
#         dag=dag)
#
#
# task_a = trigger = TriggerDagRunOperator(
#     task_id='item',
#     trigger_dag_id="item",
#     dag=dag
#     conf={}
# )
#
#
# task_a = trigger = TriggerDagRunOperator(
#     task_id='hello_world_a',
#     trigger_dag_id="hello_world_a",
#     python_callable=trigger_dag_with_context,
#     params={'condition_param': True, 'task_payload': '{}'},
#     dag=dag,
#     provide_context=True,
# )
#
# task_b = TriggerDagRunOperator(
#     task_id='hello_world_b',
#     trigger_dag_id="hello_world_b",
#     python_callable=trigger_dag_with_context,
#     params={'condition_param': True, 'task_payload': '{}'},
#     dag=dag,
#     provide_context=True,
# )
#
# task_c = TriggerDagRunOperator(
#     task_id='hello_world_c',
#     trigger_dag_id="hello_world_c",
#     python_callable=trigger_dag_with_context,
#     params={'task_payload': '{}'},
#     dag=dag,
#     provide_context=True,
# )

task_trash = DummyOperator(
    task_id='task_trash',
    dag=dag
)

# router >> task_a
# router >> task_b
# router >> task_c
router >> task_trash
