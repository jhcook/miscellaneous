#!/usr/bin/env bash
#
# Setup a single-node Kubernetes cluster with ingress, ingress-dns, and
# metrics-server with CNI plugin. Configure the pod network as 172.16.0.0/20.
# Use Kubernetes v1.21.7 as that is latest supported by Rancher. Finally, set
# resolver to forward .test DNS queries to this cluster.
#
# Author: Justin Cook

minikube --addons ingress,ingress-dns,metrics-server \
         --network-plugin=cni \
         --extra-config=kubeadm.pod-network-cidr=172.16.0.0/20 \
         --memory=6g \
         --kubernetes-version=v1.21.7 \
         --nodes=3 \
         -p calico \
         start

if [ ! -d "/etc/resolver" ]
then
  sudo mkdir /etc/resolver
fi

sudo bash -c "cat - > /etc/resolver/minikube-test <<EOF
domain test
nameserver $(minikube ip -p calico)
search_order 1
timeout 5
EOF
"