from socket import *
import os

def cls():
	os.system('cls' if os.name=='nt' else 'clear')
serverName="127.0.0.1"
serverPort=12000
clientSocket=socket(AF_INET,SOCK_STREAM)
clientSocket.connect((serverName,serverPort))
message=clientSocket.recv(1024) 
print(message)

while(True):
	try:
		answer=raw_input('Type input: ') 
		if answer=="exit":
			clientSocket.close()
			break
			sys.exit(1)
		elif message[1:9]=="Question":
			clientSocket.send(answer)
		else:
			clientSocket.send(answer)
		cls() # to clear terminal
		message=clientSocket.recv(1024)
		print(message)
	except:
		clientSocket.close()
		break
exit(0)
