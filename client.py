import socket
import sys


class Client:
    def __init__(self, hostname, port):
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

    def send(self, message):
        self.sock.sendall(message.encode())

    def receive(self):
        return self.sock.recv(1024).decode()
    
