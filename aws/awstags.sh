#!/usr/bin/env bash
#
# A wrapper for awstags.py to inspect all regions and output to files
#
# Usage: $ ./awstags.sh <tag names> <profile>
# Author: Justin Cook <jhcook@secnix.com>

case $1 in
  -h|--help)
    printf "Usage: awstags.sh <tag names> <profile>\n"
    exit 0
    ;;
esac

if [ $# -lt 2 ]
then
  >&2 printf "Usage: awstags.sh <tag names> <profile>\n"
  exit 1
fi

for region in `aws ec2 describe-regions --all-regions --query \
  "Regions[].{Name:RegionName}" --output text` ; do
  ./awstags.py $1 ${region} $2 > $2-${region}.txt
done

find . -size 0 -exec rm {} +
