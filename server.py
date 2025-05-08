import socket
import threading
import time
import sys
from collections import defaultdict
import statistics


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
        
        # Start a thread to display statistics
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
    
    def handle_client(self, client_socket, addr):
        self.tuple_space.stats['total_clients'] += 1
        print(f"New client connected: {addr}")

        try:
            while True:
                # Receive message from client
                data = client_socket.recv(1024).decode()
                if not data:
                    break
                # Process the message
                msg_len = int(data[:3])
                cmd = data[3]
                content = data[4:]

                #process the request
                if cmd == 'P':  # PUT
                    key, value = content.split(' ', 1)
                    success, response = self.tuple_space.put(key, value)
                elif cmd == 'R':  # READ
                    key = content
                    success, response = self.tuple_space.read(key)
                elif cmd == 'G':  # GET
                    key = content
                    success, response = self.tuple_space.get(key)
                else:
                    response = "ERR invalid command"

                # Send response 
                response = f"{len(response):03d}{response}"
                client_socket.send(response.encode())

        except Exception as e:
            print(f"An error occurred while handling client {addr}: {e}")
        finally:
            client_socket.close()
            print(f"Client {addr} disconnected")
    def start(self):
        print(f"Server started on port {self.port}")
        try:
            while True:
                client_socket, addr = self.server_socket.accept()
                client_thread = threading.Thread(
                    target=self.handle_client,
                    args=(client_socket, addr)
                )
                client_thread.daemon = True
                client_thread.start()
        except KeyboardInterrupt:
            print("\nServer is shutting down")
        finally:
            self.server_socket.close()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("使用方法: python server.py <port>")
        sys.exit(1)
    
    try:
        port = int(sys.argv[1])
        if not (50000 <= port <= 59999):
            raise ValueError("端口号必须在50000-59999之间")
    except ValueError as e:
        print(f"错误: {e}")
        sys.exit(1)

    server = Server(port)
    server.start() 