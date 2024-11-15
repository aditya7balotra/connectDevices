import subprocess as sp
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
    
    
    
class cmd:
    '''
    this class is gonna handle all the task related for command line control system
    '''
    
    def __init__(self, client_socket):
        self.client_socket = client_socket
        
    def send(self):
        '''
        this method will run if the client is sending commands to the cmd in the server side
        '''
        
        while True:
            
            # taking the command
            command = input()
            
            # sending the command to the server side
            self.client_socket.send(command.encode('utf-8'))
            
            
            # getting the output and error (if any) from the server side
            output = self.client_socket.recv(1024).decode('utf-8')


            error = self.client_socket.recv(1024).decode('utf-8')

            
            print('====================== \n')
            print(f'OUTPUT: \n {output}')
            
            
            print('###################### \n')
            print(f'ERROR: \n {error}')
            
            print('====================== \n')
            
            
        return None
    
    def receive(self):
        '''
        this method will run if the client side is receiving commands from server, so the client has to run the command in the shell and return the output 
        '''
        sno = 0
        while True:
            # getting the command from the server side
            command = self.client_socket.recv(2000).decode('utf-8')
            print(f'{sno}. {command}')
            # running the command
            output = sp.run(command, shell= True, capture_output= True, text= True)
            
            # if there is no error or no proper output then it will return '', changing '' to 'None' instead
            if output.stdout == '':
                output.stdout = "None"
            if output.stderr == '':
                output.stderr = "None"
            
            # sending the output and error (if any) to the server
            
            self.client_socket.send(output.stdout.encode('utf-8')) # output
            time.sleep(.1)
            
            
            self.client_socket.send(output.stderr.encode('utf-8')) # error
            time.sleep(.1)
            sno += 1
            
        return None