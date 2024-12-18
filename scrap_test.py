import os
import requests
from bs4 import BeautifulSoup
import json
import pandas as pd
import time

# Load the SIREN numbers from the CSV file
csv = pd.read_csv('./sirens.csv')
test = csv.iloc[:948, 0]

# List of column names
variabls_list = ['Sigle, Enseigne, Nom commercial', 'Nom prenom', 'RCS', 'Adresse',
                 'Téléphone public', 'Email public', 'N° SIREN', 'Code NAF', 'N° Orias']

# Path to the output CSV file
output_file = 'test_scraping.csv'

# Loop through the elements and scrape the data
for element in test:
    time.sleep(4)
    # URL to scrape
    url = f"https://www.orias.fr/home/showIntermediaire/{element}"

    # Function to scrape data for each variable
    def span_scraper(variabls_list):
        data = {}
        for element in variabls_list:
            if element != "Nom prenom":
                span = soup.find('span', string=element)
                if span:
                    sp = span.find_next('span').text.strip()
                    data[element] = sp
            else:
                span = soup.find('span', class_='case')
                if span:
                    sp = span.find_next('span').text.strip()
                    data[element] = sp
        return data

    # Send a GET request to the webpage
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content using Beautiful Soup
        soup = BeautifulSoup(response.text, 'html.parser')

        # Scrape data
        data = span_scraper(variabls_list)

        # Print data as JSON for debugging
        print(json.dumps(data, ensure_ascii=False, indent=4))

        # Append data to the CSV file
        df = pd.DataFrame([data])

        # If the file exists, append without a header
        file_exists = os.path.exists(output_file)
        df.to_csv(output_file, index=False, sep=';', encoding='utf-8', mode='a', header=not file_exists)
    else:
        print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
