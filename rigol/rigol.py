import json
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

    def load_config(self, file):
        config = open(file)
        data = json.load(config)
        config.close()
        # validate the config before continuing
        # TODO: validate the config
        # read config
        for key in data.keys():
            if "ch" in key:
                v = data[key]["volt"]
                i = data[key]["current"]
                ch = int(key[2])
                self.set_levels(ch, v, i)
        return "OK"


# x = RigolPowerSupply("dp832", "USB0::0x1AB1::0x0E11::DP8C231401286::INSTR")
# x.load_config("tests/myconfig.json")
# pass
