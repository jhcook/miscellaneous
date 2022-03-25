#!/usr/bin/env bash
#
# Configure HPA using Keda 
#
# References:
# * https://www.nginx.com/blog/microservices-march-reduce-kubernetes-latency-with-autoscaling/
#
# Author: Justin Cook

# Add the Keda Helm chart repository
helm repo add kedacore https://kedacore.github.io/charts
helm repo update

# Create the keda namespace 
kubectl create namespace keda --dry-run=client -o yaml | \
  kubectl apply -f -

# Install Keda
helm install keda kedacore/keda --namespace keda

# Wait for all the deployments to become available
for deploy in $(kubectl get deploy -n keda -o name)
do
  kubectl rollout status "${deploy}" -n keda
done

# Create the ScaledObject
kubectl apply -f - <<EOF
apiVersion: keda.sh/v1alpha1
kind: ScaledObject
metadata:
  name: recommendationservice-scale
  namespace: default
spec:
  scaleTargetRef:
    kind: Deployment
    name: recommendationservice
minReplicaCount: 1
maxReplicaCount: 20
cooldownPeriod: 30
pollingInterval: 1
triggers:
- type: prometheus
  metadata:
    serverAddress: http://boutique.mars
    metricName: nginx_connections_active_keda
    query: |
      sum(avg_over_time(nginx_ingress_nginx_connections_active{app="ingress-nginx"}[1m]))
    threshold: "30"
EOF