#!/usr/bin/env python3

import argparse
import hashlib
import json
import random
import re
import socket
from typing import Dict
from http.server import HTTPServer, SimpleHTTPRequestHandler

NUM_SERVERS = 150
SERVER_SET = set(['10.58.1.%d' % i for i in range(1, NUM_SERVERS + 1)])
IP_REGEX = r'/10\.58\.1\.[0-9]{1,3}$'
SERVICES = [
    'PermissionsService',
    'AuthService',
    'MLService',
    'StorageService',
    'TimeService',
    'GeoService',
    'TicketService',
    'RoleService',
    'IdService',
    'UserService',
    'RoleService',
]


def _server_stats(ip: str) -> Dict[str, str]:
    ip_u = ip.encode('utf-8')
    service_idx = int(hashlib.md5(ip_u).hexdigest(), 16) % len(SERVICES)
    service_name = SERVICES[service_idx]
    return {
        'cpu': '%d%%' % random.randint(0, 100),
        'memory': '%d%%' % random.randint(0, 100),
        'service': service_name
    }


class HTTPServerV6(HTTPServer):
    address_family = socket.AF_INET6


class CPXHandler(SimpleHTTPRequestHandler):
    def _invalid_endpoint(self):
        self.send_response(400)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(bytes(json.dumps({'error': 'Invalid IP'}), 'utf-8'))

    def _json(self, data: str):
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(bytes(json.dumps(data), 'utf-8'))

    def do_GET(self):
        ip_match = re.match(IP_REGEX, self.path)
        if self.path == '/servers':
            self._json(list(SERVER_SET))
        elif ip_match:
            ip = ip_match.group().replace('/', '')
            if ip not in SERVER_SET:
                self._invalid_endpoint()
            else:
                self._json(_server_stats(ip))
        else:
            self._invalid_endpoint()


def main(port: int, protocol: int):
    if protocol == 6 and not socket.has_ipv6:
        print("Falling back to IPv4")

    if protocol == 6 and socket.has_ipv6:
        httpd = HTTPServerV6(('::', port), CPXHandler)
        httpd.serve_forever()

    else:
        httpd = HTTPServer(('0.0.0.0', port), CPXHandler)
        httpd.serve_forever()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("port", help="the port on which to run", type=int)
    parser.add_argument("--protocol", help="which IP version to use, 4 for IPv4, 6 for IPv6",
                        type=int, choices=[4, 6], default=6)
    args = parser.parse_args()

    main(args.port, args.protocol)
