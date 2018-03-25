#!/bin/bash
#
# Run the Wenet 'test tx' script.
# This assumes that all wenet installation instructions have been followed,
# and that test images have been generated, and can be transmitted.
#

# Kill all existing python processes that may be using the RFM98W
sudo killall python
# Navigate to the wenet tx script directory
cd ~/wenet/tx/
# Initialise the RFM98W
sudo python init_rfm98w.py
# Transmit test images
sudo python tx_test_images.py