#!/bin/bash
#
# Get a list of all IPA users an return each user's name, group membership,
# and if the user is disabled. The information is returned in a CSV.
#
# This requires an active Kerberos session with user access to the user
# database, e.g. `kinit user.name@REALM`.
#
# Author: Justin Cook

set -o errexit
set -o nounset
set -o xtrace

idm_usersfile="idm-users-and-groups-`date +%F`.txt"

lockfile="/tmp/`basename $0 | cut -f 1 -d '.'`.lock"

get_user_info() {
  user_info="`ipa user-show ${user}`"
  groups="`echo \"$user_info\" | awk -F: '$1 ~ /Member of groups/{print$2}' | \
  sed -s 's/,//g'`"
  disabled="`echo \"$user_info\" | awk -F: '$1 ~ /Account disabled/{print$2}'`"
  while :
  do
    mkdir ${lockfile} 2>/dev/null && break
    sleep 1
  done
  echo ${user},${groups},${disabled} | tee -a ${idm_usersfile}
  rmdir ${lockfile} 2>/dev/null
}

# Change ipa to return more than 100 users it does by default
# https://access.redhat.com/solutions/2856391
# This is very ugly, but necessary indeed. Upstream bugs...
IPAOUTCOME="`ipa config-mod --searchrecordslimit=1000 2>&1`" || \
awk -F: '$3 ~ /no modifications to be performed/{rc=1;print$3}; END {exit !rc}' \
<(echo $IPAOUTCOME)

# Get a list of users
users="`ipa user-find | awk -F: '$1 ~ /User login/{print$2}' | tr -d '\n'`"

# Create the file's header
echo "User,Groups,Disabled" | tee ${idm_usersfile}

counter=0
for user in ${users}
do
  ((counter++)) || /bin/true
  if [ `expr ${counter} % 10` -eq 0 ]
  then
    sleep 10
  fi
  get_user_info ${user} &
done

wait
