#!/usr/bin/env bash

# This assumes that you only downloaded the install.sh and not the entire repository.

echo "Ensuring python3 is installed..."
sudo apt update && sudo apt install python3

echo "Installing pip dependencies..."
pip3 install --user BeautifulSoup4 lxml

echo "Cloning repository..."
git clone https://github.com/WhonderWy/my-AQI-Script.git

echo "Creating link..."
ln my-AQI-Script/AQI_not.py ~/.local/bin/AQI

echo "Complete. Restart or source relevant bashrc or zshrc in order to run AQI from anywhere."

echo "In the meantime, I'll run it and see if it works."
my-AQI-Script/AQI_not.py
