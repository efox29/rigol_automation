# from rigol import RigolPowerSupply
import time
from timeit import default_timer as timer

import pytest

from src import rigol

DP832_SERIAL = "USB0::0x1AB1::0x0E11::DP8C231401286::INSTR"


@pytest.fixture
def dp832():
    psu = rigol.RigolPowerSupply("dp832", DP832_SERIAL)

    yield psu

    psu.turn_off(1)
    psu.turn_off(2)
    psu.turn_off(3)


""" TEST BEGIN  """


def test_is_rigol_832():
    power_name = "dp832"
    p = rigol.RigolPowerSupply(power_name, DP832_SERIAL)
    assert p.get_type() == power_name
    pass


def test_power_supply_not_valid_type():
    with pytest.raises(ValueError):
        p = rigol.RigolPowerSupply("ddp832", DP832_SERIAL)


""" TURNING CHANNELS ON / OFF  """


def test_dp832_turn_off_all_channels(dp832):
    for ch in range(1, 4):
        dp832.turn_off(ch)
        assert dp832.get_channel_state(ch) == "OFF"
    time.sleep(1)


def test_dp832_turn_on_all_channels(dp832):
    for ch in range(1, 4):
        dp832.turn_on(ch)
        assert dp832.get_channel_state(ch) == "ON"
    time.sleep(1)


def test_set_channel_1_voltage(dp832):
    ref_v = 10.10
    ref_i = 1.23
    ref_ch = 1
    dp832.set_levels(ref_ch, ref_v, ref_i)
    v, i = dp832.get_levels(ref_ch)
    assert v == ref_v
    assert i == ref_i


def test_set_channel_2_voltage(dp832):
    ref_v = 10.10
    ref_i = 1.23
    ref_ch = 2
    dp832.set_levels(ref_ch, ref_v, ref_i)
    v, i = dp832.get_levels(ref_ch)
    assert v == ref_v
    assert i == ref_i


def test_set_channel_3_voltage(dp832):
    ref_v = 2.9
    ref_i = 1.23
    ref_ch = 3
    dp832.set_levels(ref_ch, ref_v, ref_i)
    v, i = dp832.get_levels(ref_ch)
    assert v == ref_v
    assert i == ref_i


""" fancy features """


"""this one is hard to test because of a blocking time function in power_cycle"""


def test_power_cycle_ch_1(dp832):
    ref_ch = 1
    ref_time = 5
    TIME_THRESHOLD = 0.1
    dp832.turn_on(ref_ch)
    time.sleep(1)
    assert dp832.get_channel_state(ref_ch) == "ON"

    start = timer()
    dp832.power_cycle(1, ref_time)
    end = timer()
    assert (end - start) - TIME_THRESHOLD < ref_time
    assert (end - start) + TIME_THRESHOLD > ref_time
    assert dp832.get_channel_state(ref_ch) == "ON"
    assert dp832.get_channel_state(ref_ch) == "ON"
