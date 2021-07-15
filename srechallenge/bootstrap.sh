#!/usr/bin/env bash
# A simple utility to install cpx-server in Kubernetes.
#
# Requires: Python3 kubectl Docker Minikube
# 
# Tested on: macOS Big Sur 11.4
#
# Author: Justin Cook <jhcook@secnix.com>

set -o nounset
set -o errexit

# Run unit tests
python3 -m unittest discover -s .

echo "Starting Minikube..."
minikube start --addons registry,ingress --insecure-registry "localhost"

eval $(minikube docker-env)
echo "Building cpx_server Docker image..."
cd src
docker build --tag localhost:5000/cpx_server .
docker push localhost:5000/cpx_server
cd $OLDPWD

# Deploy to Kubernetes
sed -e "s/__DRHOST__/localhost:5000/g" src/cpx-server-deployment.yaml > \
  cpx-server.yaml
cat src/cpx-server-service.yaml >> cpx-server.yaml
cat src/cpx-server-ingress.yaml >> cpx-server.yaml
echo "Deploying cps-server components"
kubectl apply -f cpx-server.yaml
