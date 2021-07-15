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
..IP              Service             CPU Memory
----------------------------------------------
::1 - - [15/Jul/2021 23:20:38] "GET /10.58.1.59 HTTP/1.1" 200 -
10.58.1.59      GeoService           46%   61%
::1 - - [15/Jul/2021 23:20:38] "GET /10.58.1.3 HTTP/1.1" 200 -
10.58.1.3       MLService            75%   66%
::1 - - [15/Jul/2021 23:20:38] "GET /10.58.1.16 HTTP/1.1" 200 -
10.58.1.16      IdService            80%   40%
::1 - - [15/Jul/2021 23:20:38] "GET /10.58.1.80 HTTP/1.1" 200 -
10.58.1.80      RoleService          59%   84%
::1 - - [15/Jul/2021 23:20:38] "GET /10.58.1.62 HTTP/1.1" 200 -
10.58.1.62      IdService            97%   80%
::1 - - [15/Jul/2021 23:20:38] "GET /10.58.1.135 HTTP/1.1" 200 -
10.58.1.135     TicketService         6%   20%
::1 - - [15/Jul/2021 23:20:38] "GET /10.58.1.85 HTTP/1.1" 200 -
10.58.1.85      TimeService          33%   22%
::1 - - [15/Jul/2021 23:20:38] "GET /10.58.1.128 HTTP/1.1" 200 -
10.58.1.128     PermissionsService    8%   34%
::1 - - [15/Jul/2021 23:20:38] "GET /10.58.1.5 HTTP/1.1" 200 -
10.58.1.5       StorageService       57%   96%
::1 - - [15/Jul/2021 23:20:38] "GET /10.58.1.72 HTTP/1.1" 200 -
10.58.1.72      RoleService           1%   15%
::1 - - [15/Jul/2021 23:20:38] "GET /10.58.1.61 HTTP/1.1" 200 -
10.58.1.61      AuthService          74%   25%
::1 - - [15/Jul/2021 23:20:38] "GET /10.58.1.74 HTTP/1.1" 200 -
10.58.1.74      TicketService        77%   14%
::1 - - [15/Jul/2021 23:20:38] "GET /10.58.1.120 HTTP/1.1" 200 -
10.58.1.120     IdService            53%   66%
::1 - - [15/Jul/2021 23:20:38] "GET /10.58.1.96 HTTP/1.1" 200 -
10.58.1.96      IdService            65%   83%
::1 - - [15/Jul/2021 23:20:38] "GET /10.58.1.2 HTTP/1.1" 200 -
10.58.1.2       TimeService          81%   52%
::1 - - [15/Jul/2021 23:20:38] "GET /10.58.1.119 HTTP/1.1" 200 -
10.58.1.119     GeoService           43%   32%
::1 - - [15/Jul/2021 23:20:38] "GET /10.58.1.32 HTTP/1.1" 200 -
10.58.1.32      TimeService          39%   83%
::1 - - [15/Jul/2021 23:20:38] "GET /10.58.1.123 HTTP/1.1" 200 -
10.58.1.123     IdService            79%   45%
::1 - - [15/Jul/2021 23:20:38] "GET /10.58.1.94 HTTP/1.1" 200 -
10.58.1.94      GeoService            6%   10%
::1 - - [15/Jul/2021 23:20:38] "GET /10.58.1.41 HTTP/1.1" 200 -
10.58.1.41      RoleService          86%   72%
::1 - - [15/Jul/2021 23:20:38] "GET /10.58.1.113 HTTP/1.1" 200 -
10.58.1.113     TicketService        41%   81%
::1 - - [15/Jul/2021 23:20:38] "GET /10.58.1.21 HTTP/1.1" 200 -
10.58.1.21      RoleService           8%   92%
::1 - - [15/Jul/2021 23:20:38] "GET /10.58.1.28 HTTP/1.1" 200 -
10.58.1.28      AuthService          21%    0%
::1 - - [15/Jul/2021 23:20:38] "GET /10.58.1.67 HTTP/1.1" 200 -
10.58.1.67      GeoService           56%   47%
::1 - - [15/Jul/2021 23:20:38] "GET /10.58.1.137 HTTP/1.1" 200 -
10.58.1.137     StorageService       53%   39%
::1 - - [15/Jul/2021 23:20:38] "GET /10.58.1.44 HTTP/1.1" 200 -
10.58.1.44      GeoService           37%   45%
::1 - - [15/Jul/2021 23:20:38] "GET /10.58.1.34 HTTP/1.1" 200 -
10.58.1.34      RoleService          36%   91%
::1 - - [15/Jul/2021 23:20:38] "GET /10.58.1.53 HTTP/1.1" 200 -
10.58.1.53      StorageService       94%   55%
::1 - - [15/Jul/2021 23:20:38] "GET /10.58.1.109 HTTP/1.1" 200 -
10.58.1.109     AuthService          23%   29%
::1 - - [15/Jul/2021 23:20:38] "GET /10.58.1.26 HTTP/1.1" 200 -
10.58.1.26      GeoService           85%   29%
::1 - - [15/Jul/2021 23:20:38] "GET /10.58.1.149 HTTP/1.1" 200 -
10.58.1.149     UserService          40%   80%
::1 - - [15/Jul/2021 23:20:38] "GET /10.58.1.125 HTTP/1.1" 200 -
10.58.1.125     IdService            53%   29%
::1 - - [15/Jul/2021 23:20:38] "GET /10.58.1.82 HTTP/1.1" 200 -
10.58.1.82      StorageService       58%   19%
::1 - - [15/Jul/2021 23:20:39] "GET /10.58.1.48 HTTP/1.1" 200 -
10.58.1.48      RoleService           9%   33%
::1 - - [15/Jul/2021 23:20:39] "GET /10.58.1.15 HTTP/1.1" 200 -
10.58.1.15      StorageService        0%   57%
::1 - - [15/Jul/2021 23:20:39] "GET /10.58.1.43 HTTP/1.1" 200 -
10.58.1.43      StorageService       64%   45%
::1 - - [15/Jul/2021 23:20:39] "GET /10.58.1.39 HTTP/1.1" 200 -
10.58.1.39      StorageService       11%   84%
::1 - - [15/Jul/2021 23:20:39] "GET /10.58.1.102 HTTP/1.1" 200 -
10.58.1.102     RoleService          77%   89%
::1 - - [15/Jul/2021 23:20:39] "GET /10.58.1.131 HTTP/1.1" 200 -
10.58.1.131     UserService           0%   30%
::1 - - [15/Jul/2021 23:20:39] "GET /10.58.1.57 HTTP/1.1" 200 -
10.58.1.57      AuthService          49%   21%
::1 - - [15/Jul/2021 23:20:39] "GET /10.58.1.148 HTTP/1.1" 200 -
10.58.1.148     GeoService           35%  100%
::1 - - [15/Jul/2021 23:20:39] "GET /10.58.1.49 HTTP/1.1" 200 -
10.58.1.49      RoleService          77%   41%
::1 - - [15/Jul/2021 23:20:39] "GET /10.58.1.75 HTTP/1.1" 200 -
10.58.1.75      RoleService          40%   18%
::1 - - [15/Jul/2021 23:20:39] "GET /10.58.1.24 HTTP/1.1" 200 -
10.58.1.24      IdService            58%   30%
::1 - - [15/Jul/2021 23:20:39] "GET /10.58.1.55 HTTP/1.1" 200 -
10.58.1.55      MLService            82%   54%
::1 - - [15/Jul/2021 23:20:39] "GET /10.58.1.84 HTTP/1.1" 200 -
10.58.1.84      AuthService          64%   15%
::1 - - [15/Jul/2021 23:20:39] "GET /10.58.1.81 HTTP/1.1" 200 -
10.58.1.81      AuthService          87%    3%
::1 - - [15/Jul/2021 23:20:39] "GET /10.58.1.45 HTTP/1.1" 200 -
10.58.1.45      TimeService           3%    0%
::1 - - [15/Jul/2021 23:20:39] "GET /10.58.1.140 HTTP/1.1" 200 -
10.58.1.140     PermissionsService   43%   67%
::1 - - [15/Jul/2021 23:20:39] "GET /10.58.1.40 HTTP/1.1" 200 -
10.58.1.40      IdService            81%   32%
::1 - - [15/Jul/2021 23:20:39] "GET /10.58.1.47 HTTP/1.1" 200 -
10.58.1.47      PermissionsService   66%   40%
::1 - - [15/Jul/2021 23:20:39] "GET /10.58.1.70 HTTP/1.1" 200 -
10.58.1.70      UserService          59%   39%
::1 - - [15/Jul/2021 23:20:39] "GET /10.58.1.20 HTTP/1.1" 200 -
10.58.1.20      GeoService           12%  100%
::1 - - [15/Jul/2021 23:20:39] "GET /10.58.1.111 HTTP/1.1" 200 -
10.58.1.111     TicketService        16%   79%
::1 - - [15/Jul/2021 23:20:39] "GET /10.58.1.117 HTTP/1.1" 200 -
10.58.1.117     IdService            11%   34%
::1 - - [15/Jul/2021 23:20:39] "GET /10.58.1.93 HTTP/1.1" 200 -
10.58.1.93      MLService            16%   31%
::1 - - [15/Jul/2021 23:20:39] "GET /10.58.1.27 HTTP/1.1" 200 -
10.58.1.27      RoleService          89%   49%
::1 - - [15/Jul/2021 23:20:39] "GET /10.58.1.89 HTTP/1.1" 200 -
10.58.1.89      AuthService          30%    5%
::1 - - [15/Jul/2021 23:20:39] "GET /10.58.1.139 HTTP/1.1" 200 -
10.58.1.139     TimeService          31%    0%
::1 - - [15/Jul/2021 23:20:39] "GET /10.58.1.51 HTTP/1.1" 200 -
10.58.1.51      IdService            91%   69%
::1 - - [15/Jul/2021 23:20:39] "GET /10.58.1.13 HTTP/1.1" 200 -
10.58.1.13      TicketService        56%    0%
::1 - - [15/Jul/2021 23:20:39] "GET /10.58.1.90 HTTP/1.1" 200 -
10.58.1.90      RoleService           4%   61%
::1 - - [15/Jul/2021 23:20:39] "GET /10.58.1.36 HTTP/1.1" 200 -
10.58.1.36      PermissionsService    1%   59%
::1 - - [15/Jul/2021 23:20:39] "GET /10.58.1.98 HTTP/1.1" 200 -
10.58.1.98      UserService          93%   65%
::1 - - [15/Jul/2021 23:20:39] "GET /10.58.1.106 HTTP/1.1" 200 -
10.58.1.106     MLService            55%   82%
::1 - - [15/Jul/2021 23:20:39] "GET /10.58.1.143 HTTP/1.1" 200 -
10.58.1.143     UserService           4%   55%
::1 - - [15/Jul/2021 23:20:39] "GET /10.58.1.132 HTTP/1.1" 200 -
10.58.1.132     RoleService          41%   54%
::1 - - [15/Jul/2021 23:20:39] "GET /10.58.1.14 HTTP/1.1" 200 -
10.58.1.14      IdService            51%   86%
::1 - - [15/Jul/2021 23:20:39] "GET /10.58.1.42 HTTP/1.1" 200 -
10.58.1.42      MLService            17%   47%
::1 - - [15/Jul/2021 23:20:39] "GET /10.58.1.77 HTTP/1.1" 200 -
10.58.1.77      UserService          49%    8%
::1 - - [15/Jul/2021 23:20:39] "GET /10.58.1.110 HTTP/1.1" 200 -
10.58.1.110     TimeService          97%   97%
::1 - - [15/Jul/2021 23:20:39] "GET /10.58.1.35 HTTP/1.1" 200 -
10.58.1.35      AuthService          80%    7%
::1 - - [15/Jul/2021 23:20:39] "GET /10.58.1.60 HTTP/1.1" 200 -
10.58.1.60      TicketService        14%   26%
::1 - - [15/Jul/2021 23:20:39] "GET /10.58.1.100 HTTP/1.1" 200 -
10.58.1.100     RoleService          19%   54%
::1 - - [15/Jul/2021 23:20:39] "GET /10.58.1.22 HTTP/1.1" 200 -
10.58.1.22      RoleService          10%    3%
::1 - - [15/Jul/2021 23:20:39] "GET /10.58.1.126 HTTP/1.1" 200 -
10.58.1.126     GeoService           73%   26%
::1 - - [15/Jul/2021 23:20:39] "GET /10.58.1.71 HTTP/1.1" 200 -
10.58.1.71      IdService            44%   22%
::1 - - [15/Jul/2021 23:20:39] "GET /10.58.1.23 HTTP/1.1" 200 -
10.58.1.23      TimeService          82%    6%
::1 - - [15/Jul/2021 23:20:39] "GET /10.58.1.87 HTTP/1.1" 200 -
10.58.1.87      PermissionsService    9%   18%
::1 - - [15/Jul/2021 23:20:39] "GET /10.58.1.138 HTTP/1.1" 200 -
10.58.1.138     GeoService           37%   79%
::1 - - [15/Jul/2021 23:20:39] "GET /10.58.1.18 HTTP/1.1" 200 -
10.58.1.18      RoleService          66%   73%
::1 - - [15/Jul/2021 23:20:39] "GET /10.58.1.9 HTTP/1.1" 200 -
10.58.1.9       AuthService          66%   83%
::1 - - [15/Jul/2021 23:20:39] "GET /10.58.1.116 HTTP/1.1" 200 -
10.58.1.116     IdService            31%   59%
::1 - - [15/Jul/2021 23:20:39] "GET /10.58.1.141 HTTP/1.1" 200 -
10.58.1.141     UserService          15%   74%
::1 - - [15/Jul/2021 23:20:39] "GET /10.58.1.103 HTTP/1.1" 200 -
10.58.1.103     MLService            31%   78%
::1 - - [15/Jul/2021 23:20:39] "GET /10.58.1.19 HTTP/1.1" 200 -
10.58.1.19      MLService            87%   23%
::1 - - [15/Jul/2021 23:20:39] "GET /10.58.1.124 HTTP/1.1" 200 -
10.58.1.124     RoleService          75%    9%
::1 - - [15/Jul/2021 23:20:39] "GET /10.58.1.99 HTTP/1.1" 200 -
10.58.1.99      StorageService       70%   44%
::1 - - [15/Jul/2021 23:20:39] "GET /10.58.1.63 HTTP/1.1" 200 -
10.58.1.63      MLService            43%   65%
::1 - - [15/Jul/2021 23:20:39] "GET /10.58.1.38 HTTP/1.1" 200 -
10.58.1.38      TimeService           2%   94%
::1 - - [15/Jul/2021 23:20:39] "GET /10.58.1.95 HTTP/1.1" 200 -
10.58.1.95      AuthService           9%   65%
::1 - - [15/Jul/2021 23:20:39] "GET /10.58.1.104 HTTP/1.1" 200 -
10.58.1.104     TicketService        83%   18%
::1 - - [15/Jul/2021 23:20:39] "GET /10.58.1.142 HTTP/1.1" 200 -
10.58.1.142     IdService            38%   90%
::1 - - [15/Jul/2021 23:20:39] "GET /10.58.1.115 HTTP/1.1" 200 -
10.58.1.115     GeoService           26%   10%
::1 - - [15/Jul/2021 23:20:39] "GET /10.58.1.7 HTTP/1.1" 200 -
10.58.1.7       RoleService          86%    3%
::1 - - [15/Jul/2021 23:20:39] "GET /10.58.1.58 HTTP/1.1" 200 -
10.58.1.58      TimeService          21%   48%
::1 - - [15/Jul/2021 23:20:39] "GET /10.58.1.4 HTTP/1.1" 200 -
10.58.1.4       StorageService       54%   79%
::1 - - [15/Jul/2021 23:20:39] "GET /10.58.1.50 HTTP/1.1" 200 -
10.58.1.50      TicketService        44%   35%
::1 - - [15/Jul/2021 23:20:39] "GET /10.58.1.118 HTTP/1.1" 200 -
10.58.1.118     MLService            28%   87%
::1 - - [15/Jul/2021 23:20:39] "GET /10.58.1.129 HTTP/1.1" 200 -
10.58.1.129     RoleService          33%   12%
::1 - - [15/Jul/2021 23:20:39] "GET /10.58.1.101 HTTP/1.1" 200 -
10.58.1.101     RoleService          34%   66%
::1 - - [15/Jul/2021 23:20:39] "GET /10.58.1.107 HTTP/1.1" 200 -
10.58.1.107     AuthService          98%   68%
::1 - - [15/Jul/2021 23:20:39] "GET /10.58.1.76 HTTP/1.1" 200 -
10.58.1.76      MLService            73%   98%
::1 - - [15/Jul/2021 23:20:39] "GET /10.58.1.25 HTTP/1.1" 200 -
10.58.1.25      AuthService          43%    9%
::1 - - [15/Jul/2021 23:20:39] "GET /10.58.1.78 HTTP/1.1" 200 -
10.58.1.78      IdService            95%    8%
::1 - - [15/Jul/2021 23:20:39] "GET /10.58.1.121 HTTP/1.1" 200 -
10.58.1.121     UserService          56%   45%
::1 - - [15/Jul/2021 23:20:39] "GET /10.58.1.12 HTTP/1.1" 200 -
10.58.1.12      PermissionsService   19%    8%
::1 - - [15/Jul/2021 23:20:39] "GET /10.58.1.31 HTTP/1.1" 200 -
10.58.1.31      UserService          98%   75%
::1 - - [15/Jul/2021 23:20:39] "GET /10.58.1.112 HTTP/1.1" 200 -
10.58.1.112     IdService            38%   41%
::1 - - [15/Jul/2021 23:20:39] "GET /10.58.1.145 HTTP/1.1" 200 -
10.58.1.145     AuthService          72%   49%
::1 - - [15/Jul/2021 23:20:39] "GET /10.58.1.37 HTTP/1.1" 200 -
10.58.1.37      TimeService          80%   25%
::1 - - [15/Jul/2021 23:20:39] "GET /10.58.1.83 HTTP/1.1" 200 -
10.58.1.83      StorageService       13%   48%
::1 - - [15/Jul/2021 23:20:39] "GET /10.58.1.122 HTTP/1.1" 200 -
10.58.1.122     GeoService           65%   70%
::1 - - [15/Jul/2021 23:20:39] "GET /10.58.1.69 HTTP/1.1" 200 -
10.58.1.69      StorageService       78%   18%
::1 - - [15/Jul/2021 23:20:39] "GET /10.58.1.17 HTTP/1.1" 200 -
10.58.1.17      MLService            48%   76%
::1 - - [15/Jul/2021 23:20:39] "GET /10.58.1.1 HTTP/1.1" 200 -
10.58.1.1       StorageService       81%   29%
::1 - - [15/Jul/2021 23:20:39] "GET /10.58.1.79 HTTP/1.1" 200 -
10.58.1.79      MLService             8%   49%
::1 - - [15/Jul/2021 23:20:39] "GET /10.58.1.150 HTTP/1.1" 200 -
10.58.1.150     PermissionsService   21%   19%
::1 - - [15/Jul/2021 23:20:39] "GET /10.58.1.91 HTTP/1.1" 200 -
10.58.1.91      GeoService           30%   80%
::1 - - [15/Jul/2021 23:20:39] "GET /10.58.1.73 HTTP/1.1" 200 -
10.58.1.73      StorageService       77%   73%
::1 - - [15/Jul/2021 23:20:39] "GET /10.58.1.46 HTTP/1.1" 200 -
10.58.1.46      AuthService          31%    0%
::1 - - [15/Jul/2021 23:20:39] "GET /10.58.1.88 HTTP/1.1" 200 -
10.58.1.88      AuthService          20%    3%
::1 - - [15/Jul/2021 23:20:39] "GET /10.58.1.54 HTTP/1.1" 200 -
10.58.1.54      RoleService          76%   27%
::1 - - [15/Jul/2021 23:20:39] "GET /10.58.1.52 HTTP/1.1" 200 -
10.58.1.52      UserService          77%   93%
::1 - - [15/Jul/2021 23:20:39] "GET /10.58.1.65 HTTP/1.1" 200 -
10.58.1.65      PermissionsService    0%   37%
::1 - - [15/Jul/2021 23:20:39] "GET /10.58.1.136 HTTP/1.1" 200 -
10.58.1.136     StorageService       15%   91%
::1 - - [15/Jul/2021 23:20:39] "GET /10.58.1.130 HTTP/1.1" 200 -
10.58.1.130     PermissionsService   60%   19%
::1 - - [15/Jul/2021 23:20:39] "GET /10.58.1.8 HTTP/1.1" 200 -
10.58.1.8       RoleService          45%   65%
::1 - - [15/Jul/2021 23:20:39] "GET /10.58.1.68 HTTP/1.1" 200 -
10.58.1.68      GeoService           65%   85%
::1 - - [15/Jul/2021 23:20:39] "GET /10.58.1.127 HTTP/1.1" 200 -
10.58.1.127     PermissionsService   73%    3%
::1 - - [15/Jul/2021 23:20:39] "GET /10.58.1.33 HTTP/1.1" 200 -
10.58.1.33      GeoService           62%    6%
::1 - - [15/Jul/2021 23:20:39] "GET /10.58.1.11 HTTP/1.1" 200 -
10.58.1.11      MLService             9%   65%
::1 - - [15/Jul/2021 23:20:39] "GET /10.58.1.147 HTTP/1.1" 200 -
10.58.1.147     AuthService          82%   74%
::1 - - [15/Jul/2021 23:20:39] "GET /10.58.1.133 HTTP/1.1" 200 -
10.58.1.133     IdService            22%    9%
::1 - - [15/Jul/2021 23:20:39] "GET /10.58.1.146 HTTP/1.1" 200 -
10.58.1.146     RoleService          50%   92%
::1 - - [15/Jul/2021 23:20:39] "GET /10.58.1.86 HTTP/1.1" 200 -
10.58.1.86      IdService            28%   50%
::1 - - [15/Jul/2021 23:20:39] "GET /10.58.1.66 HTTP/1.1" 200 -
10.58.1.66      MLService            28%    6%
::1 - - [15/Jul/2021 23:20:39] "GET /10.58.1.134 HTTP/1.1" 200 -
10.58.1.134     MLService             9%   17%
::1 - - [15/Jul/2021 23:20:39] "GET /10.58.1.6 HTTP/1.1" 200 -
10.58.1.6       StorageService       89%   25%
::1 - - [15/Jul/2021 23:20:39] "GET /10.58.1.105 HTTP/1.1" 200 -
10.58.1.105     RoleService          26%   42%
::1 - - [15/Jul/2021 23:20:39] "GET /10.58.1.56 HTTP/1.1" 200 -
10.58.1.56      AuthService          97%   63%
::1 - - [15/Jul/2021 23:20:39] "GET /10.58.1.144 HTTP/1.1" 200 -
10.58.1.144     GeoService            9%    9%
::1 - - [15/Jul/2021 23:20:39] "GET /10.58.1.97 HTTP/1.1" 200 -
10.58.1.97      RoleService          74%   88%
::1 - - [15/Jul/2021 23:20:39] "GET /10.58.1.92 HTTP/1.1" 200 -
10.58.1.92      IdService            80%   67%
::1 - - [15/Jul/2021 23:20:39] "GET /10.58.1.108 HTTP/1.1" 200 -
10.58.1.108     GeoService           87%   15%
::1 - - [15/Jul/2021 23:20:39] "GET /10.58.1.10 HTTP/1.1" 200 -
10.58.1.10      RoleService          48%    7%
::1 - - [15/Jul/2021 23:20:39] "GET /10.58.1.30 HTTP/1.1" 200 -
10.58.1.30      IdService            58%   48%
::1 - - [15/Jul/2021 23:20:39] "GET /10.58.1.64 HTTP/1.1" 200 -
10.58.1.64      IdService            69%   54%
::1 - - [15/Jul/2021 23:20:39] "GET /10.58.1.29 HTTP/1.1" 200 -
10.58.1.29      MLService            49%   72%
::1 - - [15/Jul/2021 23:20:39] "GET /10.58.1.114 HTTP/1.1" 200 -
10.58.1.114     StorageService       48%   54%

.::1 - - [15/Jul/2021 23:20:39] "GET /10.58.1.59 HTTP/1.1" 200 -
::1 - - [15/Jul/2021 23:20:39] "GET /10.58.1.3 HTTP/1.1" 200 -
::1 - - [15/Jul/2021 23:20:39] "GET /10.58.1.16 HTTP/1.1" 200 -
::1 - - [15/Jul/2021 23:20:39] "GET /10.58.1.80 HTTP/1.1" 200 -
::1 - - [15/Jul/2021 23:20:39] "GET /10.58.1.62 HTTP/1.1" 200 -
::1 - - [15/Jul/2021 23:20:39] "GET /10.58.1.135 HTTP/1.1" 200 -
::1 - - [15/Jul/2021 23:20:39] "GET /10.58.1.85 HTTP/1.1" 200 -
::1 - - [15/Jul/2021 23:20:39] "GET /10.58.1.128 HTTP/1.1" 200 -
::1 - - [15/Jul/2021 23:20:39] "GET /10.58.1.5 HTTP/1.1" 200 -
::1 - - [15/Jul/2021 23:20:39] "GET /10.58.1.72 HTTP/1.1" 200 -
::1 - - [15/Jul/2021 23:20:39] "GET /10.58.1.61 HTTP/1.1" 200 -
::1 - - [15/Jul/2021 23:20:39] "GET /10.58.1.74 HTTP/1.1" 200 -
::1 - - [15/Jul/2021 23:20:39] "GET /10.58.1.120 HTTP/1.1" 200 -
::1 - - [15/Jul/2021 23:20:39] "GET /10.58.1.96 HTTP/1.1" 200 -
::1 - - [15/Jul/2021 23:20:39] "GET /10.58.1.2 HTTP/1.1" 200 -
::1 - - [15/Jul/2021 23:20:39] "GET /10.58.1.119 HTTP/1.1" 200 -
::1 - - [15/Jul/2021 23:20:39] "GET /10.58.1.32 HTTP/1.1" 200 -
::1 - - [15/Jul/2021 23:20:39] "GET /10.58.1.123 HTTP/1.1" 200 -
::1 - - [15/Jul/2021 23:20:39] "GET /10.58.1.94 HTTP/1.1" 200 -
::1 - - [15/Jul/2021 23:20:39] "GET /10.58.1.41 HTTP/1.1" 200 -
::1 - - [15/Jul/2021 23:20:39] "GET /10.58.1.113 HTTP/1.1" 200 -
::1 - - [15/Jul/2021 23:20:39] "GET /10.58.1.21 HTTP/1.1" 200 -
::1 - - [15/Jul/2021 23:20:39] "GET /10.58.1.28 HTTP/1.1" 200 -
::1 - - [15/Jul/2021 23:20:39] "GET /10.58.1.67 HTTP/1.1" 200 -
::1 - - [15/Jul/2021 23:20:39] "GET /10.58.1.137 HTTP/1.1" 200 -
::1 - - [15/Jul/2021 23:20:39] "GET /10.58.1.44 HTTP/1.1" 200 -
::1 - - [15/Jul/2021 23:20:39] "GET /10.58.1.34 HTTP/1.1" 200 -
::1 - - [15/Jul/2021 23:20:39] "GET /10.58.1.53 HTTP/1.1" 200 -
::1 - - [15/Jul/2021 23:20:39] "GET /10.58.1.109 HTTP/1.1" 200 -
::1 - - [15/Jul/2021 23:20:39] "GET /10.58.1.26 HTTP/1.1" 200 -
::1 - - [15/Jul/2021 23:20:39] "GET /10.58.1.149 HTTP/1.1" 200 -
::1 - - [15/Jul/2021 23:20:39] "GET /10.58.1.125 HTTP/1.1" 200 -
::1 - - [15/Jul/2021 23:20:39] "GET /10.58.1.82 HTTP/1.1" 200 -
::1 - - [15/Jul/2021 23:20:39] "GET /10.58.1.48 HTTP/1.1" 200 -
::1 - - [15/Jul/2021 23:20:39] "GET /10.58.1.15 HTTP/1.1" 200 -
::1 - - [15/Jul/2021 23:20:39] "GET /10.58.1.43 HTTP/1.1" 200 -
::1 - - [15/Jul/2021 23:20:39] "GET /10.58.1.39 HTTP/1.1" 200 -
::1 - - [15/Jul/2021 23:20:39] "GET /10.58.1.102 HTTP/1.1" 200 -
::1 - - [15/Jul/2021 23:20:39] "GET /10.58.1.131 HTTP/1.1" 200 -
::1 - - [15/Jul/2021 23:20:39] "GET /10.58.1.57 HTTP/1.1" 200 -
::1 - - [15/Jul/2021 23:20:39] "GET /10.58.1.148 HTTP/1.1" 200 -
::1 - - [15/Jul/2021 23:20:39] "GET /10.58.1.49 HTTP/1.1" 200 -
::1 - - [15/Jul/2021 23:20:39] "GET /10.58.1.75 HTTP/1.1" 200 -
::1 - - [15/Jul/2021 23:20:39] "GET /10.58.1.24 HTTP/1.1" 200 -
::1 - - [15/Jul/2021 23:20:39] "GET /10.58.1.55 HTTP/1.1" 200 -
::1 - - [15/Jul/2021 23:20:39] "GET /10.58.1.84 HTTP/1.1" 200 -
::1 - - [15/Jul/2021 23:20:39] "GET /10.58.1.81 HTTP/1.1" 200 -
::1 - - [15/Jul/2021 23:20:39] "GET /10.58.1.45 HTTP/1.1" 200 -
::1 - - [15/Jul/2021 23:20:39] "GET /10.58.1.140 HTTP/1.1" 200 -
::1 - - [15/Jul/2021 23:20:39] "GET /10.58.1.40 HTTP/1.1" 200 -
::1 - - [15/Jul/2021 23:20:39] "GET /10.58.1.47 HTTP/1.1" 200 -
::1 - - [15/Jul/2021 23:20:39] "GET /10.58.1.70 HTTP/1.1" 200 -
::1 - - [15/Jul/2021 23:20:39] "GET /10.58.1.20 HTTP/1.1" 200 -
::1 - - [15/Jul/2021 23:20:39] "GET /10.58.1.111 HTTP/1.1" 200 -
::1 - - [15/Jul/2021 23:20:39] "GET /10.58.1.117 HTTP/1.1" 200 -
::1 - - [15/Jul/2021 23:20:39] "GET /10.58.1.93 HTTP/1.1" 200 -
::1 - - [15/Jul/2021 23:20:39] "GET /10.58.1.27 HTTP/1.1" 200 -
::1 - - [15/Jul/2021 23:20:39] "GET /10.58.1.89 HTTP/1.1" 200 -
::1 - - [15/Jul/2021 23:20:39] "GET /10.58.1.139 HTTP/1.1" 200 -
::1 - - [15/Jul/2021 23:20:39] "GET /10.58.1.51 HTTP/1.1" 200 -
::1 - - [15/Jul/2021 23:20:39] "GET /10.58.1.13 HTTP/1.1" 200 -
::1 - - [15/Jul/2021 23:20:39] "GET /10.58.1.90 HTTP/1.1" 200 -
::1 - - [15/Jul/2021 23:20:39] "GET /10.58.1.36 HTTP/1.1" 200 -
::1 - - [15/Jul/2021 23:20:39] "GET /10.58.1.98 HTTP/1.1" 200 -
::1 - - [15/Jul/2021 23:20:39] "GET /10.58.1.106 HTTP/1.1" 200 -
::1 - - [15/Jul/2021 23:20:39] "GET /10.58.1.143 HTTP/1.1" 200 -
::1 - - [15/Jul/2021 23:20:39] "GET /10.58.1.132 HTTP/1.1" 200 -
::1 - - [15/Jul/2021 23:20:39] "GET /10.58.1.14 HTTP/1.1" 200 -
::1 - - [15/Jul/2021 23:20:39] "GET /10.58.1.42 HTTP/1.1" 200 -
::1 - - [15/Jul/2021 23:20:39] "GET /10.58.1.77 HTTP/1.1" 200 -
::1 - - [15/Jul/2021 23:20:39] "GET /10.58.1.110 HTTP/1.1" 200 -
::1 - - [15/Jul/2021 23:20:39] "GET /10.58.1.35 HTTP/1.1" 200 -
::1 - - [15/Jul/2021 23:20:39] "GET /10.58.1.60 HTTP/1.1" 200 -
::1 - - [15/Jul/2021 23:20:39] "GET /10.58.1.100 HTTP/1.1" 200 -
::1 - - [15/Jul/2021 23:20:39] "GET /10.58.1.22 HTTP/1.1" 200 -
::1 - - [15/Jul/2021 23:20:39] "GET /10.58.1.126 HTTP/1.1" 200 -
::1 - - [15/Jul/2021 23:20:39] "GET /10.58.1.71 HTTP/1.1" 200 -
::1 - - [15/Jul/2021 23:20:39] "GET /10.58.1.23 HTTP/1.1" 200 -
::1 - - [15/Jul/2021 23:20:39] "GET /10.58.1.87 HTTP/1.1" 200 -
::1 - - [15/Jul/2021 23:20:39] "GET /10.58.1.138 HTTP/1.1" 200 -
::1 - - [15/Jul/2021 23:20:39] "GET /10.58.1.18 HTTP/1.1" 200 -
::1 - - [15/Jul/2021 23:20:39] "GET /10.58.1.9 HTTP/1.1" 200 -
::1 - - [15/Jul/2021 23:20:39] "GET /10.58.1.116 HTTP/1.1" 200 -
::1 - - [15/Jul/2021 23:20:39] "GET /10.58.1.141 HTTP/1.1" 200 -
::1 - - [15/Jul/2021 23:20:39] "GET /10.58.1.103 HTTP/1.1" 200 -
::1 - - [15/Jul/2021 23:20:39] "GET /10.58.1.19 HTTP/1.1" 200 -
::1 - - [15/Jul/2021 23:20:39] "GET /10.58.1.124 HTTP/1.1" 200 -
::1 - - [15/Jul/2021 23:20:39] "GET /10.58.1.99 HTTP/1.1" 200 -
::1 - - [15/Jul/2021 23:20:39] "GET /10.58.1.63 HTTP/1.1" 200 -
::1 - - [15/Jul/2021 23:20:39] "GET /10.58.1.38 HTTP/1.1" 200 -
::1 - - [15/Jul/2021 23:20:39] "GET /10.58.1.95 HTTP/1.1" 200 -
::1 - - [15/Jul/2021 23:20:39] "GET /10.58.1.104 HTTP/1.1" 200 -
::1 - - [15/Jul/2021 23:20:39] "GET /10.58.1.142 HTTP/1.1" 200 -
::1 - - [15/Jul/2021 23:20:39] "GET /10.58.1.115 HTTP/1.1" 200 -
::1 - - [15/Jul/2021 23:20:39] "GET /10.58.1.7 HTTP/1.1" 200 -
::1 - - [15/Jul/2021 23:20:39] "GET /10.58.1.58 HTTP/1.1" 200 -
::1 - - [15/Jul/2021 23:20:39] "GET /10.58.1.4 HTTP/1.1" 200 -
::1 - - [15/Jul/2021 23:20:39] "GET /10.58.1.50 HTTP/1.1" 200 -
::1 - - [15/Jul/2021 23:20:39] "GET /10.58.1.118 HTTP/1.1" 200 -
::1 - - [15/Jul/2021 23:20:39] "GET /10.58.1.129 HTTP/1.1" 200 -
::1 - - [15/Jul/2021 23:20:39] "GET /10.58.1.101 HTTP/1.1" 200 -
::1 - - [15/Jul/2021 23:20:39] "GET /10.58.1.107 HTTP/1.1" 200 -
::1 - - [15/Jul/2021 23:20:39] "GET /10.58.1.76 HTTP/1.1" 200 -
::1 - - [15/Jul/2021 23:20:39] "GET /10.58.1.25 HTTP/1.1" 200 -
::1 - - [15/Jul/2021 23:20:39] "GET /10.58.1.78 HTTP/1.1" 200 -
::1 - - [15/Jul/2021 23:20:39] "GET /10.58.1.121 HTTP/1.1" 200 -
::1 - - [15/Jul/2021 23:20:39] "GET /10.58.1.12 HTTP/1.1" 200 -
::1 - - [15/Jul/2021 23:20:39] "GET /10.58.1.31 HTTP/1.1" 200 -
::1 - - [15/Jul/2021 23:20:39] "GET /10.58.1.112 HTTP/1.1" 200 -
::1 - - [15/Jul/2021 23:20:39] "GET /10.58.1.145 HTTP/1.1" 200 -
::1 - - [15/Jul/2021 23:20:39] "GET /10.58.1.37 HTTP/1.1" 200 -
::1 - - [15/Jul/2021 23:20:39] "GET /10.58.1.83 HTTP/1.1" 200 -
::1 - - [15/Jul/2021 23:20:39] "GET /10.58.1.122 HTTP/1.1" 200 -
::1 - - [15/Jul/2021 23:20:39] "GET /10.58.1.69 HTTP/1.1" 200 -
::1 - - [15/Jul/2021 23:20:39] "GET /10.58.1.17 HTTP/1.1" 200 -
::1 - - [15/Jul/2021 23:20:39] "GET /10.58.1.1 HTTP/1.1" 200 -
::1 - - [15/Jul/2021 23:20:39] "GET /10.58.1.79 HTTP/1.1" 200 -
::1 - - [15/Jul/2021 23:20:39] "GET /10.58.1.150 HTTP/1.1" 200 -
::1 - - [15/Jul/2021 23:20:39] "GET /10.58.1.91 HTTP/1.1" 200 -
::1 - - [15/Jul/2021 23:20:39] "GET /10.58.1.73 HTTP/1.1" 200 -
::1 - - [15/Jul/2021 23:20:39] "GET /10.58.1.46 HTTP/1.1" 200 -
::1 - - [15/Jul/2021 23:20:39] "GET /10.58.1.88 HTTP/1.1" 200 -
::1 - - [15/Jul/2021 23:20:39] "GET /10.58.1.54 HTTP/1.1" 200 -
::1 - - [15/Jul/2021 23:20:39] "GET /10.58.1.52 HTTP/1.1" 200 -
::1 - - [15/Jul/2021 23:20:39] "GET /10.58.1.65 HTTP/1.1" 200 -
::1 - - [15/Jul/2021 23:20:39] "GET /10.58.1.136 HTTP/1.1" 200 -
::1 - - [15/Jul/2021 23:20:39] "GET /10.58.1.130 HTTP/1.1" 200 -
::1 - - [15/Jul/2021 23:20:39] "GET /10.58.1.8 HTTP/1.1" 200 -
::1 - - [15/Jul/2021 23:20:39] "GET /10.58.1.68 HTTP/1.1" 200 -
::1 - - [15/Jul/2021 23:20:39] "GET /10.58.1.127 HTTP/1.1" 200 -
::1 - - [15/Jul/2021 23:20:39] "GET /10.58.1.33 HTTP/1.1" 200 -
::1 - - [15/Jul/2021 23:20:39] "GET /10.58.1.11 HTTP/1.1" 200 -
::1 - - [15/Jul/2021 23:20:39] "GET /10.58.1.147 HTTP/1.1" 200 -
::1 - - [15/Jul/2021 23:20:39] "GET /10.58.1.133 HTTP/1.1" 200 -
::1 - - [15/Jul/2021 23:20:39] "GET /10.58.1.146 HTTP/1.1" 200 -
::1 - - [15/Jul/2021 23:20:39] "GET /10.58.1.86 HTTP/1.1" 200 -
::1 - - [15/Jul/2021 23:20:39] "GET /10.58.1.66 HTTP/1.1" 200 -
::1 - - [15/Jul/2021 23:20:39] "GET /10.58.1.134 HTTP/1.1" 200 -
::1 - - [15/Jul/2021 23:20:39] "GET /10.58.1.6 HTTP/1.1" 200 -
::1 - - [15/Jul/2021 23:20:39] "GET /10.58.1.105 HTTP/1.1" 200 -
::1 - - [15/Jul/2021 23:20:39] "GET /10.58.1.56 HTTP/1.1" 200 -
::1 - - [15/Jul/2021 23:20:39] "GET /10.58.1.144 HTTP/1.1" 200 -
::1 - - [15/Jul/2021 23:20:39] "GET /10.58.1.97 HTTP/1.1" 200 -
::1 - - [15/Jul/2021 23:20:40] "GET /10.58.1.92 HTTP/1.1" 200 -
::1 - - [15/Jul/2021 23:20:40] "GET /10.58.1.108 HTTP/1.1" 200 -
::1 - - [15/Jul/2021 23:20:40] "GET /10.58.1.10 HTTP/1.1" 200 -
::1 - - [15/Jul/2021 23:20:40] "GET /10.58.1.30 HTTP/1.1" 200 -
::1 - - [15/Jul/2021 23:20:40] "GET /10.58.1.64 HTTP/1.1" 200 -
::1 - - [15/Jul/2021 23:20:40] "GET /10.58.1.29 HTTP/1.1" 200 -
::1 - - [15/Jul/2021 23:20:40] "GET /10.58.1.114 HTTP/1.1" 200 -
Service             Status    CPU Memory
----------------------------------------
GeoService          Healthy    47%   65%
MLService           Healthy    46%   41%
IdService           Healthy    42%   44%
RoleService         Healthy    49%   52%
TicketService       Healthy    64%   67%
TimeService         Healthy    61%   56%
PermissionsService  Healthy    47%   52%
StorageService      Healthy    44%   60%
AuthService         Healthy    36%   45%
UserService         Healthy    53%   50%
.
----------------------------------------------------------------------
Ran 4 tests in 1.164s

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