

class chat:
    def __init__(self, name, client_socket):
        self.name = name
        
        # receiving name from the client
        self.client_name = client_socket.recv(1024).decode('utf-8')
        self.client_socket = client_socket
        # sending name to the client
        client_socket.send(name.encode('utf-8'))
        
    def send(self):
        while True:
            message = input()
            self.client_socket.send(message.encode('utf-8'))
            
            print(f'{self.name} : {message}')
    
    def receive(self):
        while True:
            msg = self.client_socket.recv(2000).decode('utf-8')
            print(f'{self.client_name}: {msg}')