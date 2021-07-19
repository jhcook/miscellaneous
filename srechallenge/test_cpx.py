#!/usr/bin/env python3
# Run unit tests for cpx.py
#
# Usage: $ python3 -m unittest discover -s .
#
# Author: Justin Cook <jhcook@secnix.com>

import unittest
import cpx
from subprocess import Popen
from socket import create_connection
from pickle import load
from json import loads
from time import perf_counter, sleep

class TestCpx(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls) -> None:
        cls.subproc = Popen(['python3', 'src/cpx_server.py', '8080'])
        start_time = perf_counter()
        timeout = 1
        while True:
            try:
                with create_connection(('localhost', 8080), timeout):
                    break
            except OSError as err:
                if perf_counter() - start_time >= timeout:
                    raise TimeoutError("setUpClass: timed out after {}".format(timeout))
                sleep(0.01)
        return super().setUpClass()

    def setUp(self) -> None:
        """Setup the app for each test.
        
        This seeds the servers and service with data to create an existing
        session.
        """
        with open('fixtures/test_servers.p', 'rb') as srv, \
             open('fixtures/test_service.p', 'rb') as svc:
            self.app = cpx.CPX(url='http://localhost:8080', 
                              servers=loads(load(srv)),
                              service=loads(load(svc)))
        return super().setUp()

    def test_get_servers(self):
        """Checks to see if servers is an instance of a list
        
        Since we seed the variable with data, this proves the
        data is loaded successfully.
        """
        self.assertIsInstance(self.app.servers, list)

    def test_get_status(self):
        """Checks to see if service is an instance of a dict
        
        Since we seed the variable with data, this proves the
        data is loaded successfully.
        """
        self.assertIsInstance(self.app.service, dict)

    def test_main_status(self):
        """Checks to see if status in main successfully executes"""
        cpx.main(self.app, "status")

    def test_main_services(self):
        """Checks to see if services in main successfully executes"""
        cpx.main(self.app, "services", noloop=True)
    
    def tearDown(self) -> None:
        return super().tearDown()
    
    @classmethod
    def tearDownClass(cls) -> None:
        """Terminate the API server and wait for exit"""
        cls.subproc.kill()
        cls.subproc.wait()        
        return super().tearDownClass()
    
if __name__ == "__main__":
    unittest.main()