import requests
from bs4 import BeautifulSoup
import json
import pandas as pd
import time
import csv


def get_data(url):
    r = requests.get(url)
    # data = dict(r.json())
    data = r.text
    # print(data)
    return data


def get_id(data):
    f = open('validation/item_ids_list.csv', 'w')
    writer = csv.writer(f)
    soup = BeautifulSoup(data, 'html.parser')
    item_ids = soup.find_all('td', {'class': 'border-right-grey type_published_1'})
    writer.writerow(["item_id"])
    print("There is",len(item_ids),"ids")
    for item_id in item_ids:
        input = str(item_id)
        soupe = BeautifulSoup(input, features="lxml")
        writer.writerow([int(soupe.get_text())])

    f.close()
    return 0


url = "https://www.adam4eve.eu/info_types.php"
get_id(get_data(url))
print("File created/updated")
