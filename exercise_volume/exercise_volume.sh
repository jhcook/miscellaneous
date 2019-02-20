#!/usr/bin/env bash
#
# This code loops indefinitely and writes a 1 GiB file, syncs to disk, and
# sleeps for 30 seconds unless configured otherwise.
#
# Tested on: macOS 10.14
#
# Author: Justin Cook <jhcook@secnix.com>

set -o errexit
set -o nounset
set -o pipefail
#set -o xtrace

##### User-defined variables #####

__TMPFILE="/tmp/bollocks"
__SLEEPTM=30

##### End user-defined variables #####

###############################################################################
# This gets called when the script exits. It cleans up artefacts that do not
# need to be left behind. 
# Globals:
#   __TMPFILE 
# Arguments:
#   1: a string representing signal caught, e.g. SIGINT
# Returns:
#   None
###############################################################################
cleanup () {
  rm -f ${__TMPFILE}
  logger -is -t exercise_volume "exiting on ${1}"
  exit 0
}

###############################################################################
# It is intended to call this function immediately after invocation to setup
# the environment including trapping catchable signals. 
# Globals:
#   BASH_VERSION: inherited from the environment
# Arguments:
#
# Returns:
#
###############################################################################
setup_env () {
  # Get the Bash version, setup signal code data structure, and then trap 
  # signals that will be disruptive.
  if [ "${BASH_VERSION%%.*}" -gt 3 ]
  # Bash >= 4 (has dictionaries)
  then
    declare -A _signals_=( \
      [1]="SIGHUP" \
      [2]="SIGINT" \
      [3]="SIGQUIT" \
      [6]="SIGABRT" \
      [9]="SIGKILL" \
      [14]="SIGALRM" \
      [15]="SIGTERM" )
    for i in 1 2 3 6 9 14 15
    do
      local sig="${_signals_[${i}]}"
      trap "cleanup ${sig}" "${sig}"
    done
  elif [ "${BASH_VERSION%%.*}" -eq 3 ]
  #Bash 3
  then
    SIG1="HUP"
    SIG2="INT"
    SIG3="QUIT"
    SIG6="ABRT"
    SIG9="KILL"
    SIG14="ALRM"
    SIG15="TERM"
    for i in 1 2 3 6 9 14 15
    do
      local sig=SIG${i}
      trap "cleanup SIG${!sig}" "${!sig}"
    done
  else
    printf "Unsupported shell version. We'll give it our best shot.\n"
  fi
}

###############################################################################
# Loop forever writing 0/1/01s to disk, sync, sleep, and repeat.
# Globals:
#   __TMPFILE
#   __SLEEPTM
# Arguments:
#   None
# Returns:
#   None
###############################################################################
exercise_volume () {
  declare -i __counter=0
  while true
  do 
    printf "Writing ${__counter} to ${__TMPFILE}\n"
    local __cmd="cat /dev/zero"
    case ${__counter} in
      0)
        ((__counter++))
        ;;
      1)
        which perl 2>&1 >/dev/null
        local __perl="$?"
        which python3 2>&1 >/dev/null
        local __python3="$?"
        if [ "${__perl}" -eq 0 ]; then # Fastest
          __cmd="perl -e 'print chr(0xFF)x512 while(1);' 2>/dev/null"
        elif [ "${__python3}" -eq 0 ]; then # Fast
          __cmd="python3 -c \"while True: print([b'\xFF']*512, end='')\" 2>/dev/null"
        else # Fast enough
          __cmd="tr '\0' '\377' < /dev/zero"
        fi
        ((__counter++))
        ;;
      2)
        __cmd="cat /dev/urandom"
        __counter=0
        ;;
    esac
    __cout="`eval ${__cmd} | dd of=${__TMPFILE} bs=512 count=2097152 2>&1 || /usr/bin/true`"
    logger -i -t exercise_volume "${__cout}"
    printf "Syncing disk\n"
    sync
    local secs=${__SLEEPTM}
    while [ ${secs} -gt 0 ]
    do
      printf "Sleep $secs\033[0K\r"
      sleep 1
      ((secs--))
    done
  done
}

main () {
  export LANG=C
  setup_env
  exercise_volume
}

main
