#!/usr/bin/env bash
#
# Install Prometheus, Grafana, and configure the monitoring stack
#
# Author: Justin Cook

set -o errexit

# Add the applicable Helm chards to the repo and update
helm repo add rancher-monitoring-crd http://charts.rancher.io
helm repo add rancher-monitoring http://charts.rancher.io
helm repo update

# Create the cattle-monitoring-system namespace 
kubectl create namespace cattle-monitoring-system --dry-run=client -o yaml | \
  kubectl apply -f -

# Install the required charts for rancher-monitoring
helm upgrade --install=true --namespace=cattle-monitoring-system --timeout=10m0s --values=monitoring/values.yaml --version=100.1.0+up19.0.3 --wait=true rancher-monitoring-crd http://charts.rancher.io/assets/rancher-monitoring-crd/rancher-monitoring-crd-100.1.0+up19.0.3.tgz
helm upgrade --install=true --namespace=cattle-monitoring-system --timeout=10m0s --values=monitoring/values.yaml --version=100.1.0+up19.0.3 --wait=true rancher-monitoring http://charts.rancher.io/assets/rancher-monitoring/rancher-monitoring-100.1.0+up19.0.3.tgz

# Wait for all the deployments to become available
for deploy in $(kubectl get deploy -n cattle-monitoring-system -o name)
do
  kubectl rollout status "${deploy}" -n cattle-monitoring-system
done