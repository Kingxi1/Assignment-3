COMPX234-A3:Tuple Space Implementation
This is a TCP-based client/server system that implements a tuple space .
Features:
Supports PUT,READ and GET operations
Synchronized client behavior
Multi-threaded server supporting concurrent client connections
Supports string key-value pairs

Requirements:
Python 3.6 or later
Python libraries: socket, threading, time, sys

## Running Instructions

1. Start the server:
```bash
python server.py <port>
```
where port is a number between 50000-59999

2. Start the client:
```bash
python client.py <hostname> <port> <request_file>
```
Parameters:
- hostname: server hostname (use "localhost" for local testing)
- port: server port number
- request_file: path to the text file containing requests

## Testing Framework

The project includes a complete unit testing framework using Python's unittest module.

### Test File Structure
- `tests/test_server.py` - Server-side tests
- `tests/test_client.py` - Client-side tests
- `run_tests.py` - Test runner

### Running Tests
```bash
python run_tests.py
```

Test suites include:
- TestTupleSpace - Tests tuple space functionality
- TestServer - Tests server functionality
- TestClient - Tests client functionality

### Performance Testing

Ten test files are provided (client_1.txt to client_10.txt), each containing 100,000 requests.

Testing steps:
1. Start the server
2. Run all clients sequentially
3. Observe server and client outputs
4. Stop the server
5. Restart the server
6. Run all clients simultaneously
7. Observe server output

## Protocol Specification

### Request Message Format
- READ: `NNNRk`
- GET: `NNNGk`
- PUT: `NNNPkv`

where:
- NNN: total message length (3 characters)
- k: key
- v: value

### Response Message Format
- Successful read: `NNNOK(k, v) read`
- Successful delete: `NNNOK(k, v) removed`
- Successful add: `NNNOK(k, v) added`
- Key exists: `NNNERR k already exists`
- Key not found: `NNNERR k does not exist` 