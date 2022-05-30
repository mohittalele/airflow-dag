#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

"""
Example DAG demonstrating the usage of BranchPythonOperator with depends_on_past=True, where tasks may be run
or skipped on alternating runs.
"""
import pendulum
import json
from airflow import DAG
from airflow.operators.dummy import DummyOperator
from airflow.operators.python import BranchPythonOperator
from airflow.operators.trigger_dagrun import TriggerDagRunOperator
from airflow import utils


def should_run(**kwargs):
    """
    Determine which empty_task should be run based on if the execution date minute is even or odd.

    :param dict kwargs: Context
    :return: Id of the task to run
    :rtype: str
    """
    print(
        f"------------- exec dttm = {kwargs['execution_date']} and minute = {kwargs['execution_date'].minute}"
    )
    if kwargs['execution_date'].minute % 2 == 0:
        return "empty_task_1"
    else:
        return "empty_task_2"


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
        print("Got message ? {}".format(body))
        print('params' in json_params)
        print('Key' in json_params)
        if 'params' in json_params:
            kwargs['ti'].xcom_push(key='job_params', value=json.dumps(json_params['params']))
            channel.basic_ack(delivery_tag=method_frame.delivery_tag)
            connection.close()
            print("Got message ? {}".format(body))
            return json_params['task']
        elif 'Key' in json_params:
            kwargs['ti'].xcom_push(key='message', value=json.dumps(json_params))
            channel.basic_ack(delivery_tag=method_frame.delivery_tag)
            connection.close()
            print("Got message ? {}".format(body))
            return 'ml_workflow'
    else:
        return 'task_trash'


with DAG(
        dag_id='external_trigger_bug_fix',
        schedule_interval='*/1 * * * *',
        start_date=pendulum.datetime(2021, 1, 1, tz="UTC"),
        catchup=False,
        default_args={'depends_on_past': True},
        tags=['example'],
) as dag:
    # cond = BranchPythonOperator(
    #     task_id='condition',
    #     python_callable=should_run,
    # )
    router = BranchPythonOperator(
        task_id='router',
        python_callable=consume_message,
    )

    task_trash = DummyOperator(task_id='task_trash')

    task_a = TriggerDagRunOperator(
        # trigger_run_id="test_trigger_dagrun",
        task_id='hello_world_a',
        trigger_dag_id="hello_world_a",
        # conf={'message': '{{ dag_run.conf.get("message") }}'},
        conf={
            "job_params":
                "{{ ti.xcom_pull(task_ids='router', key='job_params') }}"},
    )
    task_b = TriggerDagRunOperator(
        task_id='hello_world_b',
        trigger_dag_id="hello_world_b",
        conf={
            "job_params":
                "{{ ti.xcom_pull(task_ids='router', key='job_params') }}"},
    )
    task_c = TriggerDagRunOperator(
        task_id='hello_world_c',
        trigger_dag_id="hello_world_c",
        conf={
            "job_params":
                "{{ ti.xcom_pull(task_ids='router', key='job_params') }}"},
    )
    ml_workflow = TriggerDagRunOperator(
        task_id='ml_workflow',
        trigger_dag_id="ml_workflow",
        conf={
            "message":
                "{{ ti.xcom_pull(task_ids='router', key='message') }}"},
    )
    router >> [task_a, task_b, task_c, ml_workflow, task_trash]

    # empty_task_1 = EmptyOperator(task_id='empty_task_1')
    # empty_task_2 = EmptyOperator(task_id='empty_task_2')
    # cond >> [empty_task_1, empty_task_2]
