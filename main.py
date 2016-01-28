import socket
import thread
from Tkinter import *

def keyEvent(event):
    # keysArr = []
    print event.keysym
    # keysArr += [event.keysym]
    # print keysArr
    return event.keysym

def socket_server(socket):
    while True:
        print "Serving on localhost"
        # main.mainloop()
        # sleep(2)
        conn, addr = socket.accept()
        # import ipdb; pdb.set_trace()
        # print keysArr
        # while len(keysArr) > 0:
        # conn.send(keysArr.pop())
        conn.send('Hello')    
        # print "Connection received"
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
    print 'hello'

    # frame.focus_set()

    print 'hello'

    socket = socket.socket()

    HOST = 'localhost'
    PORT = 4500

    socket.bind((HOST, PORT))
    socket.listen(3)

    thread.start_new_thread(socket_server, (socket,))
    
    main.mainloop()
    # socket.close()
