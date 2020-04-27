#!/usr/bin/env python3
#
# This is special purpose code intended to create a Prometheus (prom) file
# for consumption by Prometheus. It is handled by the node_exporter.
#
# Usage: <script_name> <debug> <debug>
#
# Reference: https://gist.github.com/kaito834/36e693a3a54057666d28
#
# Authors: Justin Cook <jhcook@secnix.com>

import sys
import urllib.request, json

cdh_host=""
cdh_envt=""
promfile="/path/to/file.prom"
cdh_user="admin"
cdh_pass="admin"

# Python3 urllib
url = 'http://%s:7180/api/v19/clusters/%s/services' % (cdh_host, cdh_envt)
passman = urllib.request.HTTPPasswordMgrWithDefaultRealm()
passman.add_password(None, url, cdh_user, cdh_pass)
authhandler = urllib.request.HTTPBasicAuthHandler(passman)
opener = urllib.request.build_opener(authhandler)
urllib.request.install_opener(opener)

# Get the content from the URL, decode, and parse the JSON to a Python object
try:
    content = json.loads(urllib.request.urlopen(url).read().decode('utf-8'))
except urllib.error.HTTPError as err:
    sys.stderr.write(str(err))
    sys.exit(1)

# Setup a function that will write the contents as desired
gen_output = lambda x: ''.join(["{} {}\n".format(item['name'], 0
                               if item['entityStatus'] == 'GOOD_HEALTH'
                               else 1) for item in x['items']])

# If the script was called <script_name> debug debug print more information
if len(sys.argv) > 2 and sys.argv[2] == 'debug':
    for item in content['items']:
        print("%s: %s %s %s" % (item['displayName'], item['entityStatus'],
                                item['healthSummary'], item['serviceState']))
# If the script was called <script_name> debug print the content that would be
# written to file
elif len(sys.argv) > 1 and sys.argv[1] == 'debug':
    sys.stdout.write(gen_output(content))
# This writes the content desired to the specified file
else:
    try:
        with open(promfile, 'w+') as pf:
            pf.write(gen_output(content))
    except IOError as err:
        sys.stderr.write(str(err))
        sys.exit(2)
