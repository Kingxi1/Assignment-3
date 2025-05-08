import unittest
import sys
import os

# Add the project root directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import test modules
from tests.test_server import TestTupleSpace, TestServer
from tests.test_client import TestClient

if __name__ == '__main__':
    # Create a test suite
    suite = unittest.TestSuite()
    
    # Add server tests
    suite.addTest(unittest.makeSuite(TestTupleSpace))
    suite.addTest(unittest.makeSuite(TestServer))
    
    # Add client tests
    suite.addTest(unittest.makeSuite(TestClient))
    
    # Run the tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Set exit code based on test result
    sys.exit(not result.wasSuccessful()) 