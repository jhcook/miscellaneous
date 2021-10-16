#!/usr/bin/env bash
# A simple utility to install cpx-server in Kubernetes.
#
# Requires: Python3 kubectl Docker Minikube
# 
# Tested on: macOS Big Sur 11
#
# Author: Justin Cook <jhcook@secnix.com>

set -o nounset
set -o errexit

# Check dependencies in PATH
for cmd in docker kubectl python3 minikube
  do which ${cmd} 2>&1 >/dev/null || { 
    echo "command not found in PATH: ${cmd}" ; exit 1 ; }
done

# Run unit tests
python3 -m unittest discover -s .

# Create Minikube VM
echo "Starting Minikube..."
minikube start --addons registry,ingress --insecure-registry "localhost"

# Build Docker image and push to local registry
eval $(minikube docker-env)
echo "Building cpx_server Docker image..."
cd src
# https://stackoverflow.com/questions/37573476/
# docker-complaining-about-all-proxy-environment-variable-with-proxy-unknown-sch
unset ALL_PROXY
docker build --tag localhost:5000/cpx_server .
docker push localhost:5000/cpx_server
cd $OLDPWD

# Deploy to Kubernetes
if [ ! -d "tmp" ]
then
  mkdir tmp
fi
sed -e "s/__DRHOST__/localhost:5000/g" src/cpx-server-deployment.yaml > \
  tmp/cpx-server.yaml
cat src/cpx-server-service.yaml >> tmp/cpx-server.yaml
cat src/cpx-server-ingress.yaml >> tmp/cpx-server.yaml
echo "Deploying cps-server components"
kubectl apply -f tmp/cpx-server.yaml