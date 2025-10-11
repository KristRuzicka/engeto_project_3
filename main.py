"""
main.py: třetí projekt do Engeto Online Python Akademie
author: Kristýna Růžičková
email: krist.ruzickova@gmail.com
"""

import requests
from bs4 import BeautifulSoup as bs
import csv
import argparse

base_url = "https://www.volby.cz/pls/ps2017nss/"

# Get village url, codes and names
def get_parsed_html(url_region):
        response = requests.get(url_region)
        response.raise_for_status()
        return bs(response.text, features="html.parser")

def get_village_urls(parsed_html_reg):
    return [base_url + a["href"] for a in parsed_html_reg.select("td.cislo a")]
        
def get_village_codes(parsed_html_reg):
    return [codes.get_text() for codes in parsed_html_reg.select("td.cislo a")] 

def get_name(parsed_html_reg):
    return [names.get_text() for names in parsed_html_reg.select("td.overflow_name")] 

# Get election results for each village
def get_registered(parsed_html_vill):
    return parsed_html_vill.find("td", headers="sa2")

def get_envelopes(parsed_html_vill):
    return parsed_html_vill.find("td", headers="sa3")

def get_valid_votes(parsed_html_vill):
    return parsed_html_vill.find("td", headers="sa6")

def get_parties(parsed_html_vill):
    return [parties.get_text() for parties in parsed_html_vill.find_all("td", headers="t1sa1 t1sb2")]

def get_votes_for_parties(parsed_html_vill):
    return [parties.get_text() for parties in parsed_html_vill.find_all("td", headers="t1sa2 t1sb3")]

def get_election_results(parsed_html_vill, codes, locations):
    results = {
    "Codes": codes,
    "Location": locations,
    "Registered": get_registered(parsed_html_vill).get_text(), 
    "Envelopes": get_envelopes(parsed_html_vill).get_text(),
    "Valid_votes": get_valid_votes(parsed_html_vill).get_text(),
    }

    parties = get_parties(parsed_html_vill)
    votes_for_parties = get_votes_for_parties(parsed_html_vill)
    results.update(dict(zip(parties, votes_for_parties)))

    return results

# Save results into a csv file
def save_results_to_csv(results, filename="vysledky.csv"):
    with open(filename, mode="w", newline="", encoding="utf-8") as csv_soubor:
        zapisovac = csv.DictWriter(csv_soubor, fieldnames=results[0].keys(), delimiter=";")
        zapisovac.writeheader()
        zapisovac.writerows(results)

# Retrieve arguments from the command line
def get_args(args=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("url_region", type = str, help=" Give url of selected region.")
    parser.add_argument("file_name", help = "Give a file name for extracting results in csv format.")
    return parser.parse_args(args)

# Check for correct parameters
def validate_args(args):
    if "csv" in args.url_region:
        raise ValueError("Check position of arguments, first give url then file name.")

    if not args.file_name.endswith(".csv"):
        raise ValueError("Give a file name in correct format. Example of file name:\"Prerov_results.csv\". ")

    if not args.url_region.startswith("https://www.volby.cz/pls/ps2017nss/"):
        raise ValueError("Give correct url. Example: \"https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=9&xnumnuts=5301\"")

# main function
def run_scraper(url_region, file_name):
    parsed_html_reg = get_parsed_html(url_region)
    village_urls = get_village_urls(parsed_html_reg)
    codes = get_village_codes(parsed_html_reg)
    locations = get_name(parsed_html_reg)

    results = []

    for idx, url in enumerate(village_urls):
        parsed_html_vill = get_parsed_html(url)
        result = get_election_results(parsed_html_vill, codes [idx], locations[idx])
        results.append(result)
    
    save_results_to_csv(results, file_name)

args = get_args()

try:
    validate_args(args)
    run_scraper(args.url_region, args.file_name)
    print(f"Election results have been save in file: {args.file_name}")

except ValueError as e:
    print(f"Argument error: {e}.")

except requests.exceptions.RequestException as e:
    print(f"Error with URL loading: {e}.")

