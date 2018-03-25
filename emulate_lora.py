#!/usr/bin/env python
#
# 	LoRa Payload Emulation using a RFM98W
#
#   Copyright (C) 2018  Mark Jessop <vk5qi@rfhead.net>
#   Released under GNU GPL v3 or later
#
#   LoRaUDPServer must be running for this script to work.
#
import sys
import datetime
import random
import time
import struct
import argparse
from horuslib.packets import *


# Emulated payload position.
LAT = -34.9741
LON = 138.7089
ALT = 710
SATS = 8

# How much to twiddle the lat/long by between transmissions.
RANDOM_FACTOR = 0.0005


def generate_lora_telemetry(payload_id, sequence_no, time_dt, lat, lon, alt):
    ''' Generate a LoRa Payload Telemetry packet, and transmit it. '''

    horus_format_struct = "<BBBHBBBffHBBBBBBBB"

    _hour = time_dt.hour
    _minute = time_dt.minute
    _second = time_dt.second

    # Generate a telemetry string. Leave most fields at dummy values.
    _telem_string = struct.pack(horus_format_struct,
        HORUS_PACKET_TYPES.PAYLOAD_TELEMETRY,
        0,  # Payload Flags
        payload_id, # Payload ID
        sequence_no,
        _hour,
        _minute,
        _second,
        lat,
        lon,
        alt,
        0,  # Speed
        10, # Sats
        25, # Temperature
        250, # Battery Voltage
        250, # Pyro Voltage
        42, # Received Packets
        160, # RSSI
        0,  # Uplink Slots
        )

    # Print a string representation of the packet.
    print(payload_to_string(_telem_string))

    # Transmit it!
    tx_packet(_telem_string, blocking=False)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--frequency", default=431.650, type=float, help="Transmit Frequency (MHz). Default = 434.650 MHz.")
    args = parser.parse_args()

    tx_freq = args.frequency

    if tx_freq>450.0 or tx_freq<430.00:
        print("Frequency out of 70cm band, using default.")
        tx_freq = 431.650

    print("Setting frequency to %.3f MHz" % tx_freq)
    update_frequency(tx_freq)


    i = 0
    while True:
        _packet_time = datetime.utcnow()
        _lat = LAT+(random.random()-0.5)*RANDOM_FACTOR
        _lon = LON+(random.random()-0.5)*RANDOM_FACTOR
        
        generate_lora_telemetry(1,i,_packet_time,_lat,_lon,ALT)

        time.sleep(5)     
        i += 1    

    sys.exit(0)


