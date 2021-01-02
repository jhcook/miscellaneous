#!/usr/bin/env bash
#
# Check if the environment is using a working ssh-agent. If not, search
# all ssh-agent processes and find one we can use. If that fails, start a
# new one and pass the variables to the caller.
#
# Tested on: macOS 10.15, 11.0
# Usage: eval `basename $0`
# Author: Justin Cook <jhcook@secnix.com>

set -o nounset
set -o pipefail

SSH_AGENT_LOCKFILE="/var/tmp/`basename $0 | cut -f 1 -d '.'`.lock"

# Convenient function that takes two parameters.
# $1 a pid it checks to see if running
# $2 a file it checks to see if owned by user and a socket
# This folds out running -> owned by -> socket before terminating
# to be pedantic given root can terminate other user's processes.
check_pid_and_socket() {
  if kill -s 0 $1 2>/dev/null
  then # Process is running
    if [ -O "$2" ]
    then # File is a owned by user
      if [ -S "$2" ] 
      then # File is a socket
        return 0 # All checks out, so return success
      else 
        kill -9 $1 2>/dev/null || /bin/true
      fi
    fi
  fi
  return 1
}

# Check to see if a lock file exists. Backoff and retry for 60 seconds
# if so. Otherwise, bail loudly.

while :
do
  if test `find "${SSH_AGENT_LOCKFILE}" -mmin +1 2>/dev/null`
  then
    >&2 echo "Stale `basename $0` lockfile: ${SSH_AGENT_LOCKFILE}" 
    exit
  else
    mkdir -p "${SSH_AGENT_LOCKFILE}" 2>/dev/null && break || /bin/true
    sleep .25
  fi
done

trap "rm -fr ${SSH_AGENT_LOCKFILE}" EXIT

# If the env has an operating ssh-agent, bail.
if [ ! -z ${SSH_AGENT_PID+x} ] && [ ! -z ${SSH_AUTH_SOCK+x} ]
then
  check_pid_and_socket ${SSH_AGENT_PID} ${SSH_AUTH_SOCK}
  if [ $? -eq 0 ]
  then # We're good
    exit
  fi
fi

# Iterate through all pids that are ssh-agent and are owned by the current user.
# If a pair is found that checks out, print the information to be consumed.
for pid in $(ps aux | \
             awk "\$11 ~ /ssh-agent/ && \$1 ~ /`id -un`/ {print\$2}" | \
             sort -n)
do # Get the pid and find the associated agent's socket
  ssh_agent_pid=${pid}
  ssh_auth_sock=`find ${TMPDIR} -user $(id -un) -type s \
                 -name agent.$((${pid}-1)) 2>/dev/null`
  # Check to see if a file was actually found.
  if [ ! -z "${ssh_auth_sock}" ]
  then
    if check_pid_and_socket $ssh_agent_pid $ssh_auth_sock
    then
      printf "SSH_AUTH_SOCK=${ssh_auth_sock}; export SSH_AUTH_SOCK;\n"
      printf "SSH_AGENT_PID=${ssh_agent_pid}; export SSH_AGENT_PID;\n"
#      printf "echo Agent pid ${ssh_agent_pid}\n"
      exit
    fi
  fi
done

# If we landed here we must start an agent as nothing was found
ssh-agent -s
