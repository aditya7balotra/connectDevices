# from run import client_socket
import math, time, os, zipfile
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
    
    
    
class share_all_photos:
    '''
    this class does the word of sharing all the photos from one device to another
    '''
    def __init__(self, client_socket) -> None:
        self.client_socket = client_socket
        
    def receive(self):
        '''
        this is going to receive files
        '''
        
        print('receiving...')
        # receiving the name of the file
        file_name = 'rPictures.zip'
    
        # receiving the total_size of the sharing file
        file_size = int(self.client_socket.recv(2000).decode('utf-8'))
        
        chunk_size = 5000
        # total_iterations = math.ceil(file_size/chunk_size)
        data = b''
        # receiving the chunks
        dwnld = 0
        while True:
            
            content = self.client_socket.recv(5100)
            if len(content) > 0:
                if (dwnld + chunk_size) >= file_size:
                    dwnld = file_size
                else:
                    dwnld += chunk_size
                    
                
                
                print(f'receiving...{round((dwnld / file_size) * 100)} % \r', end= '')
                data += content
            else:
                break
            
            
        print('\n')
        
        # writing the file
        with open(file_name, 'wb') as file:
            file.write(data)
            
    @staticmethod
    def zip_folder(folder_path, output_zip_path):
        # Create a new zip file (output_zip_path), open it in write mode
        with zipfile.ZipFile(output_zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            # Walk through each file and folder within the folder_path
            for root, dirs, files in os.walk(folder_path):
                for file in files:
                    # Get the full path to the file
                    file_path = os.path.join(root, file)
                    
                    # Add the file to the zip archive, keeping its relative path
                    zipf.write(file_path, 
                            arcname=os.path.relpath(file_path, folder_path))

    def send(self, images_directory):
        '''
        images_directory: location of the images
        '''
        print('sending...')
        chunk_size = 5000
        
        # creating the zip file
        self.zip_folder(images_directory, images_directory + '.zip')
        
        # reading the zip folder
        with open(images_directory + '.zip', 'rb') as file:
            content = file.read()
            
        # seding the size of the data
        self.client_socket.send(str(len(content)).encode('utf-8'))
        time.sleep(.5)
        dwnld = 0
        # sending the zip file
        for i in range(0, len(content), chunk_size):
            if (dwnld + chunk_size) >= len(content):
                dwnld = len(content)
            else:
                dwnld += chunk_size
            
            self.client_socket.send(content[i : i + chunk_size])
            print(f'sending...{round((dwnld / len(content) * 100))} % \r', end= '')
            time.sleep(.005)
        print('')