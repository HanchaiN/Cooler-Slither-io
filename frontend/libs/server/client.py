# Hanchai Nonprasart
import socket

HEADER = 2048
PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
client = None

def connect(SERVER):
	global client
	ADDR = (SERVER, PORT)
	client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	client.connect(ADDR)
def move(direction):
	message = direction.encode(FORMAT)
	client.send(message)
def get():
	message = 's'.encode(FORMAT)
	client.send(message)
	length = int(client.recv(HEADER).decode(FORMAT))
	return client.recv(length)
def quit():
	message = 'q'.encode(FORMAT)
	client.send(message)