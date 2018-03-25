# Project Horus Test Transmitter
This repository contains a collection of Python and bash scripts to emulate the signals from a range of Project Horus telemetry payloads.

## Hardware
These scripts are intended to be run on a Raspberry Pi, with a 'Wenet' shield (RFM98W with DIO2 connected to the Pi's TXD pin). Refer to the [wenet documentation](https://github.com/projecthorus/wenet/wiki/Wenet-TX-Payload-Instructions#11-radio-module) for more information on this.


## Dependencies
* horuslib (via the [horus_utils repository](https://github.com/projecthorus/horus_utils/)) - Follow the [Headless RPi instructions](https://github.com/projecthorus/horus_utils/wiki/3.-Headless-Raspberry-Pi-Operation), though don't do steps 13/14 (auto-start).
* [wenet](https://github.com/projecthorus/wenet) - Clone this repository to ~/, and follow all the [TX setup instructions](https://github.com/projecthorus/wenet/wiki/Wenet-TX-Payload-Instructions#31-fsk-modulator) up to and including section 3.1.
* [pySX127x](https://github.com/darksidelemm/pySX127x) - Clone this, and copy the entire SX127x subdirectory into this directory.

## Producing Telemetry
### RTTY
RTTY telemetry is transmitted with the following settings:
* Baud Rate: 50 (100 baud doesn't seem to be reliable)
* Framing: 7N2  (7 ASCII bits per character, 2 stop bits)
* Tone Spacing: 470 Hz  (A limitation of the RFM98W's PLL Resolution)

To transmit, run:
```
$ sudo python tx_rtty.py
```

Run `python tx_rtty.py --help` to see what settings can be modified.

### LoRa
TODO

### Wenet
Wenet test images are transmitted using default settings (115kbaud, 441.2 MHz, 50mW).

To transmit, run:
```
$ ./tx_wenet.sh
```
CTRL-C exits.

## Stopping Transmissions
Some of the above scripts don't close the transmitter down cleanly. To shut-down the RFM98W, run:
```
$ ./shutdown_tx.sh
```
