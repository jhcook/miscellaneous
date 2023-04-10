#!/usr/bin/env bash

# Set the local WIFICIDR for use in proxy settings
wifiaddr="$(ipconfig getifaddr en0)"
wifinmsk="$(ipconfig getoption en0 subnet_mask)"
WIFICIDR="$(python3 - << __EOF__
import ipaddress
print(str(ipaddress.ip_network("$wifiaddr/$wifinmsk", strict=False)))
__EOF__
)"
export WIFICIDR

# Load profile files
for _file_ in ${HOME}/profile.d/*.sh
do
  source "${_file_}"
done

test -e "${HOME}/bin/ssh-agent-start.sh" && eval `${HOME}/bin/ssh-agent-start.sh`

test -e "${HOME}/.iterm2_shell_integration.bash" && source "${HOME}/.iterm2_shell_integration.bash"

### MANAGED BY RANCHER DESKTOP START (DO NOT EDIT)
export PATH="/Users/jcook/.rd/bin:$PATH"
### MANAGED BY RANCHER DESKTOP END (DO NOT EDIT)
