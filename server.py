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
        
        
        """
         Calculate and return statistics about the tuple space.
         Returns:
        dict: A dictionary containing the following statistics:
            - tuple_count: Number of tuples in the space
            - avg_tuple_size: Average size of tuples (key + value)
            - avg_key_size: Average size of keys
            - avg_value_size: Average size of values
            - total_clients: Total number of connected clients
            - total_operations: Total number of operations performed
            - total_reads: Total number of READ operations
            - total_gets: Total number of GET operations
            - total_puts: Total number of PUT operations
            - total_errors: Total number of errors encountered
        """
      
    def get_stats(self):
        with self.lock:    # Ensure thread safety
          # If tuple space is empty, return zero statistics
          if not self.tuples:
             return {
                'tuple_count': 0,
                'avg_tuple_size': 0,
                'avg_key_size':0,
                'avg_value_size':0,
                **self.stats     # Include other statistics
             }
          key_sizes = [len(k) for k in self.tuples.keys()]
          value_sizes = [len(v) for v in self.tuples.values()]
          tuple_sizes = [k + v  for k, v in zip(key_sizes,value_sizes)]
          return {
                'tuple_count': len(self.tuples),
                'avg_tuple_size': sum(tuple_sizes) / len(tuple_sizes),
                'avg_key_size': sum(key_sizes) / len(key_sizes),
                'avg_value_size': sum(value_sizes) / len(value_sizes),
                **self.stats
          }

class Server:
    def __init__(self, port):
        self.tuples_space = TupleSpace()
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind(('localhost', self.port))
        self.server_socket.listen(5)
        
        # 启动统计信息显示线程
        self.stats_thread = threading.Thread(target=self.display_stats)
        self.stats_thread.daemon = True
        self.stats_thread.start()

        def display_stats(self):
            while True:
                time.sleep(10)                                 # Display stats every 10 seconds
                stats = self.tuples_space.get_stats()
                print("\n=== Server Statistics ===")
                print(f"Tuple count: {stats['tuple_count']}")
                print(f"Average tuple size: {stats['avg_tuple_size']:.2f}")
                print(f"Average key size: {stats['avg_key_size']:.2f}")
                print(f"Average value size: {stats['avg_value_size']:.2f}")
                print(f"Total clients: {stats['total_clients']}")
                print(f"Total operations: {stats['total_operations']}")
                print(f"READ operations: {stats['total_reads']}")
                print(f"GET operations: {stats['total_gets']}")
                print(f"PUT operations: {stats['total_puts']}")
                print(f"Total errors: {stats['total_errors']}")
                print("=======================\n")

    