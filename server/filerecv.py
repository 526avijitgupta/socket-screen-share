import base64
import hashlib
import modules.create_socket as create_socket
import modules.decode_data as decode_data
import thread

DATASTORE_PATH = '/home/vishal/Desktop/socket-screen-share/server/datastore/'

def recv_file(conn):
    data_recv = conn.recv(1024)
    conn.send('1')
    if data_recv:
        print 'Creating file on server'
        f = open(DATASTORE_PATH + data_recv,'wb')
        file_data_recv = conn.recv(1024)
        while file_data_recv:
            print "receiving file"
            f.write(file_data_recv)
            file_data_recv = conn.recv(1024)
            if not file_data_recv:
                break

HOST = ''
PORT = 4513

if __name__ == '__main__':
    s = create_socket.start_server(HOST, PORT)
    while True:
        conn, addr = s.accept()
        thread.start_new_thread(recv_file, (conn,))
