#!/usr/bin/env python

import argparse
import json
import os
import subprocess

import rigol

CONFIG_FILE = "rigol_config.json"


def get_visa_from_config():
    config = open(CONFIG_FILE)
    data = json.load(config)
    config.close()

    return data["visa_desc"]


def get_psu():
    return rigol.RigolPowerSupply("dp832", get_visa_from_config())


parser = argparse.ArgumentParser(description="log parser")


parser.add_argument(
    "-i",
    "--init",
    action="store_true",
    help="init power supply",
)

parser.add_argument(
    "-s",
    "--state",
    action="store",
    choices={"on", "off"},
    help="state of the channel  ON/OFF",
)

parser.add_argument(
    "-ch",
    "--channel",
    action="store",
    default=3,
    type=int,
    choices={1, 2, 3},
    help="channel to use for operation",
)

parser.add_argument(
    "-on",
    "--on",
    action="store",
    type=int,
    choices={1, 2, 3},
    help="specifiy channel to turn on",
)

parser.add_argument(
    "-off",
    "--off",
    action="store",
    type=int,
    choices={1, 2, 3},
    help="specifiy channel to turn off",
)

parser.add_argument(
    "-r",
    "--read",
    action="store",
    type=int,
    choices={1, 2, 3},
    help="specifiy channel to read",
)

parser.add_argument(
    "--script",
    action="store",
    help="profile to run"
)


args = parser.parse_args()

if args.script:
    psu = get_psu()
    print(f"Config load script {args.script}")
    
   
    exit(0)

if args.init:

    psu = get_psu()
    psu.load_config(CONFIG_FILE)
    print("Config loaded")


if args.state and args.channel:
    # need to make sure we have channel

    psu = get_psu()
    if args.state == "on":

        psu.turn_on(args.channel)
    elif args.state == "off":
        psu.turn_off(args.channel)

    print(f"CH{args.channel} = {args.state}")

if args.read:
    psu = get_psu()
    i = psu.measure_current(args.read)
    print(f"CH{args.read}\tCurrent:{i}")

if args.on:
    psu = get_psu()
    psu.turn_on(args.on)

elif args.off:
    psu = get_psu()
    psu.turn_off(args.off)




