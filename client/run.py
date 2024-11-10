from connect import client

ip = '127.0.0.1' # edit this for your ip
port = '12345'
client_obj = client(ip, int(port))
client_socket = client_obj.connect()
feature = input('Enter the feature name: ')

client_obj.select_feature(featureName= feature)