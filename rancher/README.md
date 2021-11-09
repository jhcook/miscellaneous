# Rancher Projects

## Introduction



## Usage

### Minikube

Create a profile for Minikube, and assign four virtual CPU and 16Gi of memory.

```


```

Next, create an instance of Minikube with the registry, ingress, and ingress-dns
add on with a supported version of Kubernetes.

```
$ minikube start --addons registry,ingress,ingress-dns --insecure-registry "10.0.0.0/8" --kubernetes-version 1.21.1
```

### EKS Distro

...

### Install Rancher

Follow the documementation for the specific Rancher release. At the time of
this writing, that is [2.6](https://rancher.com/docs/rancher/v2.6/en/installation/install-rancher-on-k8s/). 
