#!/usr/bin/python3
import os
import sys
from typing import Tuple

import gi
from gi.repository import Gtk, Gio

current_path = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, f"{current_path}/system76_backlight_manager/")

from system76_backlight_manager.keyboard_backlight import KeyboardBacklight
from system76_backlight_manager.enums import Position

if os.geteuid() != 0:
    exit("You need to have root privileges to run this.")

gi.require_version("Gtk", "3.0")


class MainWindow(Gtk.Window):

    REGION_TO_COLOR_MAPPING = {
        "left": Position.LEFT,
        "center": Position.CENTER,
        "right": Position.RIGHT,
    }

    def __init__(self):
        self.keyboard_backlight = KeyboardBacklight()

        Gtk.Window.__init__(self)
        self.set_border_width(100)

        # HeaderBar Define
        self.headerbar = Gtk.HeaderBar()
        self.set_titlebar(self.headerbar)
        self.headerbar.set_show_close_button(True)
        self.headerbar.props.title = "Keyboard Color Switcher"

        self.aboutbutton = Gtk.Button()
        icon = Gio.ThemedIcon(name="open-menu-symbolic")
        image = Gtk.Image.new_from_gicon(icon, Gtk.IconSize.BUTTON)
        self.aboutbutton.add(image)
        self.headerbar.pack_end(self.aboutbutton)

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        self.add(vbox)

        # Label Definement
        self.aboutlabel = Gtk.Label()
        self.aboutlabel.set_text("GTK tool for changing keyboard region colors")
        self.aboutcenterlabel = Gtk.Label()
#       self.centerlabel.set_halign()

        self.grid = Gtk.Grid()
        self.grid.set_column_spacing(6)
        self.grid.set_halign(Gtk.Align.CENTER)
        self.grid.set_valign(Gtk.Align.CENTER)

        self.is_multi_color = self.keyboard_backlight.is_multi_region_color()

        if self.is_multi_color:
            self.left_button, self.left_label = self._create_control_button("Left")
            self.right_button, self.right_label = self._create_control_button("Right")

            self.grid.attach(self.left_label, 0, 2, 1, 1)
            self.grid.attach(self.left_button, 0, 1, 1, 1)

            self.grid.attach(self.right_label, 2, 2, 1, 1)
            self.grid.attach(self.right_button, 2, 1, 1, 1)

        self.center_button, self.center_label = self._create_control_button("Center")

        self.grid.attach(self.center_label, 1, 2, 1, 1)
        self.grid.attach(self.center_button, 1, 1, 1, 1)

        vbox.pack_start(self.aboutlabel, True, True, 0)
        vbox.pack_start(self.aboutcenterlabel, True, True, 0)
        vbox.pack_start(self.grid, True, True, 0)

    def _create_control_button(self, label: str, alignment: Gtk.Align = Gtk.Align.CENTER) -> Tuple[Gtk.ColorButton, Gtk.Label]:
        button = Gtk.ColorButton()
        label_component = Gtk.Label.new(label)
        button.set_halign(alignment)
        button.set_valign(Gtk.Align.CENTER)
        button.set_size_request(75, 50)

        button.connect("clicked", self.on_button_clicked)
        button.connect("color-set", self.on_color_activated, label.lower())

        return button, label_component

    def on_color_activated(self, widget, region):
        """
        Color Grab in the interface
        """
        print(region)
        color = widget.get_rgba()
        red = "{0:0{1}X}".format(int(color.red*255), 2)
        green = "{0:0{1}X}".format(int(color.green*255), 2)
        blue = "{0:0{1}X}".format(int(color.blue*255), 2)
        color_string = red + green + blue
        print(color_string)

        position = self.REGION_TO_COLOR_MAPPING[region]
        self.keyboard_backlight.set_color(color_string, position)

    def on_button_clicked(self, widget):
        win.show_all()


win = MainWindow()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()
