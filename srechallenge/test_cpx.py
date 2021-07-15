import unittest
import cpx
import subprocess
from pickle import load
from json import loads
from time import sleep

class TestCpx(unittest.TestCase):
    
    def setUp(self) -> None:
        with open('fixtures/test_servers.p', 'rb') as srv, \
             open('fixtures/test_service.p', 'rb') as svc:
            self.app = cpx.CPX(url='http://localhost:8080', 
                              servers=loads(load(srv)),
                              service=loads(load(svc)))
        return super().setUp()
    
    @classmethod
    def setUpClass(cls):
        cls.subproc = subprocess.Popen(['python3', 'src/cpx_server.py', 
                                        '8080'])

    def test_get_servers(self):
        self.assertIsInstance(self.app.servers, list)

    def test_get_status(self):
        self.assertIsInstance(self.app.service, dict)

    def test_main_status(self):
        cpx.main(self.app, "status")

    def test_main_services(self):
        cpx.main(self.app, "services", noloop=True)
    
    def tearDown(self) -> None:
        self.subproc.kill()
        self.subproc.wait()
        return super().tearDown()

if __name__ == "__main__":
    unittest.main()