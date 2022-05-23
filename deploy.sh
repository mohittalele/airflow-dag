#!/bin/bash

kubectl create ns airflow
helmfile template > template.yaml
kubectl apply -n airflow -f template.yaml
#helmfile -l app=message-producer template --skip-deps > template.yaml 
#helmfile -l app=ubuntu template --skip-deps | kubectl -n airflow apply -f-
#kubectl create configmap name-of-your-configmap --from-file=utility-functions/message-producer.py  --dry-run=client -o yaml > cm.yaml