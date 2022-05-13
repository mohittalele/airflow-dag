# airflow-dag

# Running minikube cluster requires below setting 

1) Download the minikube installer from the github site https://github.com/kubernetes/minikube/releases/tag/v1.25.2
2) Close and disconnect the VPN 
3) Make sure that HTTP_PROXY and HTTPS_PROXY and NO_PROXY environment variables are not set.
4) Open CMD as admin and run minikube start 
5) You can start VPN after the minikube deployment and all the pods have deployed and images are pulled. 

# minikube VPN setting - Not successful 
set HTTP_PROXY=<proxy URL>
set HTTPS_PROXY=<proxy URL>
set NO_PROXY=localhost,127.0.0.1,10.96.0.0/12,192.168.59.0/24,192.168.39.0/24


# Problems Encountered
- If the VPN is suddently get disconneted then the airflow git sync container starts throwing host github.com not found. In this case restart your VPN. That should solve issue. On the other hand this issue will not reoccur not starting your VPN while using airflow on Minikube  