#!/usr/bin/env python3

# Original Author: William
# Date created: 2019-12-12
# Version: 2020-01-26 version 0.1l "Colours and LOCATIONS!"
# Reason: The air quality settled down around my area and I wasn"t worrying about breathing for once so I considered writing a simple script.
# What this does:
# A simple script that outputs necessary data to terminal or elsewhere based on config.

from bs4 import BeautifulSoup

settings = {}
current_time = None
CONFIG = "$HOME/.local/AQI_config.json"
PREVIOUS = "$HOME/.local/AQI_previous_values.json"
# DEFAULT = "."
W_CONFIG = "$APPDATA\AQI\AQI_config.json"
W_PREVIOUS = "$APPDATA\AQI\AQI_previous_values.json"
# Can also use $XDG_DATA_HOME and $XDG_CONFIG_HOME if you know what it is (https://stackoverflow.com/questions/1024114/location-of-ini-config-files-in-linux-unix)
# Windows: $HOME to $USERPROFILE or $APPDATA with $XDG_DATA_DIRS pointing to :$APPDATA:$PROGRAMDATA

template = "template_AQI_config.json"

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
    import json, os, platform

    global settings

    osName = platform.system()
    if osName == "Linux":
        if CONFIG.find("HOME"):
            location = os.path.expandvars(CONFIG)
        elif CONFIG.find("~"):
            location = os.path.expanduser(CONFIG)
        else:
            location = CONFIG
    elif osName == "Windows":
        if CONFIG.find("%"):
            location = os.path.expandvars(W_CONFIG)
        elif CONFIG.find("USER"):
            location = os.path.expanduser(W_CONFIG)
        else:
            location = W_CONFIG

    flag = True
    while flag is True:
        try:
            with open(location, "r+") as config:
                settings = json.load(config)
            flag = False
        except:
            import shutil
            if not os.path.exists(location[:-15]):
                os.makedirs(location[:-15])
            for root, dirs, files in os.walk("."):
                global template
                if template in files:
                    template = os.path.join(root, template)
                    break
            shutil.copy(template, location)


def print_config():
    for field in settings:
        print(f"{field}: {settings[field]}.")


# pls help, func not descriptive enough.
def get_html():
    import requests

    html_data = requests.get(str(settings["site"]))

    return html_data.text


def save_html():
    html_data = get_html()
    with open("index.html", "w+") as html:
        html.write(html_data)


# Reads the values from the table.
def get_values():
    global fields, current_time
    import datetime

    soup = BeautifulSoup(markup=get_html(), features="lxml")

    current_time = datetime.datetime.now().strftime("%c")

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

    import json, datetime, os, platform

    location = None

    osName = platform.system()
    if osName == "Linux":
        if CONFIG.find("HOME"):
            location = os.path.expandvars(CONFIG)
        elif CONFIG.find("~"):
            location = os.path.expanduser(CONFIG)
        else:
            location = CONFIG
    elif osName == "Windows":
        if CONFIG.find("%"):
            location = os.path.expandvars(W_CONFIG)
        elif CONFIG.find("USER"):
            location = os.path.expanduser(W_CONFIG)
        else:
            location = W_CONFIG

    now = datetime.datetime.now().strftime("%c")

    with open(location, "a+") as store:
        if not "date" in fields:
            fields["date"] = current_time
        json.dump(fields, store)


# https://stackoverflow.com/a/26665998/12408018
terminalColour = {
    "VERY GOOD": "\x1b[38;2;49;173;211m",  # 74
    "GOOD": "\x1b[38;2;153;185;100m",  # 150
    "FAIR": "\x1b[38;2;255;210;54m",  # 221
    "POOR": "\x1b[38;2;236;120;58m",  # 209
    "VERY POOR": "\x1b[38;2;120;45;73m",  # 95
    "HAZARDOUS": "\x1b[38;2;208;71;48m",  # 167
    "RESET": "\x1b[0m",
}


def print_scale():
    import sys

    for key in terminalColour:
        if key != "RESET":
            sys.stdout.write(f"{terminalColour[key]}{key}{terminalColour['RESET']} ")
    sys.stdout.write("\b\n")


def format_colour(field, scale, value):
    return f"{field:<20} is {terminalColour[scale]}{scale:^10}{terminalColour['RESET']} at {terminalColour[scale]}{value:>5}{terminalColour['RESET']}"


def print_data(coloured=True):
    global fields
    
    scale = None

    get_values()
    if coloured or settings["colour"]:
        print_scale()
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
        if coloured or settings["colour"]:
            string = format_colour(field, scale, value)
        else:
            string = f"{field:<20} is {scale:^10} at {value:>5}"
        print(string)


def send_notification():
    import platform

    get_values()
    string = None

    osName = platform.system()
    if osName == "Linux":
        ubuntu_notification()
    elif osName == "Windows":
        windows_notification()
    else:
        pass


def windows_notification():
    from win10toast import ToastNotifier

    toaster = ToastNotifier()
    title = None
    string = None
    toaster.show_toast("AQI from:", current_time)
    for field in fields:
        value = fields[field]
        try:
            value = int(value)
        except:
            if len(value) == 0:
                title = f"{field} could not be determined"
            else:
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
    s.call(["notify-send", "AQI from:", current_time])
    for field in fields:
        value = fields[field]
        try:
            value = int(value)
        except:
            if len(value) == 0:
                title = f"{field} could not be determined"
            else:
                title = f"Air Quality Index for {field}: {value}"
            continue
        for level in SCALE:
            if value <= SCALE[level]:
                scale = level
                break
            elif value >= SCALE[level]:
                scale = level
        string = f"{field} is {scale} at {value}\n"
        s.call(["notify-send", title, string])


def change_settings(*args):
    # read_config()
    # if "-l" in args:
    pass


def timer(time=60):
    from apscheduler.schedulers.blocking import BlockingScheduler

    scheduler = BlockingScheduler()
    # scheduler.add_job(send_notification(), "interval", minutes=time)
    scheduler.add_job(print_data(), "interval", seconds=time)
    scheduler.start()

    # try:
    #     while True:
    #         import time
    #         time.sleep(2)
    # except (KeyboardInterrupt, SystemExit):
    #     scheduler.shutdown()


# https://stackoverflow.com/a/27529806/12408018
FUNCTION_MAP = {
    "print": print_data,
    "settings": print_config,
    "save": save_values,
    "html": save_html,
    "notify": send_notification,
    # "auto": timer
}


def read_args():
    import argparse

    parser = argparse.ArgumentParser(
        prog="myAQIScript - Air Quality Index Notifier",
        description="An easy way to see only the information I want to see.",
    )

    # Lets one use call a specific function
    parser.add_argument("-c", "--command", choices=FUNCTION_MAP.keys(), required=False)
    # Lets one immediately parse in a different location
    parser.add_argument("-l", "--location", required=False)
    parser.add_argument("-nc", "--no-colour", required=False, action="store_true")

    # subs = parser.add_subparsers()

    # parse_print = subs.add_parser("print")
    # parse_print.add_argument("-p")
    # parse_print.add_argument("--print")
    # parse_print.add_argument("print")
    # parse_print.set_defaults(func=print_data)

    # parse_settings = subs.add_parser("settings")
    # parse_print.add_argument("-c")
    # parse_print.add_argument("--settings")
    # parse_print.add_argument("settings")
    # parse_print.set_defaults(func=print_config)

    # parse_save = subs.add_parser("save")
    # parse_print.add_argument("-s")
    # parse_print.add_argument("--save")
    # parse_print.add_argument("save")
    # parse_print.set_defaults(func=save_values)

    args = parser.parse_args()
    read_config()
    if args.location:
        settings["location"] = args.location
    if args.command:
        func = FUNCTION_MAP[args.command]
        func()
    # elif args.func(args):
    #     args.func(args)
    elif args.no_colour:
        settings["colour"] = False
        print_data(coloured=False)
    else:
        print_data()


if __name__ == "__main__":
    read_args()
    # print_data()
    # send_notification()
    # save_values()
