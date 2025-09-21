"""
main.py: třetí projekt do Engeto Online Python Akademie
author: Kristýna Růžičková
email: krist.ruzickova@gmail.com
"""
import requests
from bs4 import BeautifulSoup as bs
import csv
import argparse

zakl_url = "https://www.volby.cz/pls/ps2017nss/"

#Define functions to get village url, names and codes
def get_parsed_html(url_region):
        response = requests.get(url_region)
        response.raise_for_status()
        return bs(response.text, features="html.parser")

def get_village_urls(parsed_html_reg):
    return [zakl_url + a["href"] for a in parsed_html_reg.select("td.cislo a")]
        
def get_village_codes(parsed_html_reg):
    return [codes.get_text() for codes in parsed_html_reg.select("td.cislo a")] 

def get_name(parsed_html_reg):
    return [names.get_text() for names in parsed_html_reg.select("td.overflow_name")] 

# Define functions to get election results for each village
def get_registered(parsed_html_vill):
    return parsed_html_vill.find("td", headers="sa2")

def get_envelopes(parsed_html_vill):
    return parsed_html_vill.find("td", headers="sa3")

def get_valid_votes(parsed_html_vill):
    return parsed_html_vill.find("td", headers="sa6")

def get_party(parsed_html_vill):
    return [party.get_text() for party in parsed_html_vill.find_all("td", headers="t1sa1 t1sb2")]

def get_votes_for_party(parsed_html_vill):
    return [party.get_text() for party in parsed_html_vill.find_all("td", headers="t1sa2 t1sb3")]

# Define script parameters
parser = argparse.ArgumentParser()
parser.add_argument("url_region", type = str, help=" Give url of selected region.")
parser.add_argument("file_name", help = "Give a file name for extracting results in csv format.")

args = parser.parse_args()
print("Url:", args.url_region)
print("Filename:", args.file_name)

# Check for correct parameters
try:
    if "csv" in args.url_region:
        raise ValueError("Check position of arguments, first give url then file name.")

    if not args.file_name.endswith(".csv"):
        raise ValueError("Give a file name in correct format. Example of file name:\"Prerov_results.csv\". ")

    if not args.url_region.startswith("https://www.volby.cz/pls/ps2017nss/"):
        raise ValueError("Give correct url. Example: \"https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=9&xnumnuts=5301\"")
        
except ValueError as e:
    print(e)
    exit()

url_region = args.url_region

# Create csv file
csv_soubor = open(args.file_name, mode="w", encoding="UTF-8", newline ="")

# Call functions to get village urls, check for exceptions
try:
    parsed_html_reg = get_parsed_html(url_region)
except requests.exceptions.RequestException as e:
    print(f"Error while loading URL: {e}")
    exit()
try: 
    village_urls = get_village_urls(parsed_html_reg)
except AttributeError:
        print("No url available.")
        exit()
        
# Call functions to get village codes and names
codes = get_village_codes(parsed_html_reg)
locations = get_name(parsed_html_reg)

# Define a for loop
for idx, url in enumerate(village_urls):
    codes[idx]
    locations[idx]

    # Call function to get parsed html
    parsed_html_vill = get_parsed_html(url)

    # Call functions to get election results
    registered = get_registered(parsed_html_vill).get_text() 
    envelopes = get_envelopes(parsed_html_vill).get_text()
    valid_votes = get_valid_votes(parsed_html_vill).get_text()
    parties = get_party(parsed_html_vill)
    votes_for_party = get_votes_for_party(parsed_html_vill)

    # Create dictionary for csv file
    row = {
        "Codes": codes[idx],
        "Location": locations[idx],
        "Registered": registered,
        "Envelopes": envelopes,
        "Valid": valid_votes,
    }
    row.update(dict(zip(parties, votes_for_party)))
    print(row)

    # Write results in csv file
    if url == village_urls[0]:
        zapisovac = csv.DictWriter(csv_soubor, fieldnames=row.keys(), delimiter=";")
        zapisovac.writeheader()
    zapisovac.writerow(row)
csv_soubor.close()

