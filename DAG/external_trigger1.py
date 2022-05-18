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
        kwargs['ti'].xcom_push(key='job_params', value=json.dumps(json_params['params']))
        channel.basic_ack(delivery_tag=method_frame.delivery_tag)
        connection.close()
        print("Got message ? {}".format(body))
        return json_params['task']
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
    # empty_task_1 = EmptyOperator(task_id='empty_task_1')
    # empty_task_2 = EmptyOperator(task_id='empty_task_2')
    # cond >> [empty_task_1, empty_task_2]
    router >> task_trash