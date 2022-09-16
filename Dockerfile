FROM apache/airflow:2.3.3
COPY requirements.txt /tmp/
COPY xcom_s3_backend.py /opt/airflow/config/
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir --requirement /tmp/requirements.txt && \
    pip install --no-cache-dir mlflow[extras] &&\
    pip install --no-cache-dir astro-sdk-python[amazon,google,snowflake,postgres] &&\
    pip install --no-cache-dir torch==1.11.0+cpu torchvision==0.12.0+cpu torchaudio==0.11.0 --extra-index-url https://download.pytorch.org/whl/cpu && \
    pip install --no-cache-dir torch==1.11.0+cu113 torchvision==0.12.0+cu113 torchaudio==0.11.0 --extra-index-url https://download.pytorch.org/whl/cu113