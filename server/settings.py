import base64
import hashlib
import create_socket
import os
import thread

HOST = ''
PORT = 4502
MAGIC = '258EAFA5-E914-47DA-95CA-C5AB0DC85B11'
HSHAKE_RESP = "HTTP/1.1 101 Switching Protocols\r\n" + \
            "Upgrade: websocket\r\n" + \
            "Connection: Upgrade\r\n" + \
            "Sec-WebSocket-Accept: %s\r\n" + \
            "\r\n"

def fetch_txt_files():
    files_string = ''
    for file in os.listdir('/home/avijit/github/socket-screen-share'):
        if file.endswith('.txt'):
            files_string += file + ' '
    return files_string

def encode_data(data_to_encode):
    resp = bytearray([0b10000001, len(data_to_encode)])
    for d in bytearray(data_to_encode):
        resp.append(d)
    return resp

def decode_data(data_to_decode):
    databyte = bytearray(data_to_decode)
    datalen = (0x7F & databyte[1])
    if(datalen > 0):
        mask_key = databyte[2:6]
        masked_data = databyte[6:(6+datalen)]
        unmasked_data = [masked_data[i] ^ mask_key[i%4] for i in range(len(masked_data))]
        data_from_client = str(bytearray(unmasked_data))
    return data_from_client or data_to_decode

def handle_client_handshake(conn):
    data = conn.recv(4096)
    headers = {}
    lines = data.splitlines()
    for l in lines:
        parts = l.split(": ", 1)
        if len(parts) == 2:
            headers[parts[0]] = parts[1]
    headers['code'] = lines[len(lines) - 1]
    key = headers['Sec-WebSocket-Key']
    resp_data = HSHAKE_RESP % ((base64.b64encode(hashlib.sha1(key+MAGIC).digest()),))
    conn.send(resp_data)

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
    f = open(open_file_name, 'r+')
    send_to_client(encode_data(''.join(f.readlines())), conn)
    f.close()
    return open_file_name

def save_to_file(data_from_client, open_file_name):
    if open_file_name is not None:
        print 'Writing to file name: ' + open_file_name
        f = open(open_file_name, 'r+')
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
    handle_client_handshake(conn)
    send_file_string(conn)

    while 1:
        data_recv = conn.recv(4096)
        if not data_recv:
            break
        data_from_client = decode_data(data_recv)

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
        thread.start_new_thread(new_client, (conn, addr, clients_set, files_mapping))
