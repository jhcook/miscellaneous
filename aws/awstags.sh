#!/usr/bin/env bash

for region in `aws ec2 describe-regions --all-regions --query \
  "Regions[].{Name:RegionName}" --output text` ; do
  ./awstags.py $1 ${region} $2 > $2-${region}.txt
done

find . -size 0 -exec rm {} +
