FROM apache/airflow:2.2.4
RUN pip install hydra-core --upgrade
RUN pip install pika
CMD python /app/app.py