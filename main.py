import socket
import thread
from Tkinter import *
from time import sleep
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Pango

class TextViewWindow(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="TextView Example")

        self.set_default_size(350, 350)

        self.grid = Gtk.Grid()
        self.add(self.grid)
        self.scrolledwindow = Gtk.ScrolledWindow()

        self.create_textview()

    def create_textview(self):
        self.scrolledwindow.set_hexpand(True)
        self.scrolledwindow.set_vexpand(True)
        self.grid.attach(self.scrolledwindow, 0, 1, 3, 1)

        self.textview = Gtk.TextView()
        self.textbuffer = self.textview.get_buffer()
        self.scrolledwindow.add(self.textview)

    def get_val(self):
        start_iter = self.textbuffer.get_start_iter()
        end_iter = self.textbuffer.get_end_iter()
        return self.textbuffer.get_text(start_iter, end_iter, False)

    def on_editable_toggled(self, widget):
        self.textview.set_editable(widget.get_active())


def socket_server(socket, win):
    while True:
        textValue = win.get_val()
        #conn, addr = socket.accept()
        if textValue:
            print textValue
            #conn.send(win.get_val())
        #conn.close()

if __name__ == "__main__":

    win = TextViewWindow()
    win.connect("delete-event", Gtk.main_quit)
    win.show_all()
    print win.get_val()

    socket = socket.socket()
    HOST = 'localhost'
    PORT = 4500

    socket.bind((HOST, PORT))
    socket.listen(3)

    thread.start_new_thread(socket_server, (socket, win))
    Gtk.main()

