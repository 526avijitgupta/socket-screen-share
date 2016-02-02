import socket
import sys
from time import sleep

HOST = 'localhost'
PORT = 4500

while True:
    sock = socket.socket()
    sock.connect((HOST, PORT))
    data = sock.recv(1024)
    if data:
        print data
sock.close()
