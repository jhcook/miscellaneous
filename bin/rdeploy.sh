#!/bin/env bash
#
# This code checks a cache directory for existing files. Shall more than one file
#+exist, the code will exit nonzero. On both zero and nonzero exits, the code
#+deletes the entire contents of the cache directory. Shall a file exist, it 
#+copies the file to each remote hosts and executes remote code to deploy.
#
# Tested on: RHEL6
#
# Author: Justin Cook <jhcook@secnix.com>

set -e
set -x

WHOSTS=( ssh.frogger.clientgaming.com ssh.centipede.clientgaming.com )
CACDIR="/opt/cloudbees_jenkins"

# Cleanup the cache directory on exit
trap "rm -fr $CACDIR/{clientslots,clientslots-{pages,content}}" INT TERM EXIT

BFILE="`basename ${CACDIR}/clientslots/*`"
PFILE="`basename ${CACDIR}/clientslots-pages/*`"
CFILE="`basename ${CACDIR}/clientslots-content/*`"

cd $CACDIR

for host in ${WHOSTS[@]}
do
  ssh -i ~/.ssh/cloudbees_jenkins $host "cd $CACDIR ;" \
    'for d in {clientslots,clientslots-pages,clientslots-content} ;' \
    'do [ -e $d ] && /bin/true || mkdir $d ; done'
  if [ -e "clientslots/$BFILE" ]
  then
    scp -o "StrictHostKeyChecking no" -o "CheckHostIP no" -i ~/.ssh/cloudbees_jenkins \
clientslots/$BFILE ${host}:/opt/cloudbees_jenkins/clientslots/
  fi
  if [ -e "clientslots-pages/$PFILE" ]
  then
    scp -o "StrictHostKeyChecking no" -o "CheckHostIP no" -i ~/.ssh/cloudbees_jenkins \
clientslots-pages/$PFILE ${host}:/opt/cloudbees_jenkins/clientslots-pages/
  fi
  if [ -e "clientslots-content/$CFILE" ]
  then
    scp -o "StrictHostKeyChecking no" -o "CheckHostIP no" -i ~/.ssh/cloudbees_jenkins \
clientslots-content/$CFILE ${host}:/opt/cloudbees_jenkins/clientslots-content/
  fi
  ssh -tt -o "StrictHostKeyChecking no" -o "CheckHostIP no" -i ~/.ssh/cloudbees_jenkins \
  root@${host} '/root/bin/check_and_install.sh'
done

