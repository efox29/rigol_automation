import time

import numpy as np
import pyvisa


class RigolPowerSupply:

    power_supply_types = ["dp832"]

    def __init__(self, type, visa_desc):
        if type not in self.power_supply_types:
            raise ValueError

        self.type = type
        self.psu = pyvisa.ResourceManager().open_resource(visa_desc)

    def get_type(self):
        return self.type

    def get_channel_state(self, ch):
        return self.psu.query(f"OUTP? CH{ch}").strip()

    def turn_on(self, ch):
        self.psu.write(f":OUTP CH{ch},ON")

    def turn_off(self, ch):
        self.psu.write(f":OUTP CH{ch},OFF")

    def set_levels(self, ch, v, i):
        self.psu.write(f":APPL CH{ch},{v},{i}")

    def get_levels(self, ch):
        level = self.psu.query(f"APPL? CH{ch}")
        level = level.split(",")
        return (float(level[1]), float(level[2]))

    def power_cycle(self, ch, seconds):
        self.turn_off(ch)
        time.sleep(seconds)
        self.turn_on(ch)
