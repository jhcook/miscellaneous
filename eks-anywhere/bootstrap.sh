#!/usr/bin/env sh

set -o nounset
set -o errexit

# Bring up the box
vagrant up

# Find the API endpoint port to forward
KUBECONFIG="$(find . -name *.kubeconfig)"
_EP_="$(awk -F: '/server/{print$4}' ${KUBECONFIG})"

# Set the port to forward in Vagranfile
sed -i.bak "s|config\.vm\.network \"forwarded_port\", guest: 8443, host: 8443|config.vm.network \"forwarded_port\", guest: ${_EP_}, host: ${_EP_}|g" Vagrantfile

# Reload
vagrant reload

echo "export KUBECONFIG=${KUBECONFIG}"