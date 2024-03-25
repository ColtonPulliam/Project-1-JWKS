import unittest
from main import MyServer, pem, expired_pem
import requests
import json
import jwt
from http.server import HTTPServer
from threading import Thread

class Server(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.server = HTTPServer(('localhost', 8080), MyServer)
        cls.server_thread = Thread(target=cls.server.serve_forever)
        cls.server_thread.daemon = True
        cls.server_thread.start()

    
    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()
        cls.server_thread.join()

    
    def test_token(self):
        url = 'http://localhost:8080/auth'
        response = requests.post(url)
        self.assertEqual(response.status_code, 200)
      
    
    def test_exptoken(self):
        url = 'http://localhost:8080/auth?expired=true'
        response = requests.post(url)
        self.assertEqual(response.status_code, 200)
     

    
    def test_jwks_endpoint(self):
        url = 'http://localhost:8080/.well-known/jwks.json'
        response = requests.get(url)
        self.assertEqual(response.status_code, 200)
     
    def test_handler(self):
        url = 'http://localhost:8080/auth'
        response = requests.put(url)
        self.assertEqual(response.status_code, 405)
        response = requests.patch(url)
        self.assertEqual(response.status_code, 405)
        response = requests.delete(url)
        self.assertEqual(response.status_code, 405)
        response = requests.head(url)
        self.assertEqual(response.status_code, 405)

    def test_failedlink(self):
        url = 'http://localhost:8080'
        response = requests.post(url)
        self.assertEqual(response.status_code, 405)
        response = requests.get(url)
        self.assertEqual(response.status_code, 405)

if __name__ == '__main__':
    unittest.main()