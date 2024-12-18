import requests
from bs4 import BeautifulSoup
import json
import pandas as pd
import time



csv = pd.read_csv('./sirens.csv')

test = csv.iloc[:948, 0]

variabls_list = ['Sigle, Enseigne, Nom commercial', 'Nom prenom', 'RCS','Adresse', 'Téléphone public', 'Email public', 'N° SIREN', 'Code NAF',  'N° Orias']
df = pd.DataFrame(columns = variabls_list)
# print('df', df)

for element in test:
    time.sleep(4)
    # print('element', element)
    # Step 1: Define the URL to scrape
    url = f"https://www.orias.fr/home/showIntermediaire/{element}"


    def span_scraper(variabls_list):
        for element in variabls_list:
            if element != "Nom prenom":
                span =  soup.find('span', string=element)
                if span:
                    sp = span.find_next('span').text.strip()
                    data[element] = sp
            else:
                span =  soup.find('span', class_='case')
                if span:
                    sp = span.find_next('span').text.strip()
                    data[element] = sp

        print('data', data)

    # Step 2: Send a GET request to the webpage
    response = requests.get(url)

    # Step 3: Check if the request was successful
    if response.status_code == 200:
        # Step 4: Parse the HTML content using Beautiful Soup
        soup = BeautifulSoup(response.text, 'html.parser')

        # Step 5: Extract the required fields
        data = {}


        span_scraper(variabls_list)


        # Convert the data to JSON and print it
        print(json.dumps(data, ensure_ascii=False, indent=4))
        df = df.append(data, ignore_index = True)
    else:
        print(f"Failed to retrieve the webpage. Status code: {response.status_code}")



df.to_csv('test_scraping.csv', index=False, sep=';', encoding='utf-8')


