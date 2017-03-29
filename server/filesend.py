import base64
import hashlib
import modules.create_socket as create_socket
import modules.decode_data as decode_data
import modules.handle_client_handshake as handle_client_handshake
import thread

DATASTORE_PATH = '/home/vishal/Desktop/socket-screen-share/client/files/'

def send_file(filename):
    f = open(DATASTORE_PATH + filename, 'w')
    f.close()
    f = open(DATASTORE_PATH + filename, 'r')
    l = f.read(1024)
    c = create_socket.start_client(HOST, 4513)
    c.send(filename)

    while True:
       recv_flag =  c.recv(1024)
       if recv_flag == '1':
           break

    while l:
        c.send(l)
        l = f.read(1024)
    f.close()
    c.close()

HOST = ''
PORT = 4511

def new_client(conn):
    handle_client_handshake.handle_client_handshake(conn)
    while True:
        file_name_recv = conn.recv(4096)
        if file_name_recv:
            decoded_data = decode_data.decode_data(file_name_recv)
            # print decoded_data
            file_name = decoded_data.replace('Create file:', '')
            # print file_name
            send_file(file_name)


if __name__ == '__main__':
    s = create_socket.start_server(HOST, PORT)

    while True:
        conn, addr = s.accept()
        thread.start_new_thread(new_client, (conn,))

