FROM apache/airflow:2.3.3
COPY requirements.txt /tmp/
COPY xcom_s3_backend.py /opt/airflow/config/
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir --requirement /tmp/requirements.txt && \
    pip install --no-cache-dir mlflow[extras] &&\
    pip install --no-cache-dir astro-sdk-python[amazon,google,snowflake,postgres] &&\
    pip install --no-cache-dir apache-airflow-providers-microsoft-mssql[common.sql] &&\
    # pip install --no-cache-dir torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cpu && \
    # pip install --no-cache-dir torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cu113