#!/usr/bin/env bash
#
# EFS is designed for high concurrent IO and rsync works terrible on it. So,
# this code spawns rsync for each directory in the tree.
#
# http://bruxy.regnet.cz/web/linux/EN/aws-efs-speed/
# http://arthurguru.users.sourceforge.net/blog/rsync_to_efs.html
#
# Author: Justin Cook

MAX_PROCS=100
_TMPDIR_="/tmp/$(( $BASHPID ))"

set -m

local_dir=$1
remote_dir=$2

cleanup(){
  kill 0
  rm -fr ${_TMPDIR_}
}

make_and_sync_dir(){
  _temp_="${_TMPDIR_}/$(( $BASHPID + $BASH_SUBSHELL ))"
  if [ ! -d $2 ]
  then
    mkdir -p $2
  fi
  mkdir -p ${_temp_}
  rsync -avzh \
        --numeric-ids \
        --omit-dir-times \
        --whole-file \
        --delete \
        --temp-dir=${_temp_} --exclude '/*/*/*/*/*/*/*/*/*/*' $1/ $2
  rm -fr ${_temp_}
}

child_exit(){
  (( num_firing-- ))
}

trap "cleanup" INT EXIT TERM
trap "child_exit" CHLD

# Change to the local directory and create an array of all subdirectories
cd ${local_dir}
init_array=(`find -type d \( ! -name "." \)`)

# Create an empty array and then loop through each element in the init_array
# and flip the content's location.
sorted_array=()
bot=0
top=$(( ${#init_array[@]} -1 ))

while [[ bot -lt top ]]
do
  sorted_array[$top]="${init_array[$bot]}"
  (( bot++, top-- ))
done

# Change to the remote directory and fire off a sync job
cd ${remote_dir}
num_firing=0

for dir in "${sorted_array[@]}"
do
  while true
  do
    if [ ${bot} -ge 0 ] && [ ${MAX_PROCS} -gt ${num_firing} ]
    then
      the_dir="${dir#*./}"
      make_and_sync_dir ${local_dir}/${the_dir} ${the_dir} &
      (( bot--, num_firing++ ))
      break
    else
      sleep .1
    fi
  done
done

echo "Waiting: `jobs -p`"
wait < <(jobs -p)
