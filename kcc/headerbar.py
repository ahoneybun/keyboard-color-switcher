#!/usr/bin/python3

import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


class Headerbar(Gtk.Headerbar):
    def __init__(self, parent):

        Gtk.Headerbar.__init__(self)
        self.parent = parent

        self.set_show_close_button(True)
        self.set_has_subtitle(False)

        self.switcher = Gtk.StackSwitcher()
        self.switcher.set_baseline_position(Gtk.BaselinePosition.CENTER)
        self.set_custom_title(self.switcher)

        self.spinner = Gtk.Spinner()
        self.pack_end(self.spinner)
