import unittest
import threading
import socket
import time
from server import TupleSpace, Server

class TestTupleSpace(unittest.TestCase):
    def setUp(self):
        self.tuple_space = TupleSpace()

    def test_put_success(self):
        success, response = self.tuple_space.put("test_key", "test_value")
        self.assertTrue(success)
        self.assertEqual(response, "OK (test_key, test_value) added")
        self.assertEqual(self.tuple_space.tuples["test_key"], "test_value")

    def test_put_duplicate(self):
        self.tuple_space.put("test_key", "test_value")
        success, response = self.tuple_space.put("test_key", "new_value")
        self.assertFalse(success)
        self.assertEqual(response, "ERR test_key already exists")
        self.assertEqual(self.tuple_space.tuples["test_key"], "test_value")

    def test_read_success(self):
        self.tuple_space.put("test_key", "test_value")
        success, response = self.tuple_space.read("test_key")
        self.assertTrue(success)
        self.assertEqual(response, "OK (test_key, test_value) read")

    def test_read_not_exists(self):
        success, response = self.tuple_space.read("nonexistent")
        self.assertFalse(success)
        self.assertEqual(response, "ERR nonexistent does not exist")

    def test_get_success(self):
        self.tuple_space.put("test_key", "test_value")
        success, response = self.tuple_space.get("test_key")
        self.assertTrue(success)
        self.assertEqual(response, "OK (test_key, test_value) removed")
        self.assertNotIn("test_key", self.tuple_space.tuples)

    def test_get_not_exists(self):
        success, response = self.tuple_space.get("nonexistent")
        self.assertFalse(success)
        self.assertEqual(response, "ERR nonexistent does not exist")

    def test_concurrent_access(self):
        def worker():
            for i in range(100):
                self.tuple_space.put(f"key_{i}", f"value_{i}")
                self.tuple_space.read(f"key_{i}")
                self.tuple_space.get(f"key_{i}")

        threads = [threading.Thread(target=worker) for _ in range(10)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        self.assertEqual(len(self.tuple_space.tuples), 0)

class TestServer(unittest.TestCase):
    def setUp(self):
        self.server = Server(51234)
        self.server_thread = threading.Thread(target=self.server.start)
        self.server_thread.daemon = True
        self.server_thread.start()
        time.sleep(1)   # Wait for the server to start

    def tearDown(self):
        self.server.server_socket.close()

    def test_client_connection(self):
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(('localhost', 51234))
        client.close()

    def test_put_operation(self):
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(('localhost', 51234))
        
        # Send PUT request
        request = "007Ptest_key test_value"
        client.send(request.encode())
        
        # Receive response
        response = client.recv(1024).decode()
        self.assertTrue(response.startswith("OK"))
        
        client.close()

    def test_read_operation(self):
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(('localhost', 51234))
        
        # PUT a value firstly
        put_request = "007Ptest_key test_value"
        client.send(put_request.encode())
        client.recv(1024)
        
        # Then READ
        read_request = "007Rtest_key"
        client.send(read_request.encode())
        response = client.recv(1024).decode()
        self.assertTrue(response.startswith("OK"))
        
        client.close()

    def test_get_operation(self):
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(('localhost', 51234))
        
        # PUT a value firstly
        put_request = "007Ptest_key test_value"
        client.send(put_request.encode())
        client.recv(1024)
        
        # Then GET
        get_request = "007Gtest_key"
        client.send(get_request.encode())
        response = client.recv(1024).decode()
        self.assertTrue(response.startswith("OK"))
        
        client.close()

if __name__ == '__main__':
    unittest.main() 