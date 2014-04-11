#!/usr/bin/env python3.3
"""Fetch the current Olympic medal count alloted to each country by gold,
silver and bronze. Then, apply weight calculation and sort by total. The entry
with the greatest total should return as first place followed by sorting total.
In event of a tie in weight, sort by total number of medals.
"""

from sys import exit
from urllib import request
from urllib.error import HTTPError
import json

# Thanks Will
# http://www.clearlytech.com/2014/02/08/building-simple-olympic-medals-api/
__url__ = "http://olympics.clearlytech.com/api/v1/medals/"
__author__ = "Justin Cook <jhcook@gmail.com>"

req = request.Request(__url__)

try:
    cnt = json.loads(request.urlopen(req).read(18192).decode('utf-8'))
except HTTPError as e:
    print(e)
    exit(1)

cdict = {cntry['country_name']: (3*int(cntry['gold_count']) +
                                 2*int(cntry['silver_count']) +
                                   int(cntry['bronze_count']),
                                 int(cntry['medal_count'])) for cntry in cnt}

sc = sorted(cdict.keys(), key=lambda x: cdict[x], reverse=True)

for i in range(10):
    print('{0: >2} {1: <13} {2}'.format(i+1, sc[i], cdict[sc[i]]))

