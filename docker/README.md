# Docker

Herein are notes using Docker on macOS with RHEL virtual machines as the 
engine clients are native on macOS while the daemon runs on RHEL. It is assumed
`Homebrew`, `Virtualbox`, and `Vagrant` are installed and usable.

## Install Docker Client

Docker client is installed on macOS using Homebrew -- `brew install docker`.

If you are running a proxy and have environmental variables configured
accordingly, you will need to unset `ALL_PROXY`. Else you will receive the
following error:

```
$ docker ps
proxy: unknown scheme: http
```

## Install Docker Engine

Docker CE is installed on RHEL8 (CentOS8) using the official Docker
instructions found online. 

https://docs.docker.com/engine/install/centos/

I have encapsulated this in Vagrant using the Vagrantfile below:

```
# Your SSH public key
ssh_pub_key = "ssh-rsa ..."

$script = <<-SCRIPT
# Disable firewall
systemctl disable firewalld
systemctl stop firewalld
# https://docs.docker.com/engine/install/centos/
yum install -y yum-utils
yum-config-manager --add-repo \
    https://download.docker.com/linux/centos/docker-ce.repo
yum install -y docker-ce docker-ce-cli containerd.io
# Enable tcp:2375
sed -i 's|ExecStart=.*|ExecStart=/usr/bin/dockerd --containerd=/run/containerd/containerd.sock|g' /usr/lib/systemd/system/docker.service
systemctl daemon-reload
test -d /etc/docker || mkdir /etc/docker
echo '{"hosts": ["tcp://0.0.0.0:2375", "unix:///var/run/docker.sock"]}' > \
     /etc/docker/daemon.json
systemctl start docker
systemctl enable docker
# https://github.com/docker/docker.github.io/issues/9262
usermod -aG docker vagrant
cat - << __EOF__ >> ~vagrant/.ssh/authorized_keys
#{ssh_pub_key}
__EOF__
SCRIPT

Vagrant.configure("2") do |config|
  config.vm.box = "jhcook/centos8"
  config.vm.provider "virtualbox" do |v|
    v.memory = 16384
    v.cpus = 4
  end
  config.vm.network "forwarded_port", guest: 2375, host: 2375
  config.vm.provision "shell", inline: $script
  config.vm.post_up_message = "export DOCKER_HOST=tcp://localhost:2375"
end
```

Copy your public ssh key to `ssh_pub_key` in the Vagrantfile above, and after a
`vagrant up` you will not need to copy your public key to 
`~vagrant/.ssh/authorized_keys` in order for `docker ...` to connect.

## Deploy a registry

`docker run -d -p 5000:5000 --restart=always --name registry registry:2`

https://docs.docker.com/registry/deploying/

## Docker buildx

Buildx is used for cross and multiple platform builds.

https://docs.docker.com/buildx/working-with-buildx/

## Go Build for Linux

Since we are building binaries on macOS and running in Docker on Linux, we
need to configure builds accordingly, or we will receive the following error:

```
$ docker run hw
standard_init_linux.go:228: exec user process caused: exec format error
```

The following snippet will correct these issues before `go build ...`:

```
export CGO_ENABLED=0
export GOOS=linux
export GOARCH=amd64
```
