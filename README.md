# New South Wales Air Quality Index Scraper

A very simple script I wrote so I would not need to visit the [website](https://airquality.environment.nsw.gov.au/aquisnetnswphp/getPage.php?reportid=1 "Environment NSW's Official Air Quality Index Table") myself and look for the relevant cell in the table.

## Current Goals

* ~~Have it run on a timer so I don't need to run the script whenever I need it.~~ Just run it as a cron job.
* Test with the other sites so the settings configurations actually work. I.e. Test a lot.
* Interface it with the notification APIs available to the systems I have access to (namely Windows and Ubuntu). As of 0.1b, only needs testing.

## Requirements

See requirements.txt for more details or see the script itself.  
In short, namely BeautifulSoup. It's a simple script.

## Usage

Just run `./AQI_not.py` from the terminal.

## Changelog

2019-12-20 - 0.1 "It WORKS!" - Released to public.\
2019-12-21 - 0.1b "Now on WINDOWS!" - Light tests to confirm working on Windows. Notification also sort of works.\
2020-01-01 - 0.1d "2019 is HISTORY!" - Previous values are now saved. If table cell is empty, it won't print nothing anymore.\
2020-01-03 - 0.1e "Source: BUSHFIRE!" - Users can now clone repository and link it anywhere they want so long. Default configuration location is `$HOME/.local/AQI_config.json`. An `install.sh` also exists now. Not sure if it works though.\
2020-01-08 - 0.1f "/Totally/ on TIME!" - Now includes time the data is more or less from in console.\
2020-01-08 - 0.1g "No GUI but now with OPTIONS!" - You can now print the data, settings and save the data from the command line!.\
2020-01-08 - 0.1h "HTML not HTM" - HTML file of page is now stored.\
2020-01-26 - 0.1l "Colours and LOCATIONS!" - Exact(?) colours used on the site is now displayed. `"-l"` as an argument followed by place name will override the location in the configuration.\
2020-01-27 - 0.1m "m is the new WINDOWS support!" - It should work better with Windows now. May or may not have broken it previously when I added the function to auto-create configuration at desired location.

## Licence

Probably GPL because I use BeautifulSoup. Let me learn more...
