#!/bin/bash

kubectl create ns airflow
helmfile template > template.yaml
kubectl apply -n airflow -f template.yaml

#kubectl create configmap name-of-your-configmap --from-file=utility-functions/message-producer.py  --dry-run=client -o yaml > cm.yaml