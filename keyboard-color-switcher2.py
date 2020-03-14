#!/usr/bin/python3

# Imports
import gi
import sys

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gio
from .headerbar import Headerbar
from .stack import Stack

class indow(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self)
        self.set_border_width(100)

        self.hbar = Headerbar(self)
        self.set_titlebar(self.hbar)

        self.stack = Stack(self)
        self.add(self.stack)

        self.hbar.switcher.set_stack(self.stack.stack)

        self.screen = Gdk.Screen.get_default()
        self.css_provider = Gtk.CssProvider()

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        self.add(vbox)

win = Window()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()
