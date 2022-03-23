# calico

## Up and Running

The following instructions have been wrapped and provided in `quickstart.sh`.
It was developed and tested on macOS using hyperkit. It requires Internet
connectivity, and requires just under eight minutes to complete on a 500Mbps
connection. Hyperkit uses 30GiB of RAM for the default configuration.

The code requires the following utilities to operate correctly. They are
available with `brew`.

* Minikube
* kubectl
* Helm
* Git
* Pip
* Virtualenv

```
sh quickstart.sh
...
Open browser to: http://10.109.73.206:30875

[2022-03-23 16:54:04,461] jcmmini1.local/INFO/locust.main: Starting web interface at http://0.0.0.0:8089 (accepting connections from all network interfaces)
[2022-03-23 16:54:04,475] jcmmini1.local/INFO/locust.main: Starting Locust 2.8.4
```

## Demonstration of Calico CNI with eBPF the hard way 

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
minikube node add --worker -p calico
```
## Install Rancher
* https://rancher.com/docs/rancher/v2.6/en/installation/install-rancher-on-k8s/

```
sh install_rancher.sh
```

## Install / Configure Prometheus and Grafana 
* https://rancher.com/docs/rancher/v2.6/en/monitoring-alerting/guides/customize-grafana/
* https://rancher.com/docs/rancher/v2.6/en/monitoring-alerting/guides/persist-grafana/
* https://www.tigera.io/blog/monitoring-calico-with-prometheus-and-grafana/
* https://www.tigera.io/blog/how-to-monitor-calicos-ebpf-data-plane-for-proactive-cluster-management/
* https://projectcalico.docs.tigera.io/maintenance/monitor/monitor-component-metrics

```
sh install_monitoring.sh
```

Add the services necessary and create the Prometheus service monitors for
Calico.

```
sh monitoring/configure_prometheus.sh
...
kubectl apply -f monitoring/calico-grafana-dashboards.yaml
```

## Load Testing with Locust
* https://cloud.google.com/service-mesh/docs/onlineboutique-install-kpt
* https://github.com/GoogleCloudPlatform/microservices-demo

Create a virtual environment and install Locust. Then, clone the above repo,
install the application, setup Locust, and execute the load test.

```
sh install_boutique.sh
...
```

Open your browser and load the sites (Boutique and Locust) displayed.

## Enable eBPF
* https://projectcalico.docs.tigera.io/maintenance/ebpf/enabling-bpf

```
sh ebpf/enable_ebpf.sh
```

## Disable eBPF

```
sh ebpf/disable_ebpf.sh
```