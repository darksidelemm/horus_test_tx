#!/usr/bin/env python
#
# 	RTTY Emulation using a RFM98W
#
#   Copyright (C) 2018  Mark Jessop <vk5qi@rfhead.net>
#   Released under GNU GPL v3 or later
#
#	Requires pySX127x:
#	https://github.com/darksidelemm/pySX127x
#   Copy the SX127x directory into this directory... 
#
#	Uses spidev for comms with a RFM98W module.
#
#	SPI: Connected to CE0 (like most of my LoRa shields)
#	RPi TXD: Connected to RFM98W's DIO2 pin.
#
import sys
import crcmod
import datetime
import random
import serial
import time
import argparse
from SX127x.LoRa import *
from SX127x.hardware_piloragateway import HardwareInterface

# Emulated payload position.
LAT = -34.9741
LON = 138.7089
ALT = 710
SATS = 8

# How much to twiddle the lat/long by between transmissions.
RANDOM_FACTOR = 0.0005


def setup_rfm98w(frequency=434.650, spi_device=0, shutdown=False):
    # Set this to 1 if your RFM98W is on CE1
    hw = HardwareInterface(spi_device)

    # Start talking to the module...
    lora = LoRa(hw)
    
    # Set us into FSK mode, and set continuous mode on
    lora.set_register(0x01,0x00) # Standby Mode
    # If we have been asked to shutdown the RFM98W, then exit here.
    if shutdown:
        print("Transmitter shutdown.")
        sys.exit(0)

    # Otherwise, proceed.
    lora.set_register(0x31,0x00) # Set Continuous Mode
    
    # Set TX Frequency
    lora.set_freq(frequency)

    # Set Deviation (~470 Hz)
    lora.set_register(0x04,0x00)
    lora.set_register(0x05,0x04)
  
    # Set Transmit power to 50mW.
    # NOTE: If you're in another country you'll probably want to modify this value to something legal...
    lora.set_register(0x09,0x8F)

    # Go into TX mode.
    lora.set_register(0x01,0x02) # .. via FSTX mode (where the transmit frequency actually gets set)
    lora.set_register(0x01,0x03) # Now we're in TX mode...


def crc16_ccitt(data):
    """
    Calculate the CRC16 CCITT checksum of *data*.
    (CRC16 CCITT: start 0xFFFF, poly 0x1021)
    """
    crc16 = crcmod.predefined.mkCrcFun('crc-ccitt-false')
    return hex(crc16(data))[2:].upper().zfill(4)


def create_string(callsign, sequence_no, time_dt, lat, lon, alt, sats):
    ''' Generate a HORUS compatible RTTY string '''
    _time = time_dt.strftime("%H:%M:%S")
    _telem = "$$%s,%d,%s,%.4f,%.4f,%d,0,%d,1500,25" % (callsign, sequence_no, _time, lat, lon, alt, sats)
    _checksum = crc16_ccitt(_telem[2:])
    return _telem + "*" + _checksum


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--frequency", default=434.650, type=float, help="Transmit Frequency (MHz). Default = 434.650 MHz.")
    parser.add_argument("--spidevice", default=0, type=int, help="LoRa SPI Device number. Default = 0.")
    parser.add_argument("--shutdown",action="store_true", help="Shutdown Transmitter instead of activating it.")
    parser.add_argument("--callsign", type=str, default="HORUS", help="Callsign for RTTY telemetry.")
    parser.add_argument("--serial_port", type=str, default='/dev/ttyAMA0', help='Serial port for RTTY.')
    parser.add_argument('--serial_baud', type=int, default=50, help='Baud rate for RTTY.')
    args = parser.parse_args()

    tx_freq = args.frequency

    if tx_freq>450.0 or tx_freq<430.00:
        print("Frequency out of 70cm band, using default.")
        tx_freq = 434.650

    print("Initialising RFM98W transmitter...")
    setup_rfm98w(frequency=tx_freq, spi_device=args.spidevice, shutdown=args.shutdown)

    print("Initialising Serial Port...")
    s = serial.Serial(args.serial_port, args.serial_baud, bytesize=serial.SEVENBITS, stopbits=serial.STOPBITS_TWO)

    i = 0
    while True:
        _packet_time = datetime.datetime.utcnow()
        _lat = LAT+(random.random()-0.5)*RANDOM_FACTOR
        _lon = LON+(random.random()-0.5)*RANDOM_FACTOR
        _str = create_string(args.callsign,i,_packet_time,_lat,_lon,ALT,SATS) + '\n\n\n'
        print(_str)
        s.write(_str)
        time.sleep(20)     
        i += 1    

    sys.exit(0)


