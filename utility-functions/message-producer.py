import json
from datetime import datetime
from random import randint, choice
from time import sleep

import pika
credentials = pika.PlainCredentials('user', 'MbtnNcY7DXPMX0je')
connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
channel = connection.channel()
channel.queue_declare(queue='external_airflow_triggers', durable=True)

tasks = ['hello_world_a', 'hello_world_b', 'hello_world_c']

while True:
    print('Producing messages at {}'.format(datetime.utcnow()))
    task_to_trigger = choice(tasks)
    event_time = str(datetime.utcnow())

    message = json.dumps(
        {'task': task_to_trigger, 'params': {'event_time': event_time, 'value': randint(0, 10000)}}
    )
    channel.basic_publish(exchange='', routing_key='external_airflow_triggers',
                          body=message)
    print(" [x] Sent {}".format(message))
    sleep(2)

connection.close()