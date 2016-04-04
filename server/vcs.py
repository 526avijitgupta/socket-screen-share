import modules.create_socket as create_socket
import modules.handle_client_handshake as handle_client_handshake
import modules.decode_data as decode_data
import modules.lib.diff_match_patch as dmp_module

HOST = ''
PORT = 9205

if __name__ == "__main__":
    s = create_socket.start_server(HOST, PORT)
    dmp = dmp_module.diff_match_patch()
    while True:
        conn, addr = s.accept()
        handle_client_handshake.handle_client_handshake(conn)

        data_recv = conn.recv(4096)
        if not data_recv:
            break
        data_from_client = decode_data.decode_data(data_recv)

        patch = dmp.patch_fromText(data_from_client)

        result = dmp.patch_apply(patch, '')
        print result[0]


