# Introduction

Here we have a life-saving utility that queries Cloud Provider X for a list of
servers, the associated services, resource consumption, and each's health.

In order to get started, the following will need to be installed on your 
workstation. Those procedures are dependant on your platform and are out of
scope for this documentation.

The following have been tested on macOS using `brew` installation. 

1\. Install Prerequisites
- Python3
- kubectl
- Docker
- Minikube

The enclosed `bootstrap.sh` script encloses all the following steps. 

## Development

### Minikube
You will need to add the local registry if you prefer to use local assets.
You will need to allow insecure registries, and this is easiest allowing your
entire local network. Enable the NGINX Ingress controller.

```
$ minikube start --addons registry,ingress --insecure-registry "10.0.0.0/8"
```

### Building Images

Build cpx_server Image

```
$ eval $(minikube docker-env)
$ docker build --tag $(minikube ip):5000/cpx_server .
...
$ docker tag $(minikube ip):5000/cpx_server localhost:5000/cpx_server
$ docker push localhost:5000/cpx_server
...
```

### Deploy API Server

You must first edit the `__DRHOST__` placeholder in
`cpx-server-deployment.yaml` with the Docker registry host information. After,
you can apply the yaml file accordingly followed by the service and ingress
manifests.

```
$ kubectl apply -f cpx-server-deployment.yaml
...
$ kubectl apply -f cpx-server-service.yaml
...
$ kubectl apply -f cpx-server-ingress.yaml
...
```

### Tests

This code makes use of unittest to seed a list of servers and a service for
further use by a local `cpx_server.py` process providing the API. This API
instance is further used to querie the list of preseeded servers. 

In the top level directory you my run a unittest discover like the following:

```
$ python3 -m unittest discover -s .
IP              Service             CPU Memory
----------------------------------------------
::1 - - [14/Jul/2021 10:44:32] "GET /10.58.1.59 HTTP/1.1" 200 -
10.58.1.59      GeoService           61%    4%
::1 - - [14/Jul/2021 10:44:32] "GET /10.58.1.3 HTTP/1.1" 200 -
10.58.1.3       MLService            88%   86%
::1 - - [14/Jul/2021 10:44:32] "GET /10.58.1.16 HTTP/1.1" 200 -
10.58.1.16      IdService            32%   88%
::1 - - [14/Jul/2021 10:44:32] "GET /10.58.1.80 HTTP/1.1" 200 -
10.58.1.80      RoleService          32%   53%
::1 - - [14/Jul/2021 10:44:32] "GET /10.58.1.62 HTTP/1.1" 200 -
10.58.1.62      IdService            15%   20%
::1 - - [14/Jul/2021 10:44:32] "GET /10.58.1.135 HTTP/1.1" 200 -
10.58.1.135     TicketService        93%    3%
::1 - - [14/Jul/2021 10:44:32] "GET /10.58.1.85 HTTP/1.1" 200 -
10.58.1.85      TimeService          72%   37%
::1 - - [14/Jul/2021 10:44:32] "GET /10.58.1.128 HTTP/1.1" 200 -
10.58.1.128     PermissionsService   48%   95%
::1 - - [14/Jul/2021 10:44:32] "GET /10.58.1.5 HTTP/1.1" 200 -
10.58.1.5       StorageService       59%   10%
::1 - - [14/Jul/2021 10:44:32] "GET /10.58.1.72 HTTP/1.1" 200 -
10.58.1.72      RoleService          47%   43%
::1 - - [14/Jul/2021 10:44:32] "GET /10.58.1.61 HTTP/1.1" 200 -
10.58.1.61      AuthService          55%   58%
::1 - - [14/Jul/2021 10:44:32] "GET /10.58.1.74 HTTP/1.1" 200 -
10.58.1.74      TicketService        62%   38%
::1 - - [14/Jul/2021 10:44:32] "GET /10.58.1.120 HTTP/1.1" 200 -
10.58.1.120     IdService             1%   87%
::1 - - [14/Jul/2021 10:44:32] "GET /10.58.1.96 HTTP/1.1" 200 -
10.58.1.96      IdService            61%   55%
::1 - - [14/Jul/2021 10:44:32] "GET /10.58.1.2 HTTP/1.1" 200 -
10.58.1.2       TimeService          27%   20%
::1 - - [14/Jul/2021 10:44:32] "GET /10.58.1.119 HTTP/1.1" 200 -
10.58.1.119     GeoService            0%   61%
::1 - - [14/Jul/2021 10:44:32] "GET /10.58.1.32 HTTP/1.1" 200 -
10.58.1.32      TimeService          20%   45%
::1 - - [14/Jul/2021 10:44:32] "GET /10.58.1.123 HTTP/1.1" 200 -
10.58.1.123     IdService            71%   23%
::1 - - [14/Jul/2021 10:44:32] "GET /10.58.1.94 HTTP/1.1" 200 -
10.58.1.94      GeoService           34%   78%
::1 - - [14/Jul/2021 10:44:32] "GET /10.58.1.41 HTTP/1.1" 200 -
10.58.1.41      RoleService          47%   28%
::1 - - [14/Jul/2021 10:44:32] "GET /10.58.1.113 HTTP/1.1" 200 -
10.58.1.113     TicketService        92%   20%
::1 - - [14/Jul/2021 10:44:32] "GET /10.58.1.21 HTTP/1.1" 200 -
10.58.1.21      RoleService          26%   29%
::1 - - [14/Jul/2021 10:44:32] "GET /10.58.1.28 HTTP/1.1" 200 -
10.58.1.28      AuthService           1%   84%
::1 - - [14/Jul/2021 10:44:32] "GET /10.58.1.67 HTTP/1.1" 200 -
10.58.1.67      GeoService           78%   60%
::1 - - [14/Jul/2021 10:44:32] "GET /10.58.1.137 HTTP/1.1" 200 -
10.58.1.137     StorageService       91%   44%
::1 - - [14/Jul/2021 10:44:32] "GET /10.58.1.44 HTTP/1.1" 200 -
10.58.1.44      GeoService           41%   50%
::1 - - [14/Jul/2021 10:44:32] "GET /10.58.1.34 HTTP/1.1" 200 -
10.58.1.34      RoleService          67%   92%
::1 - - [14/Jul/2021 10:44:32] "GET /10.58.1.53 HTTP/1.1" 200 -
10.58.1.53      StorageService       45%   53%
::1 - - [14/Jul/2021 10:44:32] "GET /10.58.1.109 HTTP/1.1" 200 -
10.58.1.109     AuthService          15%   51%
::1 - - [14/Jul/2021 10:44:32] "GET /10.58.1.26 HTTP/1.1" 200 -
10.58.1.26      GeoService           90%   70%
::1 - - [14/Jul/2021 10:44:32] "GET /10.58.1.149 HTTP/1.1" 200 -
10.58.1.149     UserService          63%   53%
::1 - - [14/Jul/2021 10:44:32] "GET /10.58.1.125 HTTP/1.1" 200 -
10.58.1.125     IdService            98%   26%
::1 - - [14/Jul/2021 10:44:32] "GET /10.58.1.82 HTTP/1.1" 200 -
10.58.1.82      StorageService       57%   82%
::1 - - [14/Jul/2021 10:44:32] "GET /10.58.1.48 HTTP/1.1" 200 -
10.58.1.48      RoleService          34%    0%
::1 - - [14/Jul/2021 10:44:32] "GET /10.58.1.15 HTTP/1.1" 200 -
10.58.1.15      StorageService       71%   79%
::1 - - [14/Jul/2021 10:44:32] "GET /10.58.1.43 HTTP/1.1" 200 -
10.58.1.43      StorageService       88%   95%
::1 - - [14/Jul/2021 10:44:32] "GET /10.58.1.39 HTTP/1.1" 200 -
10.58.1.39      StorageService       11%   37%
::1 - - [14/Jul/2021 10:44:32] "GET /10.58.1.102 HTTP/1.1" 200 -
10.58.1.102     RoleService          15%   83%
::1 - - [14/Jul/2021 10:44:32] "GET /10.58.1.131 HTTP/1.1" 200 -
10.58.1.131     UserService          94%   20%
::1 - - [14/Jul/2021 10:44:32] "GET /10.58.1.57 HTTP/1.1" 200 -
10.58.1.57      AuthService          88%    7%
::1 - - [14/Jul/2021 10:44:32] "GET /10.58.1.148 HTTP/1.1" 200 -
10.58.1.148     GeoService           38%   98%
::1 - - [14/Jul/2021 10:44:32] "GET /10.58.1.49 HTTP/1.1" 200 -
10.58.1.49      RoleService           1%   56%
::1 - - [14/Jul/2021 10:44:32] "GET /10.58.1.75 HTTP/1.1" 200 -
10.58.1.75      RoleService          44%   91%
::1 - - [14/Jul/2021 10:44:32] "GET /10.58.1.24 HTTP/1.1" 200 -
10.58.1.24      IdService            80%   15%
::1 - - [14/Jul/2021 10:44:32] "GET /10.58.1.55 HTTP/1.1" 200 -
10.58.1.55      MLService            47%   80%
::1 - - [14/Jul/2021 10:44:32] "GET /10.58.1.84 HTTP/1.1" 200 -
10.58.1.84      AuthService          86%   49%
::1 - - [14/Jul/2021 10:44:32] "GET /10.58.1.81 HTTP/1.1" 200 -
10.58.1.81      AuthService          49%   69%
::1 - - [14/Jul/2021 10:44:32] "GET /10.58.1.45 HTTP/1.1" 200 -
10.58.1.45      TimeService          81%   94%
::1 - - [14/Jul/2021 10:44:33] "GET /10.58.1.140 HTTP/1.1" 200 -
10.58.1.140     PermissionsService   68%   26%
::1 - - [14/Jul/2021 10:44:33] "GET /10.58.1.40 HTTP/1.1" 200 -
10.58.1.40      IdService            79%    4%
::1 - - [14/Jul/2021 10:44:33] "GET /10.58.1.47 HTTP/1.1" 200 -
10.58.1.47      PermissionsService   58%   22%
::1 - - [14/Jul/2021 10:44:33] "GET /10.58.1.70 HTTP/1.1" 200 -
10.58.1.70      UserService          51%   88%
::1 - - [14/Jul/2021 10:44:33] "GET /10.58.1.20 HTTP/1.1" 200 -
10.58.1.20      GeoService           30%   63%
::1 - - [14/Jul/2021 10:44:33] "GET /10.58.1.111 HTTP/1.1" 200 -
10.58.1.111     TicketService        27%   92%
::1 - - [14/Jul/2021 10:44:33] "GET /10.58.1.117 HTTP/1.1" 200 -
10.58.1.117     IdService            97%   28%
::1 - - [14/Jul/2021 10:44:33] "GET /10.58.1.93 HTTP/1.1" 200 -
10.58.1.93      MLService             4%   72%
::1 - - [14/Jul/2021 10:44:33] "GET /10.58.1.27 HTTP/1.1" 200 -
10.58.1.27      RoleService          65%   50%
::1 - - [14/Jul/2021 10:44:33] "GET /10.58.1.89 HTTP/1.1" 200 -
10.58.1.89      AuthService          85%   85%
::1 - - [14/Jul/2021 10:44:33] "GET /10.58.1.139 HTTP/1.1" 200 -
10.58.1.139     TimeService          30%   92%
::1 - - [14/Jul/2021 10:44:33] "GET /10.58.1.51 HTTP/1.1" 200 -
10.58.1.51      IdService            89%   27%
::1 - - [14/Jul/2021 10:44:33] "GET /10.58.1.13 HTTP/1.1" 200 -
10.58.1.13      TicketService        98%   32%
::1 - - [14/Jul/2021 10:44:33] "GET /10.58.1.90 HTTP/1.1" 200 -
10.58.1.90      RoleService          15%    1%
::1 - - [14/Jul/2021 10:44:33] "GET /10.58.1.36 HTTP/1.1" 200 -
10.58.1.36      PermissionsService   74%   31%
::1 - - [14/Jul/2021 10:44:33] "GET /10.58.1.98 HTTP/1.1" 200 -
10.58.1.98      UserService          39%   94%
::1 - - [14/Jul/2021 10:44:33] "GET /10.58.1.106 HTTP/1.1" 200 -
10.58.1.106     MLService            65%   39%
::1 - - [14/Jul/2021 10:44:33] "GET /10.58.1.143 HTTP/1.1" 200 -
10.58.1.143     UserService          47%   51%
::1 - - [14/Jul/2021 10:44:33] "GET /10.58.1.132 HTTP/1.1" 200 -
10.58.1.132     RoleService          18%   10%
::1 - - [14/Jul/2021 10:44:33] "GET /10.58.1.14 HTTP/1.1" 200 -
10.58.1.14      IdService            51%   77%
::1 - - [14/Jul/2021 10:44:33] "GET /10.58.1.42 HTTP/1.1" 200 -
10.58.1.42      MLService            37%   34%
::1 - - [14/Jul/2021 10:44:33] "GET /10.58.1.77 HTTP/1.1" 200 -
10.58.1.77      UserService          41%   28%
::1 - - [14/Jul/2021 10:44:33] "GET /10.58.1.110 HTTP/1.1" 200 -
10.58.1.110     TimeService          94%   22%
::1 - - [14/Jul/2021 10:44:33] "GET /10.58.1.35 HTTP/1.1" 200 -
10.58.1.35      AuthService          58%   10%
::1 - - [14/Jul/2021 10:44:33] "GET /10.58.1.60 HTTP/1.1" 200 -
10.58.1.60      TicketService        11%    7%
::1 - - [14/Jul/2021 10:44:33] "GET /10.58.1.100 HTTP/1.1" 200 -
10.58.1.100     RoleService          66%    1%
::1 - - [14/Jul/2021 10:44:33] "GET /10.58.1.22 HTTP/1.1" 200 -
10.58.1.22      RoleService          31%   71%
::1 - - [14/Jul/2021 10:44:33] "GET /10.58.1.126 HTTP/1.1" 200 -
10.58.1.126     GeoService           85%   89%
::1 - - [14/Jul/2021 10:44:33] "GET /10.58.1.71 HTTP/1.1" 200 -
10.58.1.71      IdService            10%   22%
::1 - - [14/Jul/2021 10:44:33] "GET /10.58.1.23 HTTP/1.1" 200 -
10.58.1.23      TimeService          72%   97%
::1 - - [14/Jul/2021 10:44:33] "GET /10.58.1.87 HTTP/1.1" 200 -
10.58.1.87      PermissionsService   69%   58%
::1 - - [14/Jul/2021 10:44:33] "GET /10.58.1.138 HTTP/1.1" 200 -
10.58.1.138     GeoService          100%   69%
::1 - - [14/Jul/2021 10:44:33] "GET /10.58.1.18 HTTP/1.1" 200 -
10.58.1.18      RoleService          90%    2%
::1 - - [14/Jul/2021 10:44:33] "GET /10.58.1.9 HTTP/1.1" 200 -
10.58.1.9       AuthService          16%   91%
::1 - - [14/Jul/2021 10:44:33] "GET /10.58.1.116 HTTP/1.1" 200 -
10.58.1.116     IdService            76%   56%
::1 - - [14/Jul/2021 10:44:33] "GET /10.58.1.141 HTTP/1.1" 200 -
10.58.1.141     UserService          52%    2%
::1 - - [14/Jul/2021 10:44:33] "GET /10.58.1.103 HTTP/1.1" 200 -
10.58.1.103     MLService            29%   71%
::1 - - [14/Jul/2021 10:44:33] "GET /10.58.1.19 HTTP/1.1" 200 -
10.58.1.19      MLService            48%   94%
::1 - - [14/Jul/2021 10:44:33] "GET /10.58.1.124 HTTP/1.1" 200 -
10.58.1.124     RoleService          63%   12%
::1 - - [14/Jul/2021 10:44:33] "GET /10.58.1.99 HTTP/1.1" 200 -
10.58.1.99      StorageService       89%    6%
::1 - - [14/Jul/2021 10:44:33] "GET /10.58.1.63 HTTP/1.1" 200 -
10.58.1.63      MLService            10%   64%
::1 - - [14/Jul/2021 10:44:33] "GET /10.58.1.38 HTTP/1.1" 200 -
10.58.1.38      TimeService          67%    3%
::1 - - [14/Jul/2021 10:44:33] "GET /10.58.1.95 HTTP/1.1" 200 -
10.58.1.95      AuthService          18%    1%
::1 - - [14/Jul/2021 10:44:33] "GET /10.58.1.104 HTTP/1.1" 200 -
10.58.1.104     TicketService        98%   22%
::1 - - [14/Jul/2021 10:44:33] "GET /10.58.1.142 HTTP/1.1" 200 -
10.58.1.142     IdService             1%   77%
::1 - - [14/Jul/2021 10:44:33] "GET /10.58.1.115 HTTP/1.1" 200 -
10.58.1.115     GeoService            7%   59%
::1 - - [14/Jul/2021 10:44:33] "GET /10.58.1.7 HTTP/1.1" 200 -
10.58.1.7       RoleService          50%   36%
::1 - - [14/Jul/2021 10:44:33] "GET /10.58.1.58 HTTP/1.1" 200 -
10.58.1.58      TimeService          15%   47%
::1 - - [14/Jul/2021 10:44:33] "GET /10.58.1.4 HTTP/1.1" 200 -
10.58.1.4       StorageService       62%   30%
::1 - - [14/Jul/2021 10:44:33] "GET /10.58.1.50 HTTP/1.1" 200 -
10.58.1.50      TicketService        99%   58%
::1 - - [14/Jul/2021 10:44:33] "GET /10.58.1.118 HTTP/1.1" 200 -
10.58.1.118     MLService            83%   46%
::1 - - [14/Jul/2021 10:44:33] "GET /10.58.1.129 HTTP/1.1" 200 -
10.58.1.129     RoleService          52%   97%
::1 - - [14/Jul/2021 10:44:33] "GET /10.58.1.101 HTTP/1.1" 200 -
10.58.1.101     RoleService          27%   55%
::1 - - [14/Jul/2021 10:44:33] "GET /10.58.1.107 HTTP/1.1" 200 -
10.58.1.107     AuthService          20%   21%
::1 - - [14/Jul/2021 10:44:33] "GET /10.58.1.76 HTTP/1.1" 200 -
10.58.1.76      MLService            80%   78%
::1 - - [14/Jul/2021 10:44:33] "GET /10.58.1.25 HTTP/1.1" 200 -
10.58.1.25      AuthService          69%   28%
::1 - - [14/Jul/2021 10:44:33] "GET /10.58.1.78 HTTP/1.1" 200 -
10.58.1.78      IdService            15%   60%
::1 - - [14/Jul/2021 10:44:33] "GET /10.58.1.121 HTTP/1.1" 200 -
10.58.1.121     UserService          94%   98%
::1 - - [14/Jul/2021 10:44:33] "GET /10.58.1.12 HTTP/1.1" 200 -
10.58.1.12      PermissionsService   29%   75%
::1 - - [14/Jul/2021 10:44:33] "GET /10.58.1.31 HTTP/1.1" 200 -
10.58.1.31      UserService          44%   43%
::1 - - [14/Jul/2021 10:44:33] "GET /10.58.1.112 HTTP/1.1" 200 -
10.58.1.112     IdService            51%   29%
::1 - - [14/Jul/2021 10:44:33] "GET /10.58.1.145 HTTP/1.1" 200 -
10.58.1.145     AuthService          45%    0%
::1 - - [14/Jul/2021 10:44:33] "GET /10.58.1.37 HTTP/1.1" 200 -
10.58.1.37      TimeService          97%   26%
::1 - - [14/Jul/2021 10:44:33] "GET /10.58.1.83 HTTP/1.1" 200 -
10.58.1.83      StorageService       98%   12%
::1 - - [14/Jul/2021 10:44:33] "GET /10.58.1.122 HTTP/1.1" 200 -
10.58.1.122     GeoService           75%   67%
::1 - - [14/Jul/2021 10:44:33] "GET /10.58.1.69 HTTP/1.1" 200 -
10.58.1.69      StorageService       31%   93%
::1 - - [14/Jul/2021 10:44:33] "GET /10.58.1.17 HTTP/1.1" 200 -
10.58.1.17      MLService            96%   70%
::1 - - [14/Jul/2021 10:44:33] "GET /10.58.1.1 HTTP/1.1" 200 -
10.58.1.1       StorageService       46%   47%
::1 - - [14/Jul/2021 10:44:33] "GET /10.58.1.79 HTTP/1.1" 200 -
10.58.1.79      MLService             6%    1%
::1 - - [14/Jul/2021 10:44:33] "GET /10.58.1.150 HTTP/1.1" 200 -
10.58.1.150     PermissionsService   53%    0%
::1 - - [14/Jul/2021 10:44:33] "GET /10.58.1.91 HTTP/1.1" 200 -
10.58.1.91      GeoService           10%   61%
::1 - - [14/Jul/2021 10:44:33] "GET /10.58.1.73 HTTP/1.1" 200 -
10.58.1.73      StorageService       87%    9%
::1 - - [14/Jul/2021 10:44:33] "GET /10.58.1.46 HTTP/1.1" 200 -
10.58.1.46      AuthService          45%   27%
::1 - - [14/Jul/2021 10:44:33] "GET /10.58.1.88 HTTP/1.1" 200 -
10.58.1.88      AuthService          74%   61%
::1 - - [14/Jul/2021 10:44:33] "GET /10.58.1.54 HTTP/1.1" 200 -
10.58.1.54      RoleService          52%   98%
::1 - - [14/Jul/2021 10:44:33] "GET /10.58.1.52 HTTP/1.1" 200 -
10.58.1.52      UserService          21%   90%
::1 - - [14/Jul/2021 10:44:33] "GET /10.58.1.65 HTTP/1.1" 200 -
10.58.1.65      PermissionsService   41%    2%
::1 - - [14/Jul/2021 10:44:33] "GET /10.58.1.136 HTTP/1.1" 200 -
10.58.1.136     StorageService       37%   25%
::1 - - [14/Jul/2021 10:44:33] "GET /10.58.1.130 HTTP/1.1" 200 -
10.58.1.130     PermissionsService   79%   43%
::1 - - [14/Jul/2021 10:44:33] "GET /10.58.1.8 HTTP/1.1" 200 -
10.58.1.8       RoleService           2%   97%
::1 - - [14/Jul/2021 10:44:33] "GET /10.58.1.68 HTTP/1.1" 200 -
10.58.1.68      GeoService           97%    6%
::1 - - [14/Jul/2021 10:44:33] "GET /10.58.1.127 HTTP/1.1" 200 -
10.58.1.127     PermissionsService   14%   73%
::1 - - [14/Jul/2021 10:44:33] "GET /10.58.1.33 HTTP/1.1" 200 -
10.58.1.33      GeoService           48%   55%
::1 - - [14/Jul/2021 10:44:33] "GET /10.58.1.11 HTTP/1.1" 200 -
10.58.1.11      MLService            80%   16%
::1 - - [14/Jul/2021 10:44:33] "GET /10.58.1.147 HTTP/1.1" 200 -
10.58.1.147     AuthService          34%   10%
::1 - - [14/Jul/2021 10:44:33] "GET /10.58.1.133 HTTP/1.1" 200 -
10.58.1.133     IdService            72%   78%
::1 - - [14/Jul/2021 10:44:33] "GET /10.58.1.146 HTTP/1.1" 200 -
10.58.1.146     RoleService          56%   20%
::1 - - [14/Jul/2021 10:44:33] "GET /10.58.1.86 HTTP/1.1" 200 -
10.58.1.86      IdService            33%   55%
::1 - - [14/Jul/2021 10:44:33] "GET /10.58.1.66 HTTP/1.1" 200 -
10.58.1.66      MLService            12%   51%
::1 - - [14/Jul/2021 10:44:33] "GET /10.58.1.134 HTTP/1.1" 200 -
10.58.1.134     MLService            64%   31%
::1 - - [14/Jul/2021 10:44:33] "GET /10.58.1.6 HTTP/1.1" 200 -
10.58.1.6       StorageService       48%    7%
::1 - - [14/Jul/2021 10:44:33] "GET /10.58.1.105 HTTP/1.1" 200 -
10.58.1.105     RoleService          48%   72%
::1 - - [14/Jul/2021 10:44:33] "GET /10.58.1.56 HTTP/1.1" 200 -
10.58.1.56      AuthService          59%    5%
::1 - - [14/Jul/2021 10:44:33] "GET /10.58.1.144 HTTP/1.1" 200 -
10.58.1.144     GeoService           12%   73%
::1 - - [14/Jul/2021 10:44:33] "GET /10.58.1.97 HTTP/1.1" 200 -
10.58.1.97      RoleService          34%   71%
::1 - - [14/Jul/2021 10:44:33] "GET /10.58.1.92 HTTP/1.1" 200 -
10.58.1.92      IdService            97%   54%
::1 - - [14/Jul/2021 10:44:33] "GET /10.58.1.108 HTTP/1.1" 200 -
10.58.1.108     GeoService           37%   85%
::1 - - [14/Jul/2021 10:44:33] "GET /10.58.1.10 HTTP/1.1" 200 -
10.58.1.10      RoleService          51%   61%
::1 - - [14/Jul/2021 10:44:33] "GET /10.58.1.30 HTTP/1.1" 200 -
10.58.1.30      IdService            16%   24%
::1 - - [14/Jul/2021 10:44:33] "GET /10.58.1.64 HTTP/1.1" 200 -
10.58.1.64      IdService            34%   81%
::1 - - [14/Jul/2021 10:44:33] "GET /10.58.1.29 HTTP/1.1" 200 -
10.58.1.29      MLService            90%   28%
::1 - - [14/Jul/2021 10:44:33] "GET /10.58.1.114 HTTP/1.1" 200 -
10.58.1.114     StorageService       29%   90%

::1 - - [14/Jul/2021 10:44:35] "GET /10.58.1.3 HTTP/1.1" 200 -
::1 - - [14/Jul/2021 10:44:35] "GET /10.58.1.16 HTTP/1.1" 200 -
::1 - - [14/Jul/2021 10:44:35] "GET /10.58.1.80 HTTP/1.1" 200 -
::1 - - [14/Jul/2021 10:44:35] "GET /10.58.1.62 HTTP/1.1" 200 -
::1 - - [14/Jul/2021 10:44:35] "GET /10.58.1.135 HTTP/1.1" 200 -
::1 - - [14/Jul/2021 10:44:35] "GET /10.58.1.85 HTTP/1.1" 200 -
::1 - - [14/Jul/2021 10:44:35] "GET /10.58.1.128 HTTP/1.1" 200 -
::1 - - [14/Jul/2021 10:44:35] "GET /10.58.1.5 HTTP/1.1" 200 -
::1 - - [14/Jul/2021 10:44:35] "GET /10.58.1.72 HTTP/1.1" 200 -
::1 - - [14/Jul/2021 10:44:35] "GET /10.58.1.61 HTTP/1.1" 200 -
::1 - - [14/Jul/2021 10:44:35] "GET /10.58.1.74 HTTP/1.1" 200 -
::1 - - [14/Jul/2021 10:44:35] "GET /10.58.1.120 HTTP/1.1" 200 -
::1 - - [14/Jul/2021 10:44:35] "GET /10.58.1.96 HTTP/1.1" 200 -
::1 - - [14/Jul/2021 10:44:35] "GET /10.58.1.2 HTTP/1.1" 200 -
::1 - - [14/Jul/2021 10:44:35] "GET /10.58.1.119 HTTP/1.1" 200 -
::1 - - [14/Jul/2021 10:44:35] "GET /10.58.1.32 HTTP/1.1" 200 -
::1 - - [14/Jul/2021 10:44:35] "GET /10.58.1.123 HTTP/1.1" 200 -
::1 - - [14/Jul/2021 10:44:35] "GET /10.58.1.94 HTTP/1.1" 200 -
::1 - - [14/Jul/2021 10:44:35] "GET /10.58.1.41 HTTP/1.1" 200 -
::1 - - [14/Jul/2021 10:44:35] "GET /10.58.1.113 HTTP/1.1" 200 -
::1 - - [14/Jul/2021 10:44:35] "GET /10.58.1.21 HTTP/1.1" 200 -
::1 - - [14/Jul/2021 10:44:35] "GET /10.58.1.28 HTTP/1.1" 200 -
::1 - - [14/Jul/2021 10:44:35] "GET /10.58.1.67 HTTP/1.1" 200 -
::1 - - [14/Jul/2021 10:44:35] "GET /10.58.1.137 HTTP/1.1" 200 -
::1 - - [14/Jul/2021 10:44:35] "GET /10.58.1.44 HTTP/1.1" 200 -
::1 - - [14/Jul/2021 10:44:35] "GET /10.58.1.34 HTTP/1.1" 200 -
::1 - - [14/Jul/2021 10:44:35] "GET /10.58.1.53 HTTP/1.1" 200 -
::1 - - [14/Jul/2021 10:44:35] "GET /10.58.1.109 HTTP/1.1" 200 -
::1 - - [14/Jul/2021 10:44:35] "GET /10.58.1.26 HTTP/1.1" 200 -
::1 - - [14/Jul/2021 10:44:35] "GET /10.58.1.149 HTTP/1.1" 200 -
::1 - - [14/Jul/2021 10:44:35] "GET /10.58.1.125 HTTP/1.1" 200 -
::1 - - [14/Jul/2021 10:44:35] "GET /10.58.1.82 HTTP/1.1" 200 -
::1 - - [14/Jul/2021 10:44:35] "GET /10.58.1.48 HTTP/1.1" 200 -
::1 - - [14/Jul/2021 10:44:35] "GET /10.58.1.15 HTTP/1.1" 200 -
::1 - - [14/Jul/2021 10:44:35] "GET /10.58.1.43 HTTP/1.1" 200 -
::1 - - [14/Jul/2021 10:44:35] "GET /10.58.1.39 HTTP/1.1" 200 -
::1 - - [14/Jul/2021 10:44:35] "GET /10.58.1.102 HTTP/1.1" 200 -
::1 - - [14/Jul/2021 10:44:35] "GET /10.58.1.131 HTTP/1.1" 200 -
::1 - - [14/Jul/2021 10:44:35] "GET /10.58.1.57 HTTP/1.1" 200 -
::1 - - [14/Jul/2021 10:44:35] "GET /10.58.1.148 HTTP/1.1" 200 -
::1 - - [14/Jul/2021 10:44:35] "GET /10.58.1.49 HTTP/1.1" 200 -
::1 - - [14/Jul/2021 10:44:35] "GET /10.58.1.75 HTTP/1.1" 200 -
::1 - - [14/Jul/2021 10:44:35] "GET /10.58.1.24 HTTP/1.1" 200 -
::1 - - [14/Jul/2021 10:44:35] "GET /10.58.1.55 HTTP/1.1" 200 -
::1 - - [14/Jul/2021 10:44:35] "GET /10.58.1.84 HTTP/1.1" 200 -
::1 - - [14/Jul/2021 10:44:35] "GET /10.58.1.81 HTTP/1.1" 200 -
::1 - - [14/Jul/2021 10:44:35] "GET /10.58.1.45 HTTP/1.1" 200 -
::1 - - [14/Jul/2021 10:44:35] "GET /10.58.1.140 HTTP/1.1" 200 -
::1 - - [14/Jul/2021 10:44:35] "GET /10.58.1.40 HTTP/1.1" 200 -
::1 - - [14/Jul/2021 10:44:35] "GET /10.58.1.47 HTTP/1.1" 200 -
::1 - - [14/Jul/2021 10:44:35] "GET /10.58.1.70 HTTP/1.1" 200 -
::1 - - [14/Jul/2021 10:44:35] "GET /10.58.1.20 HTTP/1.1" 200 -
::1 - - [14/Jul/2021 10:44:35] "GET /10.58.1.111 HTTP/1.1" 200 -
::1 - - [14/Jul/2021 10:44:35] "GET /10.58.1.117 HTTP/1.1" 200 -
::1 - - [14/Jul/2021 10:44:35] "GET /10.58.1.93 HTTP/1.1" 200 -
::1 - - [14/Jul/2021 10:44:35] "GET /10.58.1.27 HTTP/1.1" 200 -
::1 - - [14/Jul/2021 10:44:35] "GET /10.58.1.89 HTTP/1.1" 200 -
::1 - - [14/Jul/2021 10:44:35] "GET /10.58.1.139 HTTP/1.1" 200 -
::1 - - [14/Jul/2021 10:44:35] "GET /10.58.1.51 HTTP/1.1" 200 -
::1 - - [14/Jul/2021 10:44:36] "GET /10.58.1.13 HTTP/1.1" 200 -
::1 - - [14/Jul/2021 10:44:36] "GET /10.58.1.90 HTTP/1.1" 200 -
::1 - - [14/Jul/2021 10:44:36] "GET /10.58.1.36 HTTP/1.1" 200 -
::1 - - [14/Jul/2021 10:44:36] "GET /10.58.1.98 HTTP/1.1" 200 -
::1 - - [14/Jul/2021 10:44:36] "GET /10.58.1.106 HTTP/1.1" 200 -
::1 - - [14/Jul/2021 10:44:36] "GET /10.58.1.143 HTTP/1.1" 200 -
::1 - - [14/Jul/2021 10:44:36] "GET /10.58.1.132 HTTP/1.1" 200 -
::1 - - [14/Jul/2021 10:44:36] "GET /10.58.1.14 HTTP/1.1" 200 -
::1 - - [14/Jul/2021 10:44:36] "GET /10.58.1.42 HTTP/1.1" 200 -
::1 - - [14/Jul/2021 10:44:36] "GET /10.58.1.77 HTTP/1.1" 200 -
::1 - - [14/Jul/2021 10:44:36] "GET /10.58.1.110 HTTP/1.1" 200 -
::1 - - [14/Jul/2021 10:44:36] "GET /10.58.1.35 HTTP/1.1" 200 -
::1 - - [14/Jul/2021 10:44:36] "GET /10.58.1.60 HTTP/1.1" 200 -
::1 - - [14/Jul/2021 10:44:36] "GET /10.58.1.100 HTTP/1.1" 200 -
::1 - - [14/Jul/2021 10:44:36] "GET /10.58.1.22 HTTP/1.1" 200 -
::1 - - [14/Jul/2021 10:44:36] "GET /10.58.1.126 HTTP/1.1" 200 -
::1 - - [14/Jul/2021 10:44:36] "GET /10.58.1.71 HTTP/1.1" 200 -
::1 - - [14/Jul/2021 10:44:36] "GET /10.58.1.23 HTTP/1.1" 200 -
::1 - - [14/Jul/2021 10:44:36] "GET /10.58.1.87 HTTP/1.1" 200 -
::1 - - [14/Jul/2021 10:44:36] "GET /10.58.1.138 HTTP/1.1" 200 -
::1 - - [14/Jul/2021 10:44:36] "GET /10.58.1.18 HTTP/1.1" 200 -
::1 - - [14/Jul/2021 10:44:36] "GET /10.58.1.9 HTTP/1.1" 200 -
::1 - - [14/Jul/2021 10:44:36] "GET /10.58.1.116 HTTP/1.1" 200 -
::1 - - [14/Jul/2021 10:44:36] "GET /10.58.1.141 HTTP/1.1" 200 -
::1 - - [14/Jul/2021 10:44:36] "GET /10.58.1.103 HTTP/1.1" 200 -
::1 - - [14/Jul/2021 10:44:36] "GET /10.58.1.19 HTTP/1.1" 200 -
::1 - - [14/Jul/2021 10:44:36] "GET /10.58.1.124 HTTP/1.1" 200 -
::1 - - [14/Jul/2021 10:44:36] "GET /10.58.1.99 HTTP/1.1" 200 -
::1 - - [14/Jul/2021 10:44:36] "GET /10.58.1.63 HTTP/1.1" 200 -
::1 - - [14/Jul/2021 10:44:36] "GET /10.58.1.38 HTTP/1.1" 200 -
::1 - - [14/Jul/2021 10:44:36] "GET /10.58.1.95 HTTP/1.1" 200 -
::1 - - [14/Jul/2021 10:44:36] "GET /10.58.1.104 HTTP/1.1" 200 -
::1 - - [14/Jul/2021 10:44:36] "GET /10.58.1.142 HTTP/1.1" 200 -
::1 - - [14/Jul/2021 10:44:36] "GET /10.58.1.115 HTTP/1.1" 200 -
::1 - - [14/Jul/2021 10:44:36] "GET /10.58.1.7 HTTP/1.1" 200 -
::1 - - [14/Jul/2021 10:44:36] "GET /10.58.1.58 HTTP/1.1" 200 -
::1 - - [14/Jul/2021 10:44:36] "GET /10.58.1.4 HTTP/1.1" 200 -
::1 - - [14/Jul/2021 10:44:36] "GET /10.58.1.50 HTTP/1.1" 200 -
::1 - - [14/Jul/2021 10:44:36] "GET /10.58.1.118 HTTP/1.1" 200 -
::1 - - [14/Jul/2021 10:44:36] "GET /10.58.1.129 HTTP/1.1" 200 -
::1 - - [14/Jul/2021 10:44:36] "GET /10.58.1.101 HTTP/1.1" 200 -
::1 - - [14/Jul/2021 10:44:36] "GET /10.58.1.107 HTTP/1.1" 200 -
::1 - - [14/Jul/2021 10:44:36] "GET /10.58.1.76 HTTP/1.1" 200 -
::1 - - [14/Jul/2021 10:44:36] "GET /10.58.1.25 HTTP/1.1" 200 -
::1 - - [14/Jul/2021 10:44:36] "GET /10.58.1.78 HTTP/1.1" 200 -
::1 - - [14/Jul/2021 10:44:36] "GET /10.58.1.121 HTTP/1.1" 200 -
::1 - - [14/Jul/2021 10:44:36] "GET /10.58.1.12 HTTP/1.1" 200 -
::1 - - [14/Jul/2021 10:44:36] "GET /10.58.1.31 HTTP/1.1" 200 -
::1 - - [14/Jul/2021 10:44:36] "GET /10.58.1.112 HTTP/1.1" 200 -
::1 - - [14/Jul/2021 10:44:36] "GET /10.58.1.145 HTTP/1.1" 200 -
::1 - - [14/Jul/2021 10:44:36] "GET /10.58.1.37 HTTP/1.1" 200 -
::1 - - [14/Jul/2021 10:44:36] "GET /10.58.1.83 HTTP/1.1" 200 -
::1 - - [14/Jul/2021 10:44:36] "GET /10.58.1.122 HTTP/1.1" 200 -
::1 - - [14/Jul/2021 10:44:36] "GET /10.58.1.69 HTTP/1.1" 200 -
::1 - - [14/Jul/2021 10:44:36] "GET /10.58.1.17 HTTP/1.1" 200 -
::1 - - [14/Jul/2021 10:44:36] "GET /10.58.1.1 HTTP/1.1" 200 -
::1 - - [14/Jul/2021 10:44:36] "GET /10.58.1.79 HTTP/1.1" 200 -
::1 - - [14/Jul/2021 10:44:36] "GET /10.58.1.150 HTTP/1.1" 200 -
::1 - - [14/Jul/2021 10:44:36] "GET /10.58.1.91 HTTP/1.1" 200 -
::1 - - [14/Jul/2021 10:44:36] "GET /10.58.1.73 HTTP/1.1" 200 -
::1 - - [14/Jul/2021 10:44:36] "GET /10.58.1.46 HTTP/1.1" 200 -
::1 - - [14/Jul/2021 10:44:36] "GET /10.58.1.88 HTTP/1.1" 200 -
::1 - - [14/Jul/2021 10:44:36] "GET /10.58.1.54 HTTP/1.1" 200 -
::1 - - [14/Jul/2021 10:44:36] "GET /10.58.1.52 HTTP/1.1" 200 -
::1 - - [14/Jul/2021 10:44:36] "GET /10.58.1.65 HTTP/1.1" 200 -
::1 - - [14/Jul/2021 10:44:36] "GET /10.58.1.136 HTTP/1.1" 200 -
::1 - - [14/Jul/2021 10:44:36] "GET /10.58.1.130 HTTP/1.1" 200 -
::1 - - [14/Jul/2021 10:44:36] "GET /10.58.1.8 HTTP/1.1" 200 -
::1 - - [14/Jul/2021 10:44:36] "GET /10.58.1.68 HTTP/1.1" 200 -
::1 - - [14/Jul/2021 10:44:36] "GET /10.58.1.127 HTTP/1.1" 200 -
::1 - - [14/Jul/2021 10:44:36] "GET /10.58.1.33 HTTP/1.1" 200 -
::1 - - [14/Jul/2021 10:44:36] "GET /10.58.1.11 HTTP/1.1" 200 -
::1 - - [14/Jul/2021 10:44:36] "GET /10.58.1.147 HTTP/1.1" 200 -
::1 - - [14/Jul/2021 10:44:36] "GET /10.58.1.133 HTTP/1.1" 200 -
::1 - - [14/Jul/2021 10:44:36] "GET /10.58.1.146 HTTP/1.1" 200 -
::1 - - [14/Jul/2021 10:44:36] "GET /10.58.1.86 HTTP/1.1" 200 -
::1 - - [14/Jul/2021 10:44:36] "GET /10.58.1.66 HTTP/1.1" 200 -
::1 - - [14/Jul/2021 10:44:36] "GET /10.58.1.134 HTTP/1.1" 200 -
::1 - - [14/Jul/2021 10:44:36] "GET /10.58.1.6 HTTP/1.1" 200 -
::1 - - [14/Jul/2021 10:44:36] "GET /10.58.1.105 HTTP/1.1" 200 -
::1 - - [14/Jul/2021 10:44:36] "GET /10.58.1.56 HTTP/1.1" 200 -
::1 - - [14/Jul/2021 10:44:36] "GET /10.58.1.144 HTTP/1.1" 200 -
::1 - - [14/Jul/2021 10:44:36] "GET /10.58.1.97 HTTP/1.1" 200 -
::1 - - [14/Jul/2021 10:44:36] "GET /10.58.1.92 HTTP/1.1" 200 -
::1 - - [14/Jul/2021 10:44:36] "GET /10.58.1.108 HTTP/1.1" 200 -
::1 - - [14/Jul/2021 10:44:36] "GET /10.58.1.10 HTTP/1.1" 200 -
::1 - - [14/Jul/2021 10:44:36] "GET /10.58.1.30 HTTP/1.1" 200 -
::1 - - [14/Jul/2021 10:44:36] "GET /10.58.1.64 HTTP/1.1" 200 -
::1 - - [14/Jul/2021 10:44:36] "GET /10.58.1.29 HTTP/1.1" 200 -
::1 - - [14/Jul/2021 10:44:36] "GET /10.58.1.114 HTTP/1.1" 200 -
Service             Status    CPU Memory
----------------------------------------
GeoService          Healthy    46%   50%
MLService           Healthy    42%   63%
IdService           Healthy    51%   47%
RoleService         Healthy    44%   50%
TicketService       Healthy    31%   58%
TimeService         Healthy    67%   52%
PermissionsService  Healthy    45%   51%
StorageService      Healthy    45%   44%
AuthService         Healthy    38%   41%
UserService         Healthy    50%   56%

----------------------------------------------------------------------
Ran 4 tests in 9.795s

OK
```

## The Impatient

Execute `bootstrap.sh`. PRs welcome.

## Example Client Execution

The client utility features can be seen with `-h` command-line arguments.

```
$ ./cpx.py -h
usage: cpx.py [-h] command url

positional arguments:
  command     command, e.g., services, status, et al
  url         the url, e.g., http://10.0.0.1:5000/

optional arguments:
  -h, --help  show this help message and exit
```

In order to see the overall health of each service aggregated across all server
instances, execute with the status command:

```
$ ./cpx.py status http://$(minikube ip)
Service             Status    CPU Memory
----------------------------------------
GeoService          Healthy    44%   43%
MLService           Healthy    37%   50%
IdService           Healthy    57%   61%
RoleService         Healthy    47%   55%
TicketService       Healthy    50%   51%
TimeService         Healthy    45%   66%
PermissionsService  Healthy    58%   52%
StorageService      Healthy    44%   48%
AuthService         Healthy    53%   56%
UserService         Healthy    36%   57%
```

In order to see a continuous display of all services across all servers in five
second increments, issue the `services` command. When you are finished 
observing, press `ctrl + c` to exit and return to the command prompt.

```
$ ./cpx.py services http://$(minikube ip)
IP              Service             CPU Memory
----------------------------------------------
10.58.1.59      GeoService           89%   17%
10.58.1.3       MLService            99%   55%
10.58.1.16      IdService             7%   50%
10.58.1.80      RoleService          74%   62%
10.58.1.62      IdService             3%   11%
10.58.1.135     TicketService        66%   53%
10.58.1.85      TimeService          39%   41%
10.58.1.128     PermissionsService   56%   36%
...
```