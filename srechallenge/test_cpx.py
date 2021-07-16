import unittest
import cpx
import subprocess
from pickle import load
from json import loads
from time import sleep

class TestCpx(unittest.TestCase):
    
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
    
    @classmethod
    def setUpClass(cls):
        """Only one API server is necessary for all tests"""
        cls.subproc = subprocess.Popen(['python3', 'src/cpx_server.py', 
                                        '8080'])

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
        """Terminate the API server and wait for exit"""
        self.subproc.kill()
        self.subproc.wait()
        return super().tearDown()

if __name__ == "__main__":
    unittest.main()