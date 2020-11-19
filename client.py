import socket
import threading

HEADER = 64
PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = "192.168.2.249"
ADDR = (SERVER, PORT)
USERNAME = "NONE"

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

def listen():
	while True:
		msg = client.recv(2048).decode(FORMAT)

		if msg:
			print(msg)

def send(msg):
	message = msg.encode(FORMAT)
	msg_length = len(message)
	send_length = str(msg_length).encode(FORMAT)
	send_length += b' ' * (HEADER - len(send_length))
	client.send(send_length)
	client.send(message)
	#print(client.recv(2048).decode(FORMAT))

def disconnect():
	send(DISCONNECT_MESSAGE)

def start():
	USERNAME = input("Hi, please enter your name: ")
	
	thread = threading.Thread(target=listen)
	thread.start()

	send(f"!USERNAME {USERNAME}")

	print("Start chat by typing the word or enter X to quit.")
	msg = ""

	while msg != "X":
		msg = input()
		send(msg)

	disconnect()

start()
