#!/bin/bash
#
# Run the RTTY Emulation script.
# This assumes that all wenet installation instructions have been followed,
# and that test images have been generated, and can be transmitted.
#

# Kill all existing python processes that may be using the RFM98W
sudo killall python
# Run the emulation script.
sudo python emulate_rtty.py