#!/usr/bin/env bash
#
# Check if the environment is using a working ssh-agent. If not, search
# all ssh-agent processes and find one we can use. If that fails, start a
# new one and pass the variables to the caller.
#
# Tested on: macOS 10.15
# Usage: eval `basename $0`
# Author: Justin Cook <jhcook@secnix.com>

#set -x
set -o nounset
set -o pipefail

start_ssh_agent() {
  ssh-agent -s
}

check_pid_and_socket() {
  if kill -s 0 $1 2>/dev/null
  then 
    if [ -O "$2" ] && [ -S "$2" ]
    then
      return 0
    else
      kill -9 $1 2>/dev/null || /bin/true
    fi
    return 1
  fi
}

# If the env has an operating ssh-agent, bail.
if [ -z ${SSH_AGENT_PID+x} ] && [ -z ${SSH_AUTH_SOCK+x} ]
then
  if [ `check_pid_and_socket "${SSH_AGENT_PID}" "${SSH_AUTH_SOCK}"` ]
  then # We're good
    exit
  fi
fi

# Iterate through all pids that are ssh-agent and are owned by the current user
for pid in $(ps aux | awk "\$11 ~ /ssh-agent/ && \$1 ~ /`whoami`/ {print\$2}" | sort)
do
  ssh_agent_pid=${pid}
  ssh_auth_sock=`find ${TMPDIR} -name agent.$((${pid}-1)) 2>/dev/null`
  if check_pid_and_socket $ssh_agent_pid $ssh_auth_sock
  then
    printf "SSH_AUTH_SOCK=${ssh_auth_sock}; export SSH_AUTH_SOCK;\n"
    printf "SSH_AGENT_PID=${ssh_agent_pid}; export SSH_AGENT_PID;\n"
    printf "echo Agent pid ${ssh_agent_pid}\n"
    exit
  fi
done

# If we landed here we must start an agent as nothing was found
start_ssh_agent
