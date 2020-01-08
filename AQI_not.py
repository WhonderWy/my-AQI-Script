#!/usr/bin/env python3

# Original Author: William
# Date created: 2019/12/12
# Version: 2019/12/20 version 0.1 "It WORKS!"
# Reason: The air quality settled down around my area and I wasn"t worrying about breathing for once so I considered writing a simple script.
# What this does:
# A simple script that outputs necessary data to terminal or elsewhere based on config.

from bs4 import BeautifulSoup

settings = {}
current_time = None
CONFIG = "$HOME/.local/AQI_config.json"
PREVIOUS = "$HOME/.local/AQI_previous_values.json"

SCALE = {
    "VERY GOOD": 33,
    "GOOD": 66,
    "FAIR": 99,
    "POOR": 149,
    "VERY POOR": 199,
    "HAZARDOUS": 200,
    # "scale": 33,
}

fields = {
    "Site Name": None,
    "Ozone O3 hourly": None,
    "Ozone O3 four hourly": None,
    "Nitrogen Dioxide NO2": None,
    "Visibility NEPH": None,
    "Carbon Monoxide CO2": None,
    "Sulfur Dioxide SO2": None,
    "Particles PM10": None,
    "Particles PM2.5": None,
    "Site AQI": None,
    "Regional AQI": None,
}



def read_config():
    import json, os

    global settings

    if CONFIG.find("HOME"):
        location = os.path.expandvars(CONFIG)
    elif CONFIG.find("~"):
        location = os.path.expanduser(CONFIG)
    else:
        location = CONFIG

    with open(location, "r+") as config:
        settings = json.load(config)


def print_config():
    for field in settings:
        print(field)


# pls help, func not descriptive enough.
def get_html():
    import requests

    html_data = requests.get(str(settings["site"]))

    return html_data.text


# Reads the values from the table.
def get_values():
    global fields, current_time
    import datetime

    soup = BeautifulSoup(markup=get_html(), features="lxml")
    current_time = datetime.datetime.utcnow().strftime("%c")
    table = soup.find_all("table", class_="aqi")[0]
    targets = table.find_all("tr")

    for row in targets:
        if row.text.find(settings["location"]) != -1:
            text = row.text.splitlines()
            text.remove("")
            for line, key in zip(text, fields):
                fields[key] = line
            break


# Needs to be run after print_data() lest you print the date field too...
def save_values():
    global fields

    import json, datetime, os

    if CONFIG.find("HOME"):
        location = os.path.expandvars(PREVIOUS)
    elif CONFIG.find("~"):
        location = os.path.expanduser(PREVIOUS)
    else:
        location = PREVIOUS

    now = datetime.datetime.now().strftime("%c")

    with open(location, "a+") as store:
        if not "date" in fields:
            fields["date"] = current_time
        json.dump(fields, store)


def print_data():
    global fields
    scale = None
    get_values()
    print(current_time)
    for field in fields:
        value = fields[field]
        try:
            value = int(value)
        except:
            if len(value) == 0:
                print(f"{field:<20} could not be determined")
            else:
                print(f"{field:<20} is {value}")
            continue
        for level in SCALE:
            if value <= SCALE[level]:
                scale = level
                break
            elif value >= SCALE[level]:
                scale = level
        string = f"{field:<20} is {scale:^10} at {value:>5}"
        print(string)


def send_notification():
    import platform

    get_values()
    string = None

    osName = platform.system()
    if osName == "Linux":
        pass
    elif osName == "Windows":
        windows_notification()
    else:
        pass


def windows_notification():
    from win10toast import ToastNotifier

    toaster = ToastNotifier()
    title = None
    string = None
    for field in fields:
        value = fields[field]
        try:
            value = int(value)
        except:
            title = f"Air Quality Index for {field}: {value}"
            continue
        for level in SCALE:
            if value <= SCALE[level]:
                scale = level
                break
            elif value >= SCALE[level]:
                scale = level
        string = f"{field} is {scale} at {value}\n"
        toaster.show_toast(title, string)


def ubuntu_notification():
    import subprocess as s

    title = None
    string = None
    for field in fields:
        value = fields[field]
        try:
            value = int(value)
        except:
            title = f"{field:<20} is {value}"
            continue
        for level in SCALE:
            if value <= SCALE[level]:
                scale = level
                break
            elif value >= SCALE["HAZARDOUS"]:
                scale = "HAZARDOUS"
                break
        string += f"{field:<20} is {scale:^10} at {value:>5}\n"
    s.call(["notify-send", title, string])


def timer(time=60):
    from apscheduler.schedulers.blocking import BlockingScheduler

    scheduler = BlockingScheduler()
    scheduler.add_job(send_notification(), "interval", minutes=time)
    scheduler.start()


# https://stackoverflow.com/a/27529806/12408018
FUNCTION_MAP = {
    "print": print_data,
    "settings": print_config,
    "save": save_values
}

def read_args():
    import argparse

    parser = argparse.ArgumentParser(prog="myAQIScript - Air Quality Index Notifier", description="An easy way to see only the information I want to see.")
    parser.add_argument("-command", choices=FUNCTION_MAP.keys(), required=False)

    args = parser.parse_args()
    if args.command:
        func = FUNCTION_MAP[args.command]
        func()
    else:
        print_data()


if __name__ == "__main__":
    read_config()
    read_args()
    # print_data()
    # send_notification()
    # save_values()
