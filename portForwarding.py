import socket
import sys
import threading

def forward(sock1,sock2):
	try:
		data = ""
		flag = 1
		while data or flag == 1:
			flag = 0
			data = sock1.recv(4096)
			if data:
				sock2.sendall(data)
			else:
				sock1.shutdown(socket.SHUT_RD)
				sock2.shutdown(socket.SHUT_WR)
	except:
		sock1.close()
		sock2.close()
		return

if __name__ == "__main__":
	listeningPort = int(raw_input("Enter the port whose data u want to forward : "))
	ip = raw_input("Ip to which the data is forwarded : ")

	remotePort = int(raw_input("Enter the remote host port number : "))
	remoteAddress = (ip,remotePort)

	#creating a listening socket
	soc = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	print "Listening socket created"

	#bind the socket to all interfaces on the port which needs to be forwarded
	try:
		soc.bind(("",listeningPort))
	except socket.error as msg:
		print "Bind failed. Error code : "+str(msg[0]) + " message: "+msg[1]
		sys.exit()
	print "Success! Socket binding"

	#start listening for requests
	soc.listen(10)

	try:
		while True:
			clientSoc, addr = soc.accept()
			print "Connected to "+addr[0]+":"+str(addr[1])

			serverSoc = socket.socket()
			serverSoc.connect(remoteAddress)

			thread1 = threading.Thread(target=forward,args=(clientSoc,serverSoc,))
			thread1.start()

			thread2 = threading.Thread(target=forward,args=(serverSoc,clientSoc,))
			thread2.start()

	except Exception,e:
		print "Error : "+str(e)
		print "Closing server"
		soc.close()
