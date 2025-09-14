"""
main.py: třetí projekt do Engeto Online Python Akademie
author: Kristýna Růžičková
email: krist.ruzickova@gmail.com
"""

# if __name == "__main__" (lekce 11)

import requests
from bs4 import BeautifulSoup as bs
import csv
import argparse

zakl_url = "https://www.volby.cz/pls/ps2017nss/"

#Define functions to get village names and codes
def get_parsed_response(url_region):
    return bs(requests.get(url_region).text, features="html.parser")

def get_all_a(split_text):
    return [a["href"]for a in split_text.select("td.cislo a")] 

def get_village_url(url_list):
    return[zakl_url + u for u in url_list]

def get_village_codes(split_text):
    return [codes.get_text() for codes in split_text.select("td.cislo a")] 

def get_name(split_text):
    return [names.get_text() for names in split_text.select("td.overflow_name")] 

   
# Define functions to get election results
def get_registered(split_text_2):
    return split_text_2.find("td", headers="sa2")

def get_envelopes(split_text_2):
    return split_text_2.find("td", headers="sa3")

def get_valid_votes(split_text_2):
    return split_text_2.find("td", headers="sa6")

def get_party(split_text_2):
    return [party.get_text() for party in split_text_2.find_all("td", headers="t1sa1 t1sb2")]

def get_votes_for_party(split_text_2):
    return [party.get_text() for party in split_text_2.find_all("td", headers="t1sa2 t1sb3")]

# Definition of script parameters
parser = argparse.ArgumentParser()
parser.add_argument("url_region", type = str, help=" Give url of selected region.")
parser.add_argument("file_name", help = "Give a file name for extracting results in csv format.")

args = parser.parse_args()
print("Url:", args.url_region)
print("Filename:", args.file_name)

# Check for correct parameters
if "csv" in args.url_region:
    print("Check position of arguments, first give url then file name.")
    exit()

if "csv" not in args.file_name:
    print("Example of file name:\"Prerov_results.csv\". ")
    exit()

if "https://www.volby.cz/pls/ps2017nss/" not in args.url_region:
    print("Give correct url. Example: \"https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=9&xnumnuts=5301\"")
    exit()

url_region = args.url_region

# Create csv file
csv_soubor = open(args.file_name, mode="w", encoding="UTF-8", newline ="")

# Call functions to get village codes and names
split_text = get_parsed_response(url_region)
# Get url for all village codes
urls = get_all_a(split_text)
print(urls)
village_urls = get_village_url(urls)
codes = get_village_codes(split_text)
locations = get_name(split_text)

for idx, url in enumerate(village_urls):
    codes[idx]
    locations[idx]

    # Call functions to get election results
    split_text_2 = get_parsed_response(url)

    registered = get_registered(split_text_2).get_text()
    envelopes = get_envelopes(split_text_2).get_text()
    valid_votes = get_valid_votes(split_text_2).get_text()

    parties = get_party(split_text_2)
    votes_for_party= get_votes_for_party(split_text_2)
    # Create dictionary for number of votes for each party
    parties_with_votes_dict = dict(zip(parties, votes_for_party))

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
        zapisovac = csv.DictWriter(csv_soubor,fieldnames=row.keys(), delimiter=";")
        zapisovac.writeheader()
    zapisovac.writerow(row)
csv_soubor.close()
