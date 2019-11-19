#!/usr/bin/env python3
# Update this computer's public address with the associated name
# in Cloudflare's DNS management for specified domain.
#
# Requires: Python3
# Tested: macOS Catalina
# Author: Justin Cook <jhcook@secnix.com>

from urllib import request
from os.path import expanduser, isdir
from os import mkdir
from json import dumps
from urllib.error import HTTPError
import ssl

# Global variables for auth, object identity, remote provider,
# and cache location
auth_eml = ""
auth_key = ""
dns_rcrd = ""
dns_znid = ""
dns_rcid = ""
rem_prov = "https://checkip.amazonaws.com"
cach_dir = expanduser("~/Library/Application Support/CloudflareDNS/")

def get_cache():
  """Return the last known IP address.

  Look in the local cache directory and return the IP address if found.
  If there is no cache return empty string.
  """
  global cach_dir, dns_rcrd
  try:
    with open(cach_dir + dns_rcrd, 'r') as cache:
      return cache.read().strip()
  except IOError:
    return ''

def get_local():
  """Returns the IP address fetched from a specific provider.

  Fetch the IP address from a remote source and return as a string.
  """
  ctx = ssl.create_default_context()
  ctx.check_hostname = False
  ctx.verify_mode = ssl.CERT_NONE
  try:
    stf = request.urlopen(rem_prov, context=ctx)
  except urllib.error.URLError as err:
    return err
  return stf.read().decode("utf-8").strip()

def update_remote(ip_addr):
  """Updates Cloudflare record with ip address.

  Uses global configured information to update a specific zone record with
  the supplied ip address.
  """
  global auth_eml, auth_key, dns_rcrd, dns_znid
  ctx = ssl.create_default_context()
  ctx.check_hostname = False
  ctx.verify_mode = ssl.CERT_NONE
  data = dumps({ "type": "A",
                 "name": "{}".format(dns_rcrd),
                 "content": "{}".format(ip_addr),
                 "ttl": 300,
                 "proxied": False }).encode('utf-8')
  try:
    url = "https://api.cloudflare.com/client/v4/zones/{}/dns_records/{}"
    req = request.Request(url=url.format(dns_znid, dns_rcid), method='PUT')
    req.add_header("X-Auth-Email", "{}".format(auth_eml))
    req.add_header("X-Auth-Key", "{}".format(auth_key))
    req.add_header("Content-Type", "application/json")
    request.urlopen(req, data=data, context=ctx)
  except HTTPError as err:
    print(err)

def update_cache(ip_addr):
  """Update the local cache with supplied IP address.

  Creates and updates the cache with the supplied IP address.
  """
  global cach_dir, dns_rcrd
  if not isdir(cach_dir):
    mkdir(cach_dir)
  try:
    with open(cach_dir + dns_rcrd, 'w') as cache:
      cache.write(ip_addr)
  except IOError as err:
    print(err)

if __name__ == "__main__":
  # Look in local cache for the last known address
  known_ip_addr = get_cache()

  # Fetch the current local address
  ip_addr = get_local()

  # If the cache and local do not match update remote and cache
  if known_ip_addr != ip_addr:
    update_remote(ip_addr)
    update_cache(ip_addr)
