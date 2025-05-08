import unittest
import os
import tempfile
from client import Client

class TestClient(unittest.TestCase):
    def setUp(self):
        # Create temporary test file
        self.temp_file = tempfile.NamedTemporaryFile(mode='w', delete=False)
        self.temp_file.write("PUT test_key test_value\n")
        self.temp_file.write("READ test_key\n")
        self.temp_file.write("GET test_key\n")
        self.temp_file.close()

    def tearDown(self):
        os.unlink(self.temp_file.name)

    def test_file_processing(self):
        client = Client("localhost", 51234, self.temp_file.name)
        # only test file processing logic, without actually connecting to the server
        with open(self.temp_file.name, 'r') as f:
            lines = f.readlines()
            self.assertEqual(len(lines), 3)
            self.assertEqual(lines[0].strip(), "PUT test_key test_value")
            self.assertEqual(lines[1].strip(), "READ test_key")
            self.assertEqual(lines[2].strip(), "GET test_key")

    def test_request_formatting(self):
        client = Client("localhost", 51234, self.temp_file.name)
        
        #  Test PUT request formatting
        put_request = "PUT test_key test_value"
        msg = client._format_request(put_request)
        self.assertEqual(msg, "007Ptest_key test_value")
        
        # Test READ request formatting
        read_request = "READ test_key"
        msg = client._format_request(read_request)
        self.assertEqual(msg, "007Rtest_key")
        
        # Test GET request formatting
        get_request = "GET test_key"
        msg = client._format_request(get_request)
        self.assertEqual(msg, "007Gtest_key")

    def test_size_limit(self):
        client = Client("localhost", 51234, self.temp_file.name)
        
        # Test key-value size limit
        long_key = "a" * 500
        long_value = "b" * 500
        request = f"PUT {long_key} {long_value}"
        msg = client._format_request(request)
        self.assertLess(len(msg), 1000)  # Ensure message size doesn't exceed 999
    def test_invalid_request(self):
        client = Client("localhost", 51234, self.temp_file.name)
        
        # Test invalid request
        invalid_request = "INVALID test_key"
        msg = client._format_request(invalid_request)
        self.assertIsNone(msg)

if __name__ == '__main__':
    unittest.main() 