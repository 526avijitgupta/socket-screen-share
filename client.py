import socket
import sys
from time import sleep

HOST = 'localhost'
PORT = 4500

data = ""

while True:
    sock = socket.socket()
    sock.connect((HOST, PORT))
    sleep(3)
    prevData = data
    print 'prevData: ' + prevData
    data = sock.recv(1024)
    print 'data: ' + data
    if not data:
        print "data not present"
    if data is prevData:
        print "same"
sock.close()
