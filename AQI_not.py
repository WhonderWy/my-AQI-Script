#!/usr/bin/env python3

# Original Author: William
# Date created: 2019/12/12
# Reason: The air quality settled down around my area and I wasn't worrying about breathing for once so I considered writing a simple script.
# What this does:
# A simple script that outputs necessary data to terminal or elsewhere based on config.

from bs4 import BeautifulSoup

CONFIG = "config.json"
SETTINGS = {}
SCALE = {
    "VERY GOOD": 33,
    "GOOD": 66,
    "FAIR": 99,
    "POOR": 149,
    "VERY POOR": 199,
    "HAZARDOUS": 200,

    "scale": 33
}

# class Settings():
# 	def __init__(self):
# 		pass

def read_config():
    import json
    global SETTINGS

    with open(CONFIG, "w+") as config:
        SETTINGS = json.load(config)

def print_config():
    for field in SETTINGS:
        print(field)

def get_html():
    import requests
    html_data = requests.get(str(SETTINGS["site"]))
    return html_data.text

def get_value():
    soup = BeautifulSoup(markup=get_html(), features="lxml")
    return result

def print_data():
    for field in SETTINGS["interested_fields"]:
        value = get_value()
        print(f"{field}: {value}")



if __name__ == "__main__":
    pass
