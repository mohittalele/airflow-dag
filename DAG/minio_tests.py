from minio import Minio

client = Minio(
    "localhost:9000",
    access_key="ruxiu105QkeBjUXVOq4j",
    secret_key="UfvrsBtgZpwOqwiht239C5c3lJM4vWnLQcdMCuB8",
    secure=False,
)

client.list_buckets()
for obj in client.list_objects('dag-input'):
    print(obj)

with client.listen_bucket_notification(
        "dag-input",
        prefix="*",
        events=["s3:ObjectCreated:*", "s3:ObjectRemoved:*"],
) as events:
    for event in events:
        print(event)
