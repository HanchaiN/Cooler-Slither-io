# Hanchai Nonprasart
import socket
from contextlib import contextmanager 

HEADER = 2048
PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
class client:
	def __init__(self,ip):
		self.ip=ip
	@contextmanager
	def start(self):
		try:
			self.connect(self.ip)
			yield self
		finally:
			self.quit()
	
	def connect(self,SERVER):
		ADDR = (SERVER, PORT)
		self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.client.connect(ADDR)
	def move(self,direction):
		message = direction.encode(FORMAT)
		self.client.send(message)
	def get(self):
		message = 's'.encode(FORMAT)
		self.client.send(message)
		length = int(self.client.recv(HEADER).decode(FORMAT))
		return self.client.recv(length)
	def quit(self):
		message = 'q'.encode(FORMAT)
		self.client.send(message)
