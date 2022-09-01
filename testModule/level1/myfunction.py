import sys
import json


def print_context():
    """Print the Airflow context and ds variable from the context."""
    print("I am in new  context")
    print(sys.path)
    return 'Whatever you return gets printed in the logs'


# [START extract_function]
def extract(**kwargs):
    ti = kwargs['ti']
    data_string = '{"1001": 301.27, "1002": 433.21, "1003": 502.22}'
    ti.xcom_push('order_data', data_string)


# [END extract_function]

# [START transform_function]
def transform(**kwargs):
    data = kwargs['ti']
    extract_data_string = data.xcom_pull(task_ids='extract', key='order_data')
    order_data = json.loads(extract_data_string)

    total_order_value = 0
    for value in order_data.values():
        total_order_value += value

    total_value = {"total_order_value": total_order_value}
    total_value_json_string = json.dumps(total_value)
    data.xcom_push('total_order_value', total_value_json_string)


# [END transform_function]

# [START load_function]
def load(**kwargs):
    data = kwargs['ti']
    total_value_string = data.xcom_pull(task_ids='transform', key='total_order_value')
    total_order_value = json.loads(total_value_string)

    print(total_order_value)
