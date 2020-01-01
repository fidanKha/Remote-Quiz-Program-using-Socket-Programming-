from socket import *
import threading
import time


class Question:
	def __init__(self, question, answer):
		self.question = question
		self.answer = answer


class User:
	quizScore = 0
	answers_received = []
	def __init__(self, username):
		self.username = username
	def input_answers(self, answer):
		self.answers_received.append(answer)

class ThreadedServer():
	users = []
	questions = [
		Question('Which one is false for TCP.\nA)	Connectionless\nB)	In-order\nC)	Reliable\n', 'A'),
		Question('Which one is not an access network.\nA)	DSL\nB)	cable network\nC)	hosts\n', 'C'),
		Question('How is network core defined:\nA)	net of nets, interconnected routers\nB)	wired-wireless communication links\nC)	hosts: server and clients\n', 'A')
		]

	def listenToClient(self, client, addr, server):

		client.send("Enter a username.\n".encode())
		message = client.recv(1024)
		if message == "exit":
			print(addr, " is closed")
			client.close()
			sys.exit(0)

		else:
			username = message
			user = User(username)
			user.answers_received = []
			currentUser = self.existing_user(user,self.users)

			while currentUser:
				# each user attend quiz only one time
				client.send("Username is already in use, please choose another one: ")
				message = client.recv(1024)
				username = message
				user = User(username)
				currentUser = self.existing_user(user,self.users)

			count = 1
			for question in self.questions:
				questionNo = "\nQuestion " + str(count) + ": "
				questiontosend = questionNo + question.question
				client.send(questiontosend.encode())
				message = client.recv(1)
				count = count + 1
				if(message):
					print("received")
					user.input_answers(message)
					if message == question.answer or message == question.answer.lower():
						user.quizScore += 1
				else:
					print("message not received")
			self.users.append(user)

			sendresult =user.username + " you got a total score of: " + str(user.quizScore) + '/' + str(len(self.questions)) + ".\n" 
			q1 = "\nThe received and correct answers are as below: \n 1) " + self.questions[0].question + "Correct answer: " + self.questions[0].answer + "; You answered: " + user.answers_received[0] 
			q2 = "\n\n 2)" + self.questions[1].question + "Correct answer: " + self.questions[1].answer + "; You answered: " + user.answers_received[1] 
			q3 = "\n\n 3)" +  self.questions[2].question + "Correct answer: " + self.questions[2].answer + "; You answered: " + user.answers_received[2] 
			tosend = sendresult+q1+q2+q3
			client.send(tosend.encode())
			print('\n')
			for user1 in self.users:
				print(user1.username)
				print(user1.answers_received)
			print(addr, " is closed")
			client.close()
			exit(0)
			sys.exit(1)



	def existing_user(self, this_user, users_saved):
		for aUser in users_saved:
			if aUser.username == this_user.username:
				return aUser
		return False


	def __init__(self, serverPort):
		try:
			serverSocket = socket(AF_INET, SOCK_STREAM)
		except:
			print("Socket cannot be created!!!")
			exit(1)
		print("Socket is created...")
		try:
			serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
		except:
			print("Socket cannot be used!!!")
			exit(1)
		print("Socket is being used...")
		try:
			serverSocket.bind(('', serverPort))
		except:
			print("Binding cannot de done!!!")
			exit(1)
		print("Binding is done...")
		try:
			serverSocket.listen(45)
		except:
			print("Server cannot listen!!!")
			exit(1)
		print("The server is ready to receive")
		while True:
			connectionSocket, addr = serverSocket.accept()
			threading.Thread(target=self.listenToClient, args=(connectionSocket, addr, serverSocket)).start()

if __name__ == "__main__":
	serverPort = 12000
ThreadedServer(serverPort)
