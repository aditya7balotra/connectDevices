
import os
import math
import time

class chat:
    def __init__(self, name, client_socket):
        self.name = name
        
        self.client_socket = client_socket
        # sending name to the server
        client_socket.send(name.encode('utf-8'))
        
        # receiving name from the server
        self.server_name = client_socket.recv(1024).decode('utf-8')
        
        
    def send(self):
        while True:
            message = input()
            self.client_socket.send(message.encode('utf-8'))
            print(f'{self.name}: {message}')
        
    def receive(self):
        while True:
            msg = self.client_socket.recv(2000).decode('utf-8')
            print(f'{self.server_name}: {msg}')
    
    
class share:
    
    '''
    this feature allows the sharing of files between two sockets
    '''
    def __init__(self, client_socket):
        self.client_socket = client_socket
        
        
    def receive(self):
        '''
        this is going to receive files
        '''
        
        print('receiving...')
        # receiving the name of the file
        file_name = self.client_socket.recv(2000).decode('utf-8')
    
        # receiving the total_size of the sharing file
        file_size = int(self.client_socket.recv(10).decode('utf-8'))
        
        chunk_size = 1024
        total_iterations = math.ceil(file_size/chunk_size)
        data = b''
        # receiving the chunks
        dwnld = 0
        for i in range(total_iterations):
            if (dwnld + 1024) >= file_size:
                dwnld = file_size
            else:
                dwnld += 1024
                
            
            content = self.client_socket.recv(1025)
            print(f'receiving...{round((dwnld / file_size) * 100)} % \r', end= '')
            data += content
        print('\n')
        
        # writing the file
        with open(file_name, 'wb') as file:
            file.write(data)
            
    def send(self, file_directory):
        '''
        file_directory: location of the file to send
        '''
        print('sending...')
        chunk_size = 1024
        # fetching the name of the file
        file_name = file_directory.split('/')[-1]
        
        
        # reading the file
        with open(file_directory , 'rb') as file:
            content = file.read()
        # sending file name
        self.client_socket.send(file_name.encode('utf-8'))
        time.sleep(1)
        # sending the total size of the file
        self.client_socket.send(str(len(content)).encode('utf-8'))
        time.sleep(1)
        # print(str(len(content)).encode('utf-8'))
        # sending chunks with iteration
        for i in range(0, len(content), chunk_size):
            self.client_socket.send(content[i : i + chunk_size])
            
            print(f'sending...{round(len(content[: i + chunk_size]) / len(content) * 100)} %\r', end='')
            time.sleep(.5)
        print('\n')
        print('Send successfull')
        
        return 'success'
        
    