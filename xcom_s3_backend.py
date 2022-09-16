import os
import uuid
import pandas as pd

from typing import Any
from airflow.models.xcom import BaseXCom
from airflow.providers.amazon.aws.hooks.s3 import S3Hook
from typing import Optional


class S3XComBackend(BaseXCom):
    PREFIX = "s3"
    BUCKET_NAME = os.environ.get("S3_XCOM_BUCKET_NAME")
    CONN_ID = os.environ.get("S3_XCOM_CONN_ID")

    @staticmethod
    def _assert_s3_backend():
        if S3XComBackend.BUCKET_NAME is None:
            raise ValueError("Unknown bucket for S3 backend.")

    @staticmethod
    def serialize_value(value: Any):
        if isinstance(value, pd.DataFrame):
            S3XComBackend._assert_s3_backend()
            hook = S3Hook(aws_conn_id=S3XComBackend.CONN_ID)
            key = f"data_{str(uuid.uuid4())}.csv"
            filename = f"{key}.csv"
            value.to_csv(filename, index=False)
            hook.load_file(
                filename=filename,
                key=key,
                bucket_name=S3XComBackend.BUCKET_NAME,
                replace=True
            )
            value = f"{S3XComBackend.PREFIX}://{S3XComBackend.BUCKET_NAME}/{key}"

        elif isinstance(value, dict) and all(isinstance(x, pd.DataFrame) for x in value.values()):
            S3XComBackend._assert_s3_backend()
            hook = S3Hook(aws_conn_id=S3XComBackend.CONN_ID)
            stripped_dict = {}
            for df_key, df_value in value.items():
                key = f"data_{str(uuid.uuid4())}.csv"
                filename = f"{key}.csv"
                df_value.to_csv(filename, index=False)
                hook.load_file(
                    filename=filename,
                    key=key,
                    bucket_name=S3XComBackend.BUCKET_NAME,
                    replace=True
                )
                stripped_dict[df_key] = f"{S3XComBackend.PREFIX}://{S3XComBackend.BUCKET_NAME}/{key}"
            value = stripped_dict

        return BaseXCom.serialize_value(value)

    @staticmethod
    def deserialize_value(result) -> Any:
        result = BaseXCom.deserialize_value(result)

        if isinstance(result, str) and result.startswith(S3XComBackend.PREFIX):
            S3XComBackend._assert_s3_backend()
            hook = S3Hook(aws_conn_id=S3XComBackend.CONN_ID)
            key = result.replace(f"{S3XComBackend.PREFIX}://{S3XComBackend.BUCKET_NAME}/", "")
            filename = hook.download_file(
                key=key,
                bucket_name=S3XComBackend.BUCKET_NAME,
                local_path="/tmp"
            )
            result = pd.read_csv(filename)
        elif isinstance(result, dict) and all(x.startswith(S3XComBackend.PREFIX) for x in result.values()):
            S3XComBackend._assert_s3_backend()
            hook = S3Hook(aws_conn_id=S3XComBackend.CONN_ID)
            loaded_dict = {}
            for df_key, df_value in result.items():
                key = df_value.replace(f"{S3XComBackend.PREFIX}://{S3XComBackend.BUCKET_NAME}/", "")
                filename = hook.download_file(
                    key=key,
                    bucket_name=S3XComBackend.BUCKET_NAME,
                    local_path="/tmp"
                )
                loaded_dict[df_key] = pd.read_csv(filename)
            result = loaded_dict
        return result


class S3XComBackendPickling(BaseXCom):
    PREFIX = "s3"
    BUCKET_NAME = os.environ.get("S3_XCOM_BUCKET_NAME")
    CONN_ID = os.environ.get("S3_XCOM_CONN_ID")

    @staticmethod
    def _assert_s3_backend():
        if S3XComBackendPickling.BUCKET_NAME is None:
            raise ValueError("Unknown bucket for S3 backend.")

    @staticmethod
    def serialize_value(value: Any,
                        key: Optional[str] = None,
                        task_id: Optional[str] = None,
                        dag_id: Optional[str] = None,
                        run_id: Optional[str] = None,
                        map_index: Optional[int] = None):
        if isinstance(value, pd.DataFrame):
            S3XComBackendPickling._assert_s3_backend()
            hook = S3Hook(aws_conn_id=S3XComBackendPickling.CONN_ID)
            s3key = f"data_{str(uuid.uuid4())}.pickle"
            filename = f"{s3key}.pickle"
            value.to_pickle(filename)
            hook.load_file(
                filename=filename,
                key=s3key,
                bucket_name=S3XComBackendPickling.BUCKET_NAME,
                replace=True
            )
            value = f"{S3XComBackendPickling.PREFIX}://{S3XComBackendPickling.BUCKET_NAME}/{s3key}"

        elif isinstance(value, dict) and all(isinstance(x, pd.DataFrame) for x in value.values()):
            S3XComBackendPickling._assert_s3_backend()
            hook = S3Hook(aws_conn_id=S3XComBackendPickling.CONN_ID)
            stripped_dict = {}
            for df_key, df_value in value.items():
                s3key = f"data_{str(uuid.uuid4())}.csv"
                filename = f"{s3key}.csv"
                df_value.to_pickle(filename)
                hook.load_file(
                    filename=filename,
                    key=s3key,
                    bucket_name=S3XComBackendPickling.BUCKET_NAME,
                    replace=True
                )
                stripped_dict[df_key] = f"{S3XComBackendPickling.PREFIX}://{S3XComBackendPickling.BUCKET_NAME}/{s3key}"
            value = stripped_dict

        return BaseXCom.serialize_value(value)

    @staticmethod
    def deserialize_value(result) -> Any:
        result = BaseXCom.deserialize_value(result)

        if isinstance(result, str) and result.startswith(S3XComBackendPickling.PREFIX):
            S3XComBackendPickling._assert_s3_backend()
            hook = S3Hook(aws_conn_id=S3XComBackendPickling.CONN_ID)
            s3key = result.replace(f"{S3XComBackendPickling.PREFIX}://{S3XComBackendPickling.BUCKET_NAME}/", "")
            filename = hook.download_file(
                key=s3key,
                bucket_name=S3XComBackendPickling.BUCKET_NAME,
                local_path="/tmp"
            )
            result = pd.read_pickle(filename)
        elif isinstance(result, dict) and all(x.startswith(S3XComBackendPickling.PREFIX) for x in result.values()):
            S3XComBackendPickling._assert_s3_backend()
            hook = S3Hook(aws_conn_id=S3XComBackendPickling.CONN_ID)
            loaded_dict = {}
            for df_key, df_value in result.items():
                s3key = df_value.replace(f"{S3XComBackendPickling.PREFIX}://{S3XComBackendPickling.BUCKET_NAME}/", "")
                filename = hook.download_file(
                    key=s3key,
                    bucket_name=S3XComBackendPickling.BUCKET_NAME,
                    local_path="/tmp"
                )
                loaded_dict[df_key] = pd.read_pickle(filename)
            result = loaded_dict
        return result
