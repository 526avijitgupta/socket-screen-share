import socket,hashlib,base64,thread

MAGIC = '258EAFA5-E914-47DA-95CA-C5AB0DC85B11'
HSHAKE_RESP = "HTTP/1.1 101 Switching Protocols\r\n" + \
            "Upgrade: websocket\r\n" + \
            "Connection: Upgrade\r\n" + \
            "Sec-WebSocket-Accept: %s\r\n" + \
            "\r\n"
file_recv_flag = 0
HOST = ''
PORT = 4500
# client_count = 0
clients_set = set()

data_from_client = ''
f = open("file.txt", 'r+')
list_arr = f.readlines()
for line in list_arr:
    data_from_client += line + '\n'
print 'Data from client: %s' % (data_from_client)
f.close()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(5)
# conn, addr = s.accept()         

# print 'Connected by', addr

def encode_data(data_to_encode):
    resp = bytearray([0b10000001, len(data_to_encode)])
    for d in bytearray(data_to_encode):
        resp.append(d)
    return resp

def new_client(conn, addr):
    global clients_set
    global data_from_client
    clients_set.add(conn)
    print len(clients_set)
    print ' is the count'
    print 'Connected by', addr
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
    if len(data_from_client) >= 1:
        # for con in clients_set:
        encoded_data = encode_data(data_from_client)
        try:
            conn.sendall(encoded_data)
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


        if file_recv_flag == 1:
            filename = data_from_client
            print filename
            f = open(filename,'wb')
            while data_from_client:
                f.write(data_from_client)
                data_from_client = conn.recv(1024)
                if not data_from_client:
                    break
                databyte = bytearray(data_from_client))
                datalen = (0x7F & databyte[1])
                if(datalen > 0):
                    mask_key = databyte[2:6]
                    masked_data = databyte[6:(6+datalen)]
                    unmasked_data = [masked_data[i] ^ mask_key[i%4] for i in range(len(masked_data))]
                    data_from_client = str(bytearray(unmasked_data))
            f.close()


        if data_from_client == 'filestart':
            file_recv_flag  += 1

        if data_from_client == 'fileend':
            file_recv_flag  += 1

        if file_recv_flag == 2:
            print "file has received"


        #f = open("file.txt", 'r+')
        #f.write(data_from_client)
        #f.close()

        encoded_data = encode_data(data_from_client)
        for con in clients_set:
            try:
                con.sendall(encoded_data)
            except:
                print("error sending to a client")

while 1:
    conn, addr = s.accept()
    thread.start_new_thread(new_client, (conn, addr,))

# conn.close()
