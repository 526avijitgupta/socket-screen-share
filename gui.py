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
        self.textbuffer.set_text("This is some text inside of a Gtk.TextView. "
            + "Select text and click one of the buttons 'bold', 'italic', "
            + "or 'underline' to modify the text accordingly.")
        self.scrolledwindow.add(self.textview)

    def get_val(self):
        start_iter = self.textbuffer.get_start_iter()
        end_iter = self.textbuffer.get_end_iter()
        print self.textbuffer.get_text(start_iter, end_iter, True)

    def on_editable_toggled(self, widget):
        self.textview.set_editable(widget.get_active())

win = TextViewWindow()
win.connect("delete-event", Gtk.main_quit)
win.show_all()
win.get_val()
Gtk.main()
