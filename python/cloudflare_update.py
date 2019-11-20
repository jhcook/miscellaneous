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
from urllib.error import HTTPError, URLError
from ssl import create_default_context, CERT_NONE
from sys import stdout
from inspect import currentframe
import logging

# Global variables for auth, object identity, remote provider, 
# cache location, and logger.
auth_eml = ""
auth_key = ""
dns_rcrd = ""
dns_znid = ""
dns_rcid = ""
cach_dir = expanduser("~/Library/Application Support/CloudflareDNS/")
logging.basicConfig(stream=stdout, level=logging.DEBUG,
                    format="%(asctime)s:%(levelname)s:%(message)s")

def get_cache():
  """Return the last known IP address.

  Look in the local cache directory and return the IP address if found.
  If there is no cache return empty string. 
  """
  global cach_dir, dns_rcrd
  try:
    with open(cach_dir + dns_rcrd, 'r') as cache:
      return cache.read().strip()
  except IOError as err:
    logging.debug("{0}: {1}".format(currentframe().f_code.co_name, err))
    return None

def get_local():
  """Returns the IP address fetched from a specific provider.
  
  Fetch the IP address from a remote source and return as a string.  
  """
  ctx = create_default_context()
  ctx.check_hostname = False
  ctx.verify_mode = CERT_NONE
  try:
    stf = request.urlopen("https://checkip.amazonaws.com", context=ctx)
  except URLError as err:
    logging.debug("{0}: {1}".format(currentframe().f_code.co_name, err))
    return None
  return stf.read().decode("utf-8").strip()

def update_remote(ip_addr):
  """Updates Cloudflare record with ip address.

  Uses global configured information to update a specific zone record with
  the supplied ip address. 
  """
  global auth_eml, auth_key, dns_rcrd, dns_znid
  ctx = create_default_context()
  ctx.check_hostname = False
  ctx.verify_mode = CERT_NONE
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
    logging.debug("{0}: {1}".format(currentframe().f_code.co_name, err))

def update_cache(ip_addr):
  """Update the local cache with supplied IP address.

  Creates and updates the cache with the supplied IP address.
  """
  global cach_dir, dns_rcrd
  try:
    if not isdir(cach_dir):
      mkdir(cach_dir)
    with open(cach_dir + dns_rcrd, 'w') as cache:
      cache.write(ip_addr)
  except Exception as err:
    logging.debug("{0}: {1}".format(currentframe().f_code.co_name, err))

if __name__ == "__main__":
  # Look in local cache for the last known address
  known_ip_addr = get_cache()
  logging.info("cached addr: {0}".format(known_ip_addr))

  # Fetch the current local address
  ip_addr = get_local()
  logging.info("current addr: {0}".format(ip_addr))

  # If the cache and local do not match update remote and cache
  if not ip_addr:
    logging.critical("unable to retrieve IP")
  elif known_ip_addr != ip_addr:
    logging.info("updating remote")
    update_remote(ip_addr)
    logging.info("updating cache")
    update_cache(ip_addr)
  else:
    logging.info("no update")

