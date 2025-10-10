#election_scraper_env\Scripts\Activate

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

def get_election_results(parsed_html_vill, codes, locations):
    return{
    "Codes": codes,
    "Location": locations,
    "Registered": get_registered(parsed_html_vill).get_text(), 
    "Envelopes": get_envelopes(parsed_html_vill).get_text(),
    "Valid_votes": get_valid_votes(parsed_html_vill).get_text(),
    }

def save_results_to_csv(results, filename="vysledky.csv"):
    with open(filename, mode="w", newline="", encoding="utf-8") as csv_soubor:
        zapisovac = csv.DictWriter(csv_soubor, fieldnames=results[0].keys(), delimiter=";")
        zapisovac.writeheader()
        zapisovac.writerows(results)

def getArgs(args=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("url_region", type = str, help=" Give url of selected region.")
    parser.add_argument("file_name", help = "Give a file name for extracting results in csv format.")
    return parser.parse_args(args)

def print_parameters():
    print("Url:", args.url_region)
    print("Filename:", args.file_name)
    
args = getArgs()
url_region = args.url_region
file_name = args.file_name

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

# Check for exceptions 
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

codes = get_village_codes(parsed_html_reg)
locations = get_name(parsed_html_reg)

results = []

for idx, url in enumerate(village_urls):
    parsed_html_vill = get_parsed_html(url)
    data = get_election_results(parsed_html_vill, codes[idx], locations[idx])
    parties = get_party(parsed_html_vill)
    votes_for_party = get_votes_for_party(parsed_html_vill)
    data.update(dict(zip(parties, votes_for_party)))
    results.append(data)
    
save_results_to_csv(results, file_name)



