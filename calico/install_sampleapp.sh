#!/usr/bin/env sh

# Install the app
kubectl apply -f https://raw.githubusercontent.com/tigera/ccol1/main/yaobank.yaml

# Wait on the customer microservice
kubectl rollout status -n yaobank deployment/customer

# Wait on the summary microservice
kubectl rollout status -n yaobank deployment/summary

# Wait on the database microservice
kubectl rollout status -n yaobank deployment/database

# Test the app
while :
do
  curl 198.19.0.1:30180 2>/dev/null && break
  sleep 1
done

