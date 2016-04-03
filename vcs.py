import modules.lib.diff_match_patch as dmp_module
import modules.create_socket as create_socket
import base64
import hashlib


HOST = ''
PORT = 9201
MAGIC = '258EAFA5-E914-47DA-95CA-C5AB0DC85B11'
HSHAKE_RESP = "HTTP/1.1 101 Switching Protocols\r\n" + \
            "Upgrade: websocket\r\n" + \
            "Connection: Upgrade\r\n" + \
            "Sec-WebSocket-Accept: %s\r\n" + \
            "\r\n"

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

def decode_data(data_to_decode):
    databyte = bytearray(data_to_decode)
    datalen = (0x7F & databyte[1])
    if(datalen > 0):
        mask_key = databyte[2:6]
        masked_data = databyte[6:(6+datalen)]
        unmasked_data = [masked_data[i] ^ mask_key[i%4] for i in range(len(masked_data))]
        data_from_client = str(bytearray(unmasked_data))
    return data_from_client or data_to_decode


if __name__ == "__main__":
    s = create_socket.start_server(HOST, PORT)
    dmp = dmp_module.diff_match_patch()
    while True:
        conn, addr = s.accept()
        handle_client_handshake(conn)

        data_recv = conn.recv(4096)
        if not data_recv:
            break
        data_from_client = decode_data(data_recv)

        patch = dmp.patch_fromText(data_from_client)

        result = dmp.patch_apply(patch, '')
        print result[0]


    
    
