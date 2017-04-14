import base64
import hashlib
import modules.create_socket as create_socket
import modules.decode_data as decode_data
import modules.handle_client_handshake as handle_client_handshake
import os
from time import sleep
import thread
from filelock import FileLock
import io
import sys

HOST = ''
PORT = 4540
DATASTORE_PATH = '/home/vishal/Desktop/socket-screen-share/server/datastore/'
connected_ips_list = []

def fetch_txt_files():
    files_string = ''
    for file in os.listdir(DATASTORE_PATH):
        if file.endswith('.txt'):
            files_string += file + ' '
    return files_string

def encode_data(data_to_encode):
    resp = bytearray([0b10000001, len(data_to_encode)])
    for d in bytearray(data_to_encode):
        resp.append(d)
    return resp
    # return data_to_encode

def send_to_client(data, conn):
    try:
        conn.sendall(data)
        return 1
    except:
        print("error sending to a client")
        return 0

def send_file_string(conn,clients_set,files_mapping):
    conn_removal = set()
    while 1:
    # print 'Calling once'
    # for i in range(0,5):
        # print 'Sending %d time' % (i)
        files_string = fetch_txt_files()
        if len(files_string) >= 1:
            # print 'Sending.. ' + files_string
            list_flag = send_to_client(encode_data('Files_List: ' + files_string), conn)
            if list_flag == 0:
                if conn in clients_set:
                    clients_set.remove(conn)
                    files_mapping.pop(conn, 0)
                    conn.close()
                break
        else:
            # print 'Sending.. ' + files_string
            list_flag = send_to_client(encode_data('Files_List: empty'), conn)
            if list_flag == 0:
                if conn in clients_set:
                    clients_set.remove(conn)
                    files_mapping.pop(conn, 0)
                    conn.close()
                break
        sleep(3)
    thread.exit()

def store_mapping_and_send_file_data(conn, data_from_client, files_mapping):
    open_file_name = data_from_client
    print 'New file..........'
    print 'Data from client: ' + data_from_client
    files_mapping[conn] = open_file_name
    f = open(DATASTORE_PATH + open_file_name, 'rb')
    send_to_client(encode_data(''.join(f.readlines())), conn)
    f.close()
    return open_file_name

def save_to_file(data_from_client, open_file_name):
    if open_file_name is not None:
        print 'Writing to file name: ' + open_file_name
        lock = FileLock(DATASTORE_PATH + open_file_name)
        lock.acquire()
        try:
            f = open(DATASTORE_PATH + open_file_name, 'w+')
            f.write(data_from_client)
        finally:
            f.close()
            # file.close()
            lock.release()


def send_updated_file(data_from_client, open_file_name, clients_set, files_mapping):
    encoded_data = encode_data(data_from_client)
    for con in clients_set:
        if files_mapping[con] == open_file_name:
            print 'OPEN_FILE_NAME ', open_file_name
            send_to_client(encoded_data, con)

def new_client(conn, addr, clients_set, files_mapping):
    clients_set.add(conn)
    handle_client_handshake.handle_client_handshake(conn)
    thread.start_new_thread(send_file_string, (conn,clients_set,files_mapping))

    while 1:
        print 'Calling file send'
        data_recv = conn.recv(4096)
        print "data received: " + data_recv
        if not data_recv:
            print "connection closing"
            clients_set.remove(conn)
            files_mapping.pop(conn, 0)
            print "closing this connection"
            conn.close()
            break
        data_from_client = decode_data.decode_data(data_recv)
        # data_from_client = data_recv.decode('utf-8', 'ignore')
        print "decoded data: " + data_from_client
        # data_from_client = b""+data_recv.decode("utf-8")
        if "connection closed" in data_from_client:
            print "connection closed"
            clients_set.remove(conn)
            files_mapping.pop(conn, 0)
            conn.close()
            thread.exit()

        if ".txt" in data_from_client:
            open_file_name = store_mapping_and_send_file_data(conn, data_from_client, files_mapping)
        else:
            save_to_file(data_from_client, open_file_name)
            send_updated_file(data_from_client, open_file_name, clients_set, files_mapping)
    thread.exit()


if __name__ == "__main__":
    clients_set = set()
    files_mapping = {}
    s = create_socket.start_server(HOST, PORT)

    while 1:
        conn, addr = s.accept()
        # if addr[0] not in connected_ips_list:
        connected_ips_list.append(addr[0])
        #     print 'Got new connection'
        #     print conn
        #     print addr
        #     print 'NEW client connected'
        thread.start_new_thread(new_client, (conn, addr, clients_set, files_mapping))
        # else:
        #     print 'Same client already connected'
