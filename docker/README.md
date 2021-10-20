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
# https://docs.docker.com/engine/install/centos/
yum install -y yum-utils
yum-config-manager --add-repo \
    https://download.docker.com/linux/centos/docker-ce.repo
yum install -y docker-ce docker-ce-cli containerd.io
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
  config.vm.provision "shell", inline: $script
  config.vm.post_up_message = "export DOCKER_HOST=ssh://vagrant@localhost:2222"
end
```

After a `vagrant up` you will need to copy your public key to 
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
