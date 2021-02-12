import subprocess
from time import sleep
from typing import Dict

from kcc_cli.common import read_file, write_file
from kcc_cli.enums import Position, Mode
from kcc_cli.backlight_paths import ONE_BACKLIGHT_PATH, FOUR_BACKLIGHT_PATH


def get_laptop_model() -> str:
    return subprocess.check_output(['pkexec', 'dmidecode', '-s', 'system-version']).decode('utf-8').strip()


class KeyboardBacklight:
    MODEL_NUMBER_BACKLIGHT_MAPPING = {
        'oryp6': ONE_BACKLIGHT_PATH,
        'oryp4': FOUR_BACKLIGHT_PATH,
        'serw11': FOUR_BACKLIGHT_PATH,
	'serw12': FOUR_BACKLIGHT_PATH,
        # More to come
    }

    def __init__(self):
        self.laptop_model = get_laptop_model()
        keyboard_backlight_paths = self.MODEL_NUMBER_BACKLIGHT_MAPPING.get(
            self.laptop_model,
        )

        if keyboard_backlight_paths is None:
            raise RuntimeError(
                f"{laptop_model} is not supported by this script"
            )

        self.brightness_path = keyboard_backlight_paths['brightness_path']
        self.brightness_color_paths = keyboard_backlight_paths['brightness_color']

        self.mode_functions_mapping = {
            Mode.BREATH: self.breath,
            Mode.STATIC: self.static,
        }

    def breath(self):
        self._ramp_up()
        self._ramp_down()

    def static(self):
        if self._read_brightness() != self.brightness_max_value:
            self._set_full_brightness()

    def set_color(self, color: str, position: Position):
        if not position in self.brightness_color_paths:
            raise RuntimeError(
                f"{position} is not supported for model {self.laptop_model}"
            )
        write_file(self.brightness_color_paths[position], color)

    @property
    def brightness(self) -> int:
        return int(read_file(path=self.brightness_path))

    @brightness.setter
    def brightness(self, value: int):
        write_file(path=self.brightness_path, value=str(value))

    def _ramp_up(self):
        current_brightness = self._read_brightness()
        while current_brightness < self.brightness_max_value:
            self._set_brightness(value=current_brightness)
            current_brightness += 1

    def _ramp_down(self):
        current_brightness = self._read_brightness()
        while current_brightness > self.brightness_min_value:
            self._set_brightness(value=current_brightness)
            current_brightness -= 1

    def update_color(self, color):
        write_file(path=self.brightness_color, value=color)

    def is_multi_region_color(self):
        return len(self.brightness_color_paths) > 1
