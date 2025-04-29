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
        with self.lock:
          if key in self.tuples:
              self.stats['total_errors'] += 1
              return False,"ERR {} aleady exists".format(key)
          self.tuples[key] = value
          self.stats['total_puts'] += 1
          self.stats['total_operations'] += 1
          return True,"OK ({}, {}) added".format(key,value)  

    def read(self, key):
        with self.lock:
          if key not in self.tuples:
              self.stats['total_errors'] += 1
              return False,"ERR {} not found".format(key)
          self.stats['total_reads'] += 1
          self.stats['total_operations'] += 1
          return True,"OK ({}, {})".format(key,self.tuples[key])    
        
    def get(self, key):
        with self.lock:
          if key not in self.tuples:
              self.stats['total_errors'] += 1
              return False,"ERR {} not found".format(key)
          value = self.tuples.pop(key)
          self.stats['total_gets'] += 1
          self.stats['total_operations'] += 1
          return True,"OK ({}, {})removed".format(key,value)
    

    
