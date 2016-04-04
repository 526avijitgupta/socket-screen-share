import base64
import hashlib
import modules.create_socket as create_socket
import modules.decode_data as decode_data
import modules.handle_client_handshake as handle_client_handshake
import os
import thread

HOST = ''
PORT = 4530
DATASTORE_PATH = '/home/avijit/github/socket-screen-share/server/datastore/'
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

def send_to_client(data, conn):
    try:
        conn.sendall(data)
    except:
        print("error sending to a client")

def send_file_string(conn):
    files_string = fetch_txt_files()
    if len(files_string) >= 1:
        print 'Sending.. ' + files_string
        send_to_client(encode_data('Files_List: ' + files_string), conn)

def store_mapping_and_send_file_data(conn, data_from_client, files_mapping):
    open_file_name = data_from_client
    files_mapping[conn] = open_file_name
    f = open(DATASTORE_PATH + open_file_name, 'r+')
    send_to_client(encode_data(''.join(f.readlines())), conn)
    f.close()
    return open_file_name

def save_to_file(data_from_client, open_file_name):
    if open_file_name is not None:
        print 'Writing to file name: ' + open_file_name
        f = open(DATASTORE_PATH + open_file_name, 'r+')
        f.write(data_from_client)
        f.close()

def send_updated_file(data_from_client, open_file_name, clients_set, files_mapping):
    encoded_data = encode_data(data_from_client)
    for con in clients_set:
        if files_mapping[con] == open_file_name:
            print 'OPEN_FILE_NAME ', open_file_name
            send_to_client(encoded_data, con)

def new_client(conn, addr, clients_set, files_mapping):
    clients_set.add(conn)
    handle_client_handshake.handle_client_handshake(conn)
    send_file_string(conn)

    while 1:
        data_recv = conn.recv(4096)
        if not data_recv:
            break
        data_from_client = decode_data.decode_data(data_recv)

        if ".txt" in data_from_client:
            open_file_name = store_mapping_and_send_file_data(conn, data_from_client, files_mapping)
        else:
            save_to_file(data_from_client, open_file_name)
            send_updated_file(data_from_client, open_file_name, clients_set, files_mapping)


if __name__ == "__main__":
    clients_set = set()
    files_mapping = {}
    s = create_socket.start_server(HOST, PORT)

    while 1:
        conn, addr = s.accept()
        if addr[0] not in connected_ips_list:
            connected_ips_list.append(addr[0])
            print 'Got new connection'
            print conn
            print addr
            print 'NEW client connected'
            thread.start_new_thread(new_client, (conn, addr, clients_set, files_mapping))
        else:
            print 'Same client already connected'
