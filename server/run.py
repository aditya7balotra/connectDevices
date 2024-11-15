from connect import server


ip = '127.0.0.1' # edit this for you ip
port = '12345'
server_obj = server(ip, int(port))
client_socket = server_obj.search()

feature= server_obj.recvFeature()

