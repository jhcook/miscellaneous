#!/usr/bin/env sh
#
# Install the Tigera Calico operator and deploy Calico CNI
# Watch pods until calico-kube-controllers is deployed
#
# Requires: kubectl
#
# Author: Justin Cook

set -o errexit

# Install Tigera operator
kubectl apply -f https://docs.projectcalico.org/archive/v3.19/manifests/tigera-operator.yaml

# Wait on the operator to run
kubectl rollout status deploy/tigera-operator -n tigera-operator

# Install Calico using Installation kind
cat <<EOF | kubectl apply -f -
apiVersion: operator.tigera.io/v1
kind: Installation
metadata:
  name: default
spec:
  calicoNetwork:
    containerIPForwarding: Enabled
    ipPools:
    - cidr: 172.16.0.0/20
      natOutgoing: Enabled
      encapsulation: None
  typhaMetricsPort: 9093
EOF

# Wait until the Installation is progressing
while :
do
  kubectl get tigerastatus/calico 2>/dev/null && break
  sleep 1
done

# Display pods until calico-kube-controllers rolls out
kubectl get pods -A -w &
watch_pid="$!"

# Wait on calico-kube-controllers deployment
kubectl rollout status deploy/calico-kube-controllers -n calico-system

kill -15 ${watch_pid}
wait ${watch_pid}
