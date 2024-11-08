import socket
from features import chat, share
import threading

class server:
    def __init__(self, ip, port, listen = 1):
        self.ip = ip
        self.port = port
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((ip, port))
        self.server.listen(listen)
    
    def search(self):
        print('==========')
        print('looking for connections....')
        self.client , self.client_adrs = self.server.accept()
        
        print(f'server connected to : {self.client_adrs}')
        
        print('==========', end='\n')
        
        init_msg = '''
        WELCOME!
        Here we provide different features: chat, control, video etc
        '''
        self.client.send(init_msg.encode('utf-8'))
        
        return self.client
    
    def recvFeature(self):
        feature = self.client.recv(1024).decode('utf-8')
        
        if feature == 'chat':
            chat_obj = chat('SERVER', self.client)
            
            
            chat_send_th = threading.Thread(target=chat_obj.send)
            chat_recv_th = threading.Thread(target = chat_obj.receive)
            chat_send_th.start()
            chat_recv_th.start()
            
            # rcv1 = chat_obj.receive()
            
            # print(f'{chat_obj.name}: {rcv1}')
        elif feature == 'share':
            share_obj = share(self.client)
            # receiving the share type
            share_type = self.client.recv(10).decode('utf-8')
            
            
            if share_type == 'recv':
                # means the client is receiving and the server has to send something
                dire = input('Enter directory with / slashes: ')
                send_obj = share_obj.send(dire)
            elif share_type == 'send':
                # means the client is sending and the server has to receive something
                share_obj.receive()
    