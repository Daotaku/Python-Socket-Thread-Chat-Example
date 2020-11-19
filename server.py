import socket
import threading

HEADER = 64
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
USERNAME_MESSAGE = "!USERNAME"
GLOBAL_MESSAGE = []

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

def idx_last(last_message):
	for i in range(len(GLOBAL_MESSAGE)):
		if last_message == GLOBAL_MESSAGE[i]:
			return i

	return False

def broadcast(conn, last_message):
	while True:
		last_index = idx_last(last_message)

		for glob_message in GLOBAL_MESSAGE[last_index+1:]:
			conn.send(glob_message.encode(FORMAT))
			last_message = glob_message


def handle_client(conn, addr):
	print(f"[NEW CONNECTION] {addr} connected.")

	connected = True

	if len(GLOBAL_MESSAGE):
		last_message = GLOBAL_MESSAGE[-1]
	else:
		last_message = ""

	while connected:

		try:
			msg_length = conn.recv(HEADER).decode(FORMAT)

			if msg_length:
			msg_length = int(msg_length)
			msg = conn.recv(msg_length).decode(FORMAT)

			if msg == DISCONNECT_MESSAGE:
				connected = False

			if USERNAME_MESSAGE in msg:
				username_length = len(USERNAME_MESSAGE)+1
				username = msg[username_length:]
				GLOBAL_MESSAGE.append(f"<< {username} is now logged in.. >>")
				thread = threading.Thread(target=broadcast, args=(conn, last_message))
				thread.start()
			else:
				GLOBAL_MESSAGE.append(f"<{username}>: {msg}")

			last_message = GLOBAL_MESSAGE[-1]

		except:
			connected = False
			conn.close()	
			print("connection closed")

	conn.close()
	print("connection closed")

def start():
	server.listen()
	print(f"[LISTENING] Server is listening on {SERVER}")
	while True:
		conn, addr = server.accept()
		thread = threading.Thread(target=handle_client, args=(conn, addr))
		thread.start()
		print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")

print("[STARTING] server is starting...")
start()

