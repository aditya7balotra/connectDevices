import socket
from features import chat, share
import threading

class client:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
    def connect(self):
        print('=====')
        print(f'connecting to {self.ip}/{self.port}')
        self.client_socket.connect((self.ip, self.port))
        print('connection successfull')
        print('=====')
        print(self.client_socket.recv(1024).decode('utf-8'))
        print('\n')
        return self.client_socket
    
    def select_feature(self , featureName):
        '''
        featureName
        => chat: chatting with the server end
        '''
        
        # sending the feature name to the server
        self.client_socket.send(featureName.encode('utf-8'))
        
        if featureName == 'chat':
            chat_obj = chat('CLIENT', self.client_socket)
            
            chat_send_th = threading.Thread(target = chat_obj.send)
            chat_recv_th = threading.Thread(target = chat_obj.receive)
            chat_send_th.start()
            chat_recv_th.start()
            # msg1 = input('Your first message: ')
            # print(chat_obj.send())
        elif featureName == 'share':
            share_obj = share(self.client_socket)
            share_type = input('Enter your share type (send or recv): ')
            # sending to the server share_type
            self.client_socket.send(share_type.encode('utf-8'))
            
            if share_type == 'recv':
                share_obj.receive()
            elif share_type == 'send':
                dire = input('Enter directory with / slashes: ')
                send_obj = share_obj.send(dire)
            
    
    