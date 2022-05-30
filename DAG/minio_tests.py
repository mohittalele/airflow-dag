from minio import Minio
import os

client = Minio(
    "localhost:9000",
    access_key="ruxiu105QkeBjUXVOq4j",
    secret_key="UfvrsBtgZpwOqwiht239C5c3lJM4vWnLQcdMCuB8",
    secure=False,
)

client.list_buckets()
for obj in client.list_objects('dag-input'):
    print(obj)

txt = "dag-input/airflow-dag/validation-data/yoda.jpg"

client.fget_object(
    "dag-input", txt.partition("dag-input/")[2], "outputs/copied_" + os.path.basename(txt)
)

client.fput_object(
    "dag-input", "vyper_dev/20220530-115911/copied_" + os.path.basename(txt),
                 "outputs/copied_" + os.path.basename(txt)
)

# with client.listen_bucket_notification(
#         "dag-input",
#         prefix="*",
#         events=["s3:ObjectCreated:*", "s3:ObjectRemoved:*"],
# ) as events:
#     for event in events:
#         print(event)
