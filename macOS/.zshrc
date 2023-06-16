#!/usr/bin/env bash

# Set the local WIFICIDR for use in proxy settings
wifiaddr=""
wifinmsk=""
while [ -z "${wifiaddr:-}" ] || [ -z "${wifinmsk:-}" ]
do
  wifiaddr="$(ipconfig getifaddr en1)"
  wifinmsk="$(ipconfig getoption en1 subnet_mask)"
  sleep 1
done

WIFICIDR="$(python3 - << __EOF__
import ipaddress
print(str(ipaddress.ip_network("${wifiaddr}/${wifinmsk}", strict=False)))
__EOF__
)"
export WIFICIDR

# Load profile files
for _file_ in ${HOME}/profile.d/*.sh
do
  source "${_file_}"
done

test -e "${HOME}/bin/ssh-agent-start.sh" && eval `${HOME}/bin/ssh-agent-start.sh`

test -e "${HOME}/.iterm2_shell_integration.zsh" && source "${HOME}/.iterm2_shell_integration.zsh"

