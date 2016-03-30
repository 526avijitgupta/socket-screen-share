import socket,hashlib,base64,thread

MAGIC = '258EAFA5-E914-47DA-95CA-C5AB0DC85B11'
HSHAKE_RESP = "HTTP/1.1 101 Switching Protocols\r\n" + \
            "Upgrade: websocket\r\n" + \
            "Connection: Upgrade\r\n" + \
            "Sec-WebSocket-Accept: %s\r\n" + \
            "\r\n"

HOST = ''
PORT = 4501
# client_count = 0
clients_set = set()
data_arr = []
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(5)
# conn, addr = s.accept()         
# print 'Connected by', addr

def new_client(conn, addr):
    global clients_set
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
    while 1:
        data_recv = conn.recv(4096)
        if not data_recv:
            break
        databyte = bytearray(data_recv)
        datalen = (0x7F & databyte[1])
        str_data = ''
        if(datalen > 0):
            mask_key = databyte[2:6]
            masked_data = databyte[6:(6+datalen)]
            unmasked_data = [masked_data[i] ^ mask_key[i%4] for i in range(len(masked_data))]
            str_data = str(bytearray(unmasked_data))
        data_arr.append(str_data)
        print str_data
        # resp = bytearray([0b10000001, len(str_data)])
        # for d in bytearray(str_data):
        #     resp.append(d)
        # conn.sendall(resp)
        # data1 = 'Avijit'
        data1 = str_data
        resp1 = bytearray([0b10000001, len(data1)])
        for d in bytearray(data1):
            resp1.append(d)
        for con in clients_set:
            print 'Sending to client'
            try:
                con.sendall(resp1)
            except:
                print("error sending to a client")

while 1:
    conn, addr = s.accept()
    thread.start_new_thread(new_client, (conn, addr,))

# conn.close()
