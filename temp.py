import socket,hashlib,base64,thread, os

HOST = ''
PORT = 4500
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


clients_set = set()
files_string = fetch_txt_files()
files_mapping = {}

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(5)

def new_client(conn, addr):
    global clients_set
    global files_mapping

    clients_set.add(conn)
    # print len(clients_set)
    # print ' is the count'
    # print 'Connected by', addr
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

    if len(files_string) >= 1:
        print 'Sending.. ' + files_string
        encoded_files_string = encode_data('Files_List: ' + files_string)
        try:
            conn.sendall(encoded_files_string)
        except:
            print("error sending to a client")

    while 1:
        data_recv = conn.recv(4096)
        if not data_recv:
            break
        databyte = bytearray(data_recv)
        datalen = (0x7F & databyte[1])
        if(datalen > 0):
            mask_key = databyte[2:6]
            masked_data = databyte[6:(6+datalen)]
            unmasked_data = [masked_data[i] ^ mask_key[i%4] for i in range(len(masked_data))]
            data_from_client = str(bytearray(unmasked_data))
        print data_from_client

        if ".txt" in data_from_client:
            open_file_name = data_from_client
            files_mapping[conn] = open_file_name
            f = open(open_file_name, 'r+')
            try:
                conn.sendall(encode_data(''.join(f.readlines())))
            except:
                print 'error'
            f.close()

        else:
            if open_file_name is not None:
                print 'Writing to file name: ' + open_file_name
                f = open(open_file_name, 'r+')
                f.write(data_from_client)
                f.close()

            encoded_data = encode_data(data_from_client)
            for con in clients_set:
                if files_mapping[con] == open_file_name:
                    print 'OPEN_FILE_NAME ', open_file_name
                    try:
                        con.sendall(encoded_data)
                    except:
                        print("error sending to a client")

while 1:
    conn, addr = s.accept()
    thread.start_new_thread(new_client, (conn, addr,))

# conn.close()
