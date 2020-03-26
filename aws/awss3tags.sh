#!/usr/bin/env bash
#
# Iterate through a list of S3 buckets and return tags
#
# Usage: awss3tags.sh <profile>
# Author: Justin Cook <jhcook@secnix.com>

if [ $# -lt 1 ]
then
  >&2 printf "usage: awss3tags.sh <profile>"
  exit 1
fi

case $1 in
  -h|--help)
     printf "usage: awss3tags.sh <profile>"
     exit 0
     ;;
esac

trap exit SIGINT

# Get each bucket's tags
for bucket in `aws s3api list-buckets --query "Buckets[].Name" --profile $1 \
               --output text`
do
  printf "\n***** ${bucket} *****\n" 
  aws s3api get-bucket-tagging --bucket ${bucket} --query "TagSet" --profile \
    $1 --output text
done >> $1-s3-buckets.txt 2>&1
