#!/usr/bin/env sh
# 
# If you back up macOS over VPN, you will notice the Time Capsule cannot be
# found. This is because of Bonjour and multicast DNS. You'll need to provide 
# or gather the information and create the proxy advertisement.
#
# https://superuser.com/questions/949140/repeating-mdns-bonjour-requests-from-eth0-through-a-tunnel-tun0
# http://www.dns-sd.org/servicetypes.html
#
# Author: Justin Cook <jhcook@secnix.com>

set -o nounset
set -o errexit

usage()
{
cat << __EOF__
usage: $(basename "$0") -t <Time Capsule Name> -i <Time Capsule IP>

$(basename "$0") is used to create a proxy advertisement for SMB to a remote host

OPTIONS:
   -h      Show this message
   -i      Time Capsule IP, e.g., 192.168.0.1
   -t      Time Capsule name, e.g., TimeCapsule.local
   -v      Verbose

EXAMPLE:
$(basename "$0") -vt <hostname.tld> -i [ip address]
__EOF__
}

trap usage ERR

# A convenience function to resolve the Time Capsule hostname using DNS.
# This is a last resort as DNS may not be configured appropriately for dynamic
# address allocation. Nevertheless, hail Mary. Use Python as the more 
# convenient programmatic solution available on most platforms.
gethostbyname()
{
  python3 - <<__EOF__
from __future__ import print_function
from socket import (gethostbyname, gaierror)
from sys import stderr
try:
  print(gethostbyname("${TIMECAPSULE_NAME}.${TIMECAPSULE_TLD}"))
except gaierror as err:
  print(err, file=stderr)
__EOF__
}

# Necessary values
TIMECAPSULE_NAME=""
TIMECAPSULE_IP=""

while getopts "hi:t:v" OPTION
do
  case $OPTION in
    h)
      usage
      exit 0
      ;;
    i)
      TIMECAPSULE_IP="${OPTARG}"
      ;;
    t) # read -a is not POSIX. I'm terribly sorry.
      IFS='.' read -r -a TIMECAPSULE_INFO <<< "${OPTARG}"
      TIMECAPSULE_NAME="${TIMECAPSULE_INFO[0]}"
      TIMECAPSULE_TLD="${TIMECAPSULE_INFO[1]:=local}"
      ;;
    v)
      set -o xtrace
      ;;
    ?)
      usage
      exit 1
      ;;
  esac
done

if [ -z "${TIMECAPSULE_NAME}" ] || [ -z "${TIMECAPSULE_IP:=$(gethostbyname)}" ]
then
  usage
  exit 1
fi

# $ dns-sd -Z _smb._tcp
# Browsing for _smb._tcp
# DATE: ---Thu 12 Aug 2021---
# 15:14:25.561  ...STARTING...

# ; To direct clients to browse a different domain, substitute that domain in
# place of '@'
# lb._dns-sd._udp                                 PTR     @

# ; In the list of services below, the SRV records will typically reference
# dot-local Multicast DNS names.
# ; When transferring this zone file data to your unicast DNS server, you'll 
# need to replace those dot-local
# ; names with the correct fully-qualified (unicast) domain name of the target
# host offering the service.

# _smb._tcp                                       PTR     TimeCapsule._smb._tcp
# TimeCapsule._smb._tcp                   SRV     0 0 445 TimeCapsule.local.
# ; Replace with unicast FQDN of target host
# TimeCapsule._smb._tcp                   TXT     “”
# ...

# Create the relevant proxy advertisement on the host attached to VPN.

dns-sd -P "${TIMECAPSULE_NAME}" '_smb._tcp' "${TIMECAPSULE_TLD}." \
  445 \
  "${TIMECAPSULE_NAME}.${TIMECAPSULE_TLD}" \
  "${TIMECAPSULE_IP}"

# /usr/bin/tmutil startbackup
