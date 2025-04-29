import socket
import threading
import time
import sys


class TupleSpace:
    def __init__(self):
        self.lock = threading.Lock()        # thread synchronization
        self.tuples = {}      # Store key-value pairs
        self.stats = {
            'total_clients': 0,
            'total_operations': 0,
            'total_puts': 0,
            'total_gets': 0,
            'total_reads': 0,
            'total_errors': 0
        }

    def put(self, key, value):
