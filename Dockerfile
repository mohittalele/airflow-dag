FROM apache/airflow:2.3.3
COPY requirements.txt /tmp/
COPY xcom_s3_backend.py /opt/airflow/config/
RUN sudo pip install --no-cache-dir --upgrade pip && \
    sudo pip install --no-cache-dir --requirement /tmp/requirements.txt && \
    sudo pip install --no-cache-dir mlflow[extras] &&\
    sudo pip install --no-cache-dir astro-sdk-python[amazon,google,snowflake,postgres] &&\
    sudo pip install --no-cache-dir torch==1.10.0+cpu torchvision==0.11.0+cpu torchaudio==0.10.0 -f https://download.pytorch.org/whl/torch_stable.html
