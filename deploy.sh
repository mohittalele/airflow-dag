#!/bin/bash

kubectl create ns airflow
helmfile template > template.yaml
kubectl apply -n airflow -f template.yaml