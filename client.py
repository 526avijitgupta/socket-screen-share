import socket
import sys

HOST = 'localhost'
PORT = 4500


while True:
    sock = socket.socket()
    sock.connect((HOST, PORT))
    
    while True:
        data = sock.recv(1024)
        if not data:
            break
        print data

    sock.close()


