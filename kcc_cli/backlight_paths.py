from kcc_cli.enums import Position


ONE_BACKLIGHT_PATH = {
    'brightness_path': '/sys/class/leds/system76_acpi::kbd_backlight/brightness',
    'brightness_color': {
        Position.CENTER: '/sys/class/leds/system76_acpi::kbd_backlight/color',
    }
}


THREE_BACKLIGHT_PATH = {
    'brightness_path': '/sys/class/leds/system76::kbd_backlight/brightness',
    'brightness_color': {
        Position.LEFT: '/sys/class/leds/system76::kbd_backlight/color_left',
        Position.CENTER: '/sys/class/leds/system76::kbd_backlight/color',
        Position.RIGHT: '/sys/class/leds/system76::kbd_backlight/color_right',
    }
}
