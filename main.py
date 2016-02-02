import socket
import thread
from Tkinter import *

keysArr = []

def keyEvent(event):
    global keysArr
    print event.keysym
    keysArr += [event.keysym]
    return event.keysym

def socket_server(socket):
    global keysArr
    while True:
        print "Serving on localhost"
	print keysArr
        conn, addr = socket.accept()
        if len(keysArr):
            conn.send(''.join(keysArr))
            keysArr = []
        conn.close()

if __name__ == "__main__":

    main = Tk()
    frame = Frame(main, width=500, height=500)
    Label(main, text="Code").grid(row=0)
    key = main.bind('<Key>', keyEvent)

    print 'hello'
    e1 = Entry(main)
    e2 = Entry(main)

    e1.grid(row=0, column=1)
    e1.grid(row=1, column=1)
    socket = socket.socket()
    HOST = 'localhost'
    PORT = 4500

    socket.bind((HOST, PORT))
    socket.listen(3)

    thread.start_new_thread(socket_server, (socket,))
    
    main.mainloop()
