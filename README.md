# New South Wales Air Quality Index Scraper

A very simple script I wrote so I would not need to visit the [website](https://airquality.environment.nsw.gov.au/aquisnetnswphp/getPage.php?reportid=1 "Environment NSW's Official Air Quality Index Table") myself and look for the relevant cell in the table.

## Current Goals

* Have it run on a timer so I don't need to run the script whenever I need it.
* Test with the other sites so the settings configurations actually work. I.e. Test a lot.
* Interface it with the notification APIs available to the systems I have access to (namely Windows and Ubuntu).

## Requirements

See requirements.txt for more details or see the script itself.

In short, namely BeautifulSoup. It's a simple script.

## Usage

Just run `./AQI_not.py` from the terminal.

## Changelog

2019-12-20 - 0.1 "It WORKS!" - Released to public

2019-12-21 - 0.1b "Now on WINDOWS!" - Light tests to confirm working on Windows. Notification also sort of works.

## Licence

Probably GPL because I use BeautifulSoup. Let me learn more...
