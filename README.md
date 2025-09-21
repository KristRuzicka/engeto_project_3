# engeto_project_3

# Introduction
This program scrapes election result data in each village for given region and saves them in a csv file. The regions can be found on following link: "https://www.volby.cz/pls/ps2017nss/ps3?xjazyk=CZ".

The csv file includes:
- village code, 
- village name, 
- number of registered citizens, 
- number of given envelopes, 
- number of valid votes
- number of votes for each party.

# Requirements
Python 3.x
install libraries from requerements.txt
- pip install -r requirements.txt

# Usage
Open the link "https://www.volby.cz/pls/ps2017nss/ps3?xjazyk=CZ"
Choose a region and click on "x" in column "Vyber obce" 

To run program open cmd prompt and run: python main.py "url" name of the csv file
i.e. python main.py "https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=2&xnumnuts=2101" Benesov.csv

# Results 
Results will be presented in a csv file. 
Example for one village:
|Codes   |Location|Registered|Envelopes|Votes|Občanská demokratická strana|Other parties....
|553433  |Babylon |       230|      171|  169|                          19|