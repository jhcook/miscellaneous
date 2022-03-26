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
helm upgrade --install keda kedacore/keda --namespace keda

# Wait for all the deployments to become available
for deploy in $(kubectl get deploy -n keda -o name)
do
  kubectl rollout status "${deploy}" -n keda
done

# Create an Ingress for the Boutique®
kubectl apply -f hpa/frontend-ingress.yaml

# Create the ScaledObject(s)
PROMHOST=$(kubectl get svc rancher-monitoring-prometheus -n \
           cattle-monitoring-system -o jsonpath='{.spec.clusterIP}')

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
      serverAddress: http://${PROMHOST}:9090
      metricName: nginx_ingress_controller_requests
      query: |
        sum(rate(nginx_ingress_controller_requests[30s]))
      threshold: "30"
EOF

kubectl apply -f - <<EOF
apiVersion: keda.sh/v1alpha1
kind: ScaledObject
metadata:
  name: cartservice-scale
  namespace: default
spec:
  scaleTargetRef:
    kind: Deployment
    name: cartservice
  minReplicaCount: 1
  maxReplicaCount: 20
  cooldownPeriod: 30
  pollingInterval: 1
  triggers:
  - type: prometheus
    metadata:
      serverAddress: http://${PROMHOST}:9090
      metricName: nginx_ingress_controller_requests
      query: |
        sum(rate(nginx_ingress_controller_requests[30s]))
      threshold: "30"
EOF