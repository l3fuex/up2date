#!/usr/bin/python3

import platform
import logging
from datetime import datetime
import calendar
import re
import requests
from bs4 import BeautifulSoup

logging.basicConfig(
    level=logging.INFO, format="%(levelname)-8s %(message)s"
)


def detect_system():
    os = version = None

    if platform.system() == "Linux":
        with open("/etc/os-release") as f:
            for line in f:
                if line.split("=")[0] == "ID":
                    os = line.split("=")[1].strip()
                if line.split("=")[0] == "VERSION_ID":
                    version = line.split("=")[1].strip("\"\n")

    if platform.system() == "Darwin":
        os = "MacOS"
        version = platform.mac_ver()[0]

    if platform.system() == "Windows":
        os = "Windows"
        version = platform.release()

    return os, version


def table_scraper(url, tblnbr=0):
    table = []

    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    rawtable = soup.find_all("table")[tblnbr]
    tablerow = rawtable.find_all("tr")
    for row in tablerow[1:]:
        tabledata = row.find_all("td")
        rowlist = [data.text.strip() for data in tabledata]
        table.append(rowlist)

    return table


def debian_table_parser(table):
    # remove unnecessary data
    for data in table:
        del data[1:4]
        del data[2:]


def ubuntu_table_parser(table):
    # remove unnecessary data
    for data in table:
        del data[1]
        del data[2:]

    for data in table:
        # convert version string to number only
        data[0] = data[0].split(" ")[0]

        # convert date format
        date = datetime.strptime(data[1], "%b %Y")
        day = calendar.monthrange(date.year, date.month)[1]
        date = datetime(date.year, date.month, day)
        data[1] = date.strftime("%Y-%m-%d")


def win_table_parser(table):
    # remove unnecessary data
    del table[0][1]

    # convert version string to number only
    match = re.search(r"([\d.]+)", table[0][0])
    table[0][0] = match.group()

    # convert date format
    if table[0][1] == "In Support":
        table[0][1] = "TBA"
    else:
        date = datetime.fromisoformat(table[0][1])
        table[0][1] = date.strftime("%Y-%m-%d")


def main():
    # Determine OS and Version
    os, version = detect_system()
    if None in (os, version):
        logging.error("Could not determine operating system or version.")
        raise SystemExit(2)

    # Retrieve lifecycle data for given OS
    if os == "debian":
        url="https://www.debian.org/releases/"
        dataref = table_scraper(url)
        debian_table_parser(dataref)

    elif os == "ubuntu":
        url="https://ubuntu.com/about/release-cycle"
        dataref = table_scraper(url)
        ubuntu_table_parser(dataref)

    elif os == "Windows" and version == "11":
        url="https://learn.microsoft.com/en-us/lifecycle/products/windows-11-home-and-pro"
        dataref = table_scraper(url)
        win_table_parser(dataref)

    elif os == "Windows" and version == "10":
        url="https://learn.microsoft.com/en-us/lifecycle/products/windows-10-home-and-pro"
        dataref = table_scraper(url)
        win_table_parser(dataref)

    elif os == "Windows" and version == "8.1":
        url="https://learn.microsoft.com/en-us/lifecycle/products/windows-81"
        dataref = table_scraper(url)
        win_table_parser(dataref)

    elif os == "Windows" and version == "7":
        url="https://learn.microsoft.com/en-us/lifecycle/products/windows-7"
        dataref = table_scraper(url)
        win_table_parser(dataref)

    else:
        logging.error("%s %s is currently not supported.", os, version)
        raise SystemExit(2)

    # Get EOS date for given OS version
    eosdate = None
    for data in dataref:
        if data[0] == version:
            eosdate = data[1]

    if eosdate is None:
        logging.error("Could not find corresponding EOS date.")
        raise SystemExit(2)

    print(f"{os} {version} EOS date: {eosdate}")


if __name__ == "__main__":
    main()
