import socket
from features import chat
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
            
    
    