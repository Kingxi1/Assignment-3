import socket
import sys


class Client:
    def __init__(self, hostname, port, request_file):
        """Initialize the client with server details and request file"""
        self.host = hostname
        self.port = port
        self.request_file = request_file
        self.socket = None    # Will hold the socket connection
    
    def connect(self):                    # Connect to the server
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect((self.host, self.port))
            print(f"Connected to server {self.hostname}:{self.port}")
        except Exception as e:
            print(f"Failed to connect to server: {e}")
            sys.exit(1)
    
    def _format_request(self, request):
        try:
            # construct the request message
            if request.startswith("PUT"):
                _, key, value = request.split(" ", 2)
                msg = f"P{key} {value}"
            elif request.startswith("READ"):
                _, key = request.split(" ", 1)
                msg = f"R{key}"
            elif request.startswith("GET"):
                _, key = request.split(" ", 1)
                msg = f"G{key}"
            else:
                print(f"Invalid request: {request}")
                return None

            # Validate message size
            if len(msg) > 999:
                print(f"Request message too long: {request}")
                return None

            # Add length prefix 
            return f"{len(msg):03d}{msg}"

        except Exception as e:
            print(f"Error formatting request: {e}")
            return None

    def send_request(self, request):
        """Send a formatted request to the server and handle response"""
        try:
            msg = self._format_request(request)
            if not msg:
                return False

            # send the request
            self.socket.send(msg.encode())

            # receive the response
            response = self.socket.recv(1024).decode()
            if not response:
                print("Server closed the connection")
                return False

            # parse the response
            msg_len = int(response[:3])
            response_content = response[3:]

            # check if the response is valid
            if len(response_content) == msg_len:
                print(f"{request}: {response_content}")
                return True

            else:
                print(f"Invalid response: {response}")
                return False

        except Exception as e:
            print(f"Error processing request: {e}")
            return False
    
    def process_file(self):
        """Process requests from the input file"""
        try:
            with open(self.request_file, 'r') as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    
                    # Validate key-value size for PUT commands
                    if line.startswith("PUT"):
                        _, key, value = line.split(" ", 2)
                        if len(key) + len(value) > 970:
                            print(f"Key-value pair too large: {line}")
                            continue
                    
                    if not self.send_request(line):
                        break

        except FileNotFoundError:
            print(f"Request file not found: {self.request_file}")
        except Exception as e:
            print(f"Error processing file: {e}")
        finally:
            if self.socket:
                self.socket.close()

