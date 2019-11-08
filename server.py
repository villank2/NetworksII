import socket
import threading
import sys
ip_addr = '127.0.0.1'
port = 8100 

#setup 32bit ipv4, TCP/IP
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
print('server started')
#give socket an ip address and port
socket_details = (ip_addr, port)
serversocket.bind(socket_details)
serverrunning = True
serversocket.listen(100)

# make list for connected devices 

connected_devices = {}

#function to create a thread

def start_client_thread(connection,address):
	th = threading.Thread(target=client_thread, args=(connection,address))
	th.start()
	connected_devices[connection]['thread'] = th
#broadcast function, send data to all clients except the og sender
def broadcast(message, og_conn):
	# loop through connected devices 
	#send data to connection
	for conn in connected_devices:
		if conn != og_conn:
			conn.send(message.encode())



# function to handle connection thread
def client_thread(conn, addr):
	welcome = "Welcome to the chatroom"
	conn.send(welcome.encode())

	# if the client sends us data
	# send the data to every other client
	while serverrunning:
		try:
			message = conn.recv(1024)
			if message is not None:
				enc_message = message.decode()
				message_to_send = "<{}> {}".format(addr, enc_message)
				print(message_to_send)
				broadcast(message_to_send, conn)
			else:
				pass
		except:
			continue
#main loop
#loop forever
#if thre is a client waiting to connect
#make thread for the client 
# go to 1
try:
	while True:
		conn , addr = serversocket.accept()
		connected_devices[conn] = {'addr':addr}
		print("{} connected".format(addr))
		#start a thread for the cleint connection
		start_client_thread(conn,addr)
except KeyBoardInterrupt:
	print('Server shutting down')
	for conn in  connected_devices:
		conn.close()
	serversocket.close()
	serverrunning = False
	print('Goodbye')
	sys.exit(0)