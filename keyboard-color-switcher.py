#!/usr/bin/python3
import os
import sys
from typing import Tuple

import gi
from gi.repository import Gtk, Gio

from kcc_cli.keyboard_backlight import KeyboardBacklight
from kcc_cli.enums import Position

if os.geteuid() != 0:
    exit("You need to have root privileges to run this.")

gi.require_version('Gtk', '3.0')


class MainWindow(Gtk.Window):

    REGION_TO_COLOR_MAPPING = {
        'left': Position.LEFT,
        'center': Position.CENTER,
        'right': Position.RIGHT,
    }

    def __init__(self):
        self.keyboard_backlight = KeyboardBacklight()

        Gtk.Window.__init__(self)
        self.set_border_width(100)

        #### HeaderBar Define
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

        ### Label Definement
        self.aboutlabel = Gtk.Label()
        self.aboutlabel.set_text("GTK tool for changing keyboard region colors")
        self.aboutcenterlabel = Gtk.Label()
#       self.centerlabel.set_halign()

        self.ledPath = "/"+ os.path.join('sys', 'class', 'leds', 'system76_acpi::kbd_backlight')
        if os.path.exists(self.ledPath) == False:
           self.ledPath = "/" + os.path.join('sys', 'class', 'leds', 'system76::kbd_backlight')

        # Detect if single color or multi color regions
        self.colors = False
        self.colorCenter = "/color"
        if os.path.exists(os.path.join(self.ledPath, 'color_left')):
           self.colors = True
           self.colorCenter = "/color_center"

        if self.colors == True:
           ### Button Definement
           self.leftbutton = Gtk.ColorButton()
           self.leftlabel = Gtk.Label.new("Left")
           self.leftbutton.set_halign(Gtk.Align.CENTER)
           self.leftbutton.set_valign(Gtk.Align.CENTER)
           self.leftbutton.set_size_request(75, 50)

        self.centerbutton = Gtk.ColorButton()
        self.centerlabel = Gtk.Label.new("Center")
        self.centerbutton.set_halign(Gtk.Align.CENTER)
        self.centerbutton.set_valign(Gtk.Align.CENTER)
        self.centerbutton.set_size_request(75, 50)

        if self.colors == True:
           self.rightbutton = Gtk.ColorButton()
           self.rightlabel = Gtk.Label.new("Right")
           self.rightbutton.set_halign(Gtk.Align.CENTER)
           self.rightbutton.set_valign(Gtk.Align.CENTER)
           self.rightbutton.set_size_request(75, 50)

        ### Grid Setup
        self.grid = Gtk.Grid()
        self.grid.set_column_spacing(6)
        self.grid.set_halign(Gtk.Align.CENTER)
        self.grid.set_valign(Gtk.Align.CENTER)

        ### Connect Signal handlers
        if self.colors == True:
           self.leftbutton.connect("clicked", self.on_button_clicked)
           self.leftbutton.connect("color-set", self.on_color_activated, "left")
           self.rightbutton.connect("clicked", self.on_button_clicked)
           self.rightbutton.connect("color-set", self.on_color_activated, "right")

        self.centerbutton.connect("clicked", self.on_button_clicked)
        self.centerbutton.connect("color-set", self.on_color_activated, "center")


        ### Grid Setup/2
        if self.colors == True:
           self.grid.attach(self.leftlabel, 0, 2, 1, 1)
           self.grid.attach(self.leftbutton, 0, 1, 1, 1)
           self.grid.attach(self.rightlabel, 2, 2, 1, 1)
           self.grid.attach(self.rightbutton, 2, 1, 1, 1)

        self.grid.attach(self.centerlabel, 1, 2, 1, 1)
        self.grid.attach(self.centerbutton, 1, 1, 1, 1)

        vbox.pack_start(self.aboutlabel, True, True, 0)
        vbox.pack_start(self.aboutcenterlabel, True, True, 0)
        vbox.pack_start(self.grid, True, True, 0)

        ### Color Grab
    def on_color_activated(self, widget, region):
        print(region)
        color = widget.get_rgba()
        red = "{0:0{1}X}".format(int(color.red*255),2)
        green = "{0:0{1}X}".format(int(color.green*255),2)
        blue = "{0:0{1}X}".format(int(color.blue*255),2)
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
