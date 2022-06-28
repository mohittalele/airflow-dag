FROM apache/airflow:2.2.4
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir --requirement /tmp/requirements.txt && \
    pip install --no-cache-dir torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cpu && \
    pip install --no-cache-dir torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cu113