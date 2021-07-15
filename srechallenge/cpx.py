#!/usr/bin/env python3

import os
import sys
import argparse
from signal import signal, SIGINT
from json import loads
from urllib.request import urlopen
from time import sleep
from urllib.error import URLError
from socket import timeout
from pickle import dump

def exit_handler(sig, frame):
    """Exit on ctrl + c"""
    sys.exit(0)

class CPX():
    def __init__(self, url, servers=None, service=None):
        self.url = url
        self.servers = servers
        self.service = service

    @staticmethod
    def open_url(url):
        """Fetch a URL with a timeout of five seconds.
        
        This utility function only works with utf-8. If this character set is 
        not returned, this code will not handle the error. 
        """
        content = None
        try:
            with urlopen(url, timeout=5) as f:
                content = f.read().decode('utf-8')
        except URLError as err:
            print(err, file=sys.stderr)
            sys.exit(1)
        except timeout as err:
            print(err, file=sys.stderr)
            sys.exit(1)
        except ValueError as err:
            print(err, file=sys.stderr)
            sys.exit(1)
        return content

    def get_servers(self):
        """Get a list of servers as a Python list.
        
        This is at the discretion of the API server.
        """
        content = self.open_url("{}/servers".format(self.url))
        with open('fixtures/server.p', 'wb') as f:
            dump(content, f)
        self.servers = loads(content)

    def get_services(self, server):
        """Return the status of each server service as a Python dictionary.
        
        This is at the discretion of the API server.
        """
        content = self.open_url("{}/{}".format(self.url, server))
        with open('fixtures/service.p', 'wb') as f:
            dump(content, f)
        self.service = loads(content)

def main(cpx, command, noloop=False):
    # Should this exit on error if no servers? After all, it will be a valid
    # request if a 200 is returned.
    if not cpx.servers: exit(0)

    # 1. Print running services to stdout in tabular format
    # 2. Print out average CPU/Memory of services of the same type
    # 3. Flag services which have fewer than 2 healthy instances running
    if command == "status":
        # Iterate through all servers and track each service by name
        services = {}
        for server in cpx.servers:
            cpx.get_services(server)
            cpx.service['server'] = server
            try:
               services[cpx.service['service']].append(cpx.service)
            except KeyError:
                services[cpx.service['service']] = [cpx.service]

        print("{0:<20}{1:<10}{2:<4}{3:<6}".format('Service', 'Status', 'CPU',
                                                  'Memory'))
        print('-'*(20+10+4+6))
        for svc in services:
            cpu = [int(l['cpu'].replace('%', '')) for l in services[svc]]
            memory = [int(l['memory'].replace('%', '')) for l in services[svc]]
            resources = { 'cpu': int(sum(cpu)/len(cpu)), 
                          'memory': int(sum(memory)/len(memory))}
            print("{0:<20}{1:<10}{cpu:>3}%{memory:>5}%".format(svc, 
                        'Healthy' if len(services[svc]) > 1 else 'Unhealthy',
                        **resources))                
    
    # Track and print CPU/Memory of all instances of a given service over time
    # until the command is stopped, e.g., ctrl + c.
    elif command == "services":
        while True:
            print("{0:<16}{1:<20}{2:<4}{3:<6}".format('IP', 'Service', 'CPU',
                                                      'Memory'))
            print('-'*(16+20+4+6))
            for server in cpx.servers:
                cpx.get_services(server)
                print("{0:<16}{service:<20}{cpu:>4}{memory:>6}".format(server,
                                                                **cpx.service))
            print()
            if noloop: break
            sleep(5)
    else:
        print("unknown command: {}".format(command), file=sys.stderr)
        sys.exit(2)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("command", 
                        help="command, e.g., services, status, et al", 
                        type=str)
    parser.add_argument("url", help="the url, e.g., http://10.0.0.1:5000/", 
                        type=str)
    args = parser.parse_args()
    signal(SIGINT, exit_handler)
    cpx = CPX(args.url)
    cpx.get_servers()
    main(cpx, args.command)