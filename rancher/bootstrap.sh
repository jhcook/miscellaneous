#!/usr/bin/env sh
#
# Create an instance of Kubernetes and deploy Rancher.
#
# Author: Justin Cook <jhcook@secnix.com>

set -o errexit
set -o xtrace

check_requirements() {
  # Check if requirements exist
  REQUIREMENTS="minikube helm kubectl"

  for exe in $REQUIREMENTS
  do
    which "$exe" >/dev/null 2>&1 || { \
    echo "Not found in PATH: $exe" ; exit 1; }
  done
}

start_minikube() {
  # Create an instance of Minikube
  minikube start \
    -p rancher \
    --cpus=4 \
    --memory=16g \
    --addons registry,ingress,ingress-dns \
    --insecure-registry "10.0.0.0/8" \
    --kubernetes-version 1.21.1
}

add_helm_repos() {
  # Add Helm repos
  helm repo add rancher-latest \
    https://releases.rancher.com/server-charts/latest
  helm repo add jetstack https://charts.jetstack.io
  helm repo update
}

install_cert_manager() {
  # Install cert-manager
  helm install cert-manager jetstack/cert-manager \
    --namespace cert-manager \
    --create-namespace \
    --set installCRDs=true \
    --version v1.5.1

  for dep in $(kubectl get deploy --namespace cert-manager -o name)
  do
    kubectl -n cert-manager rollout status "$dep"
  done
}

install_rancher() {
  # Install Rancher
  kubectl create namespace cattle-system
  helm install rancher rancher-latest/rancher \
    --namespace cattle-system \
    --set hostname=rancher.k8s.test \
    --set bootstrapPassword=admin
  kubectl -n cattle-system rollout status deploy/rancher
}

check_requirements
minikube -p rancher status >/dev/null 2>&1 || start_minikube
add_helm_repos
install_cert_manager
install_rancher