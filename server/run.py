from connect import server

# making the server obj with proper ip and port
# ip = input('Enter the ip to listen for: ')
# port = input('Enter the port to listen for: ')

ip = '127.0.0.1' # edit this for you ip
port = '12345'
server_obj = server(ip, int(port))
client_socket = server_obj.search()

feature= server_obj.recvFeature()

