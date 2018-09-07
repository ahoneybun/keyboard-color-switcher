# Imports
import gi
import sys

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gio

class MainWindow(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self)
        self.set_border_width(100)

        # HeaderBar Define
        self.headerbar = Gtk.HeaderBar()
        self.set_titlebar(self.headerbar)
        self.headerbar.set_show_close_button(True)
        self.headerbar.props.title = "Keyboard Color Switcher"

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.add(vbox)

        # Button Definement
        self.leftbutton = Gtk.ColorButton()
        self.leftlabel = Gtk.Label("Left")
        self.leftbutton.set_halign(Gtk.Align.CENTER)
        self.leftbutton.set_valign(Gtk.Align.CENTER)
        self.leftbutton.set_size_request(75, 50)

        self.centerbutton = Gtk.ColorButton()
        self.centerlabel = Gtk.Label("Center")
        self.centerbutton.set_halign(Gtk.Align.CENTER)
        self.centerbutton.set_valign(Gtk.Align.CENTER)
        self.centerbutton.set_size_request(75, 50)

        self.rightbutton = Gtk.ColorButton()
        self.rightlabel = Gtk.Label("Right")
        self.rightbutton.set_halign(Gtk.Align.CENTER)
        self.rightbutton.set_valign(Gtk.Align.CENTER)
        self.rightbutton.set_size_request(75, 50)

        self.grid = Gtk.Grid()
        self.grid.set_column_spacing(6)
        self.grid.set_halign(Gtk.Align.CENTER)
        self.grid.set_valign(Gtk.Align.CENTER)

        # Connect Signal handlers
        self.leftbutton.connect("clicked", self.on_button_clicked)
        self.leftbutton.connect("color-set", self.on_color_activated, "left")

        self.centerbutton.connect("clicked", self.on_button_clicked)
        self.centerbutton.connect("color-set", self.on_color_activated, "center")

        self.rightbutton.connect("clicked", self.on_button_clicked)
        self.rightbutton.connect("color-set", self.on_color_activated, "right")

        # Grid Setup
        self.grid.attach(self.leftlabel, 0, 1, 1, 1)
        self.grid.attach(self.leftbutton, 0, 0, 1, 1)
        self.grid.attach(self.centerlabel, 1, 1, 1, 1)
        self.grid.attach(self.centerbutton, 1, 0, 1, 1)
        self.grid.attach(self.rightlabel, 2, 1, 1, 1)
        self.grid.attach(self.rightbutton, 2, 0, 1, 1)

        vbox.pack_start(self.grid, True, True, 0)

        # Color Grab
    def on_color_activated(self, widget, region):
        print(region)
        color = widget.get_rgba()
        red = "{0:0{1}X}".format(int(color.red*255),2)
        green = "{0:0{1}X}".format(int(color.green*255),2)
        blue = "{0:0{1}X}".format(int(color.blue*255),2)
        color_string = red + green + blue
        print(color_string)

        if region == "left":
            try:
                with open('/sys/class/leds/system76::kbd_backlight/color_left', 'w') as f_left:
                    f_left.write(color_string)
            except:
                print("Failed to set color")

        if region == "center":
            try:
                with open('/sys/class/leds/system76::kbd_backlight/color_center', 'w') as f_center:
                    f_center.write(color_string)
            except:
                print("Failed to set color")

        if region == "right":
            try:
                with open('/sys/class/leds/system76::kbd_backlight/color_right', 'w') as f_right:
                    f_right.write(color_string)
            except:
                print("Failed to set color")

    def on_button_clicked(self, widget):
        win.show_all()

win = MainWindow()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()
