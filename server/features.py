import subprocess as sp
import time

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
            
class cmd:
    '''
    this class is gonna handle all the task related for command line control system
    '''
    
    def __init__(self, client_socket):
        self.client_socket = client_socket
        
    def receive(self):
        '''
        this method will run if the client side is sending commands to server, so the server has to run the command in the shell and return the output 
        '''
        sno = 0
        while True:
            # getting the command from the client side
            command = self.client_socket.recv(2000).decode('utf-8')
            print(f'{sno}. {command}')
            # running the command
            output = sp.run(command, shell= True, capture_output= True, text= True)
            
            # if there is no error or no proper output then it will return '', changing '' to 'None' instead
            if output.stdout == '':
                output.stdout = "None"
            if output.stderr == '':
                output.stderr = "None"
            
            # sending the output and error (if any) to the client
            
            self.client_socket.send(output.stdout.encode('utf-8')) # output
            time.sleep(.1)
            
            
            self.client_socket.send(output.stderr.encode('utf-8')) # error
            time.sleep(.1)
            sno += 1
            
        return None
    
    
    def send(self):
        '''
        this method will run if the server is sending commands to the cmd in the client side
        '''
        
        while True:
            
            # taking the command
            command = input()
            
            # sending the command to the client side
            self.client_socket.send(command.encode('utf-8'))
            
            
            # getting the output and error (if any) from the client side
            output = self.client_socket.recv(1024).decode('utf-8')


            error = self.client_socket.recv(1024).decode('utf-8')

            
            print('====================== \n')
            print(f'OUTPUT: \n {output}')
            
            
            print('###################### \n')
            print(f'ERROR: \n {error}')
            
            print('====================== \n')
            
            
        return None