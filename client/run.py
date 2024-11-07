from connect import client

# object for the client server with proper host and port
# ip = input('Enter the ip of the server: ')
# port = input('Enter the port for the server: ')

ip = '127.0.0.1'
port = '12345'
client_obj = client(ip, int(port))
client_socket = client_obj.connect()
feature = input('Enter the feature name: ')

client_obj.select_feature(featureName= feature)