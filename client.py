import socket
import sys


class Client:
    def __init__(self, hostname, port):
        self.host = hostname
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.host, self.port))

    def send(self, message):
        self.sock.sendall(message.encode())

    def receive(self):
        return self.sock.recv(1024).decode()
    
