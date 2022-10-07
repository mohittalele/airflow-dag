# airflow-dag

# Running minikube cluster requires below setting 

1) Download the minikube installer from the github site https://github.com/kubernetes/minikube/releases/tag/v1.25.2
2) Close and disconnect the VPN 
3) Make sure that HTTP_PROXY and HTTPS_PROXY and NO_PROXY environment variables are not set.
4) Open CMD as admin and run minikube start 

# Starting Minikube 
- If you are connected using Client Mobile 
  - Stop the VPN
  - ``` minikube start``` 
  - ``` k9s``` 
  - Start VPN 
  
# Deploy helm charts
``` helmfile apply ``` 

# minikube VPN setting - Not successful 
set HTTP_PROXY=<proxy URL>
set HTTPS_PROXY=<proxy URL>
set NO_PROXY=localhost,127.0.0.1,10.96.0.0/12,192.168.59.0/24,192.168.39.0/24

# Mount local file folder on to Minikube 
while testing you might want to mount the local folders to the minikube pods. To mount the local folder run this command :
``` minikube mount ${HOME}:/host ``` This will mount the home folder to path ```/host ```
# Problems Encountered
- If the VPN is suddently get disconneted then the airflow git sync container starts throwing host github.com not found. In this case restart your VPN. That should solve issue. On the other hand this issue will not reoccur not starting your VPN while using airflow on Minikube
- Airflow dont have Pika package. So we need to either manually install the package in the airflow-components or build a custom image with all packages that DAGs require




# Advanced Templating


```
from airflow.models import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime

filelist = [f'file{x}.txt' for x in range(30)]

default_args = {
  'start_date': datetime(2020, 4, 15),
}

cleandata_dag = DAG('cleandata',
                    default_args=default_args,
                    schedule_interval='@daily')


templated_command = """
  <% for filename in params.filenames %>
  bash cleandata.sh {{ ds_nodash }} {{ filename }};
  <% endfor %>
"""

clean_task = BashOperator(task_id='cleandata_task',
                          bash_command=templated_command,
                          params={'filenames': filelist},
                          dag=cleandata_dag)
```

# Building docer images 

```docker build -t airflow:2.2.4v1 . ``` 

``` docker tag airflow:2.2.4v1  mohittalele/airflow:2.2.4v1 ```

``` docker push mohittalele/airflow:2.2.4v1  ```
