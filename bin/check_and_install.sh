#!/bin/env bash
#
# This code checks a cache directory for existing files. Shall more than one file
#+exist, the code will exit nonzero. On both zero and nonzero exits, the code
#+deletes the entire contents of the cache directory.
#
# Tested on: RHEL6
#
# Author: Justin Cook <jhcook@secnix.com>

set -e
set -x

CACDIR="/opt/cloudbees_jenkins"
WRKDIR="/tmp/check_and_install_`date --iso-8601=minutes`"

# Cleanup the cache directory on exit
trap "rm -fr $CACDIR/{clientslots,clientslots-{pages,content}} ; rm -fr $WRKDIR" INT TERM EXIT

# Add /sbin to PATH
export PATH=$PATH:/sbin

BFILE="`basename ${CACDIR}/clientslots/*`"
PFILE="`basename ${CACDIR}/clientslots-pages/*`"
CFILE="`basename ${CACDIR}/clientslots-content/*`"

test -d $WRKDIR && rm -fr $WRKDIR || mkdir $WRKDIR

cd $CACDIR

if [ -e "clientslots-pages/$PFILE" ]
then
  unzip -o -q clientslots-pages/${PFILE} -d $WRKDIR >/dev/null 2>&1
  test -d /etc/default/pages && rm -fr /etc/default/pages/* || mkdir -p /etc/default/pages
  mv ${WRKDIR}/html/*.html /etc/default/pages/
fi

if [ -e "clientslots-content/$CFILE" ]
then
  unzip -o -q clientslots-content/${CFILE} -d $WRKDIR >/dev/null 2>&1
  test -d /etc/default/content/offers && rm -fr /etc/default/content/offers/* \
|| mkdir -p /etc/default/content/offers
  mv ${WRKDIR}/offers/* /etc/default/content/offers/
fi

if [ -e "clientslots/$BFILE" ] 
then
  unzip -o ${CACDIR}/clientslots/${BFILE} -d $WRKDIR >/dev/null 2>&1
  cd ${WRKDIR}/${BFILE%-dist.zip}/deploy/
  ./deploy.sh frogger
fi

