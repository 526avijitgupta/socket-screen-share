import socket

def start_server(host, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind((host, port))
    s.listen(5)
    return s

def start_client(host, port):
    c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    c.connect((host, port))
    return c

