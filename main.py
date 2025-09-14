"""
main.py: třetí projekt do Engeto Online Python Akademie
author: Kristýna Růžičková
email: krist.ruzickova@gmail.com
"""

# sys knihovna, if __name == "__main__" (lekce 11)

import requests
from bs4 import BeautifulSoup as bs
import sys
import csv
import argparse
import sys
from typing import Optional

parser = argparse.ArgumentParser()
parser.add_argument("url_region", type = str, help=" Give url of selected region.")
parser.add_argument("file_name", help= "Give a file name for extracting results in csv format.")

args = parser.parse_args()
print("Url:", args.url_region)
print("Filename:", args.file_name)

if "csv" in args.url_region:
    print("Check position of argumests, first give url then file name.")
    exit()

if "https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=11&xnumnuts" not in args.url_region:
    print("Give correct url")
    exit()

#Define functions to get village names and codes
url_region = "https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=11&xnumnuts=6204"

def get_parsed_response(url_region):
    return bs(requests.get(url_region).text, features="html.parser")

def get_village_codes(split_text):
    return [codes.get_text() for codes in split_text.select("td.cislo a")] 

def get_name(split_text):
    return [names.get_text() for names in split_text.select("td.overflow_name")] 
   
# Define functions to get election results
def ziskej_parsovanou_odpoved(url):
    return bs(requests.get(url).text, features="html.parser")

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

# Call functions to get village codes and names
split_text = get_parsed_response(url_region)
village_codes = get_village_codes(split_text)
names = get_name(split_text)

# Create csv file
csv_soubor = open("vysledky_3.csv", mode="a", encoding="UTF-8")

# Get url for all village codes
for idx, code in enumerate(village_codes):
    url = f"https://www.volby.cz/pls/ps2017nss/ps311?xjazyk=CZ&xkraj=11&xobec={code}&xvyber=6204"

    # Call functions to get election results
    split_text_2 = ziskej_parsovanou_odpoved(url)
    location = get_name(split_text_2)
    registered = get_registered(split_text_2).get_text()
    envelopes = get_envelopes(split_text_2).get_text()
    valid_votes = get_valid_votes(split_text_2).get_text()
    parties = get_party(split_text_2)
    votes_for_party= get_votes_for_party(split_text_2)

    # Create dictionary for number of votes for each party
    parties_with_votes_dict = dict(zip(parties, votes_for_party))

    # Create dictionary for csv file
    row = {
        "Codes": code,
        "Location": names[idx],
        "Registered": registered,
        "Envelopes": envelopes,
        "Valid": valid_votes,
    }
    rows = row | parties_with_votes_dict
    print(rows)

    # Write results in csv file
    if idx == 0:
        zapisovac = csv.DictWriter(csv_soubor,fieldnames=rows.keys(), delimiter=";")
        zapisovac.writeheader()
    zapisovac.writerow(rows)

"""
sys.argv(url_uzem_celek, vysledky_breclav)
"""
