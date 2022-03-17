# calico

## Demonstration of Calico CNI with eBPF 

Create a Minikube cluster enabling ingress and ingress-dns addon, set the
cidr range to 172.16.0.0/20, and set the Kubernetes version.
* https://www.suse.com/suse-rancher/support-matrix/all-supported-versions/rancher-v2-6-3/
* https://minikube.sigs.k8s.io/docs/drivers/hyperkit/

### Configure .test TLD to to use Minikube
* https://minikube.sigs.k8s.io/docs/handbook/addons/ingress-dns/

```
sh setup_k8s.sh
```

## Install Calico CNI
* https://projectcalico.docs.tigera.io/getting-started/kubernetes/minikube

```
sh install_calico.sh
```

## Add Nodes to Minikube

```
minikube config set memory 4096 -p calico
minkube node add --worker -p calico
```

## Install Rancher
* https://rancher.com/docs/rancher/v2.6/en/installation/install-rancher-on-k8s/

```
sh install_rancher.sh
```

## Install / Configure Prometheus and Grafana 
* https://rancher.com/docs/rancher/v2.6/en/monitoring-alerting/guides/customize-grafana/
* https://www.tigera.io/blog/monitoring-calico-with-prometheus-and-grafana/
* https://www.tigera.io/blog/how-to-monitor-calicos-ebpf-data-plane-for-proactive-cluster-management/
* https://projectcalico.docs.tigera.io/maintenance/monitor/monitor-component-metrics

...


## Load Testing with Locust
* https://github.com/joakimhew/locust-kubernetes
* https://faun.pub/kubernetes-distributed-performance-testing-using-locust-871b46ba5c9c


## Enable eBPF
* https://projectcalico.docs.tigera.io/maintenance/ebpf/enabling-bpf
