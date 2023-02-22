from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
import pandas as pd
from csv import DictWriter


# This function gets the gains margin on each item of the shop.
def find_prices(item_id, budget=-1, driver=None):
    url = "https://evetycoon.com/market/item_id".replace(
        'item_id', str(item_id))
    if driver is None:
        driver = webdriver.Firefox()
    driver.get(url)
    time.sleep(1)
    delay = 3

    try:
        myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located(
            (By.XPATH, '/html/body/main/main/div/div[2]/div[1]/div[3]/table/tbody/tr[1]/td[2]/div[2]/input')))
    except TimeoutException:
        print("page didn't load")

    if driver.find_element(By.XPATH, "/html/body/main/main/div/div[2]/div[2]/div[1]/div[1]/div/h3").text == 'Loading...':
        print("item not found")
        return -3
    if budget != -1:
        input_element = driver.find_element(
            By.XPATH, "/html/body/main/main/div/div[2]/div[1]/div[3]/table/tbody/tr[1]/td[2]/div[2]/input")
        input_element.clear()
        time.sleep(2)
        input_element.send_keys(str(budget))
        activate_budget = driver.find_element(
            By.XPATH, "/html/body/main/main/div/div[2]/div[1]/div[3]/table/tbody/tr[1]/td[1]/div/label")
        activate_budget.click()

    if driver.find_element(By.XPATH, "/html/body/main/main/div/div[2]/div[2]/div[1]/div[2]/table/tbody/tr[1]/td[4]").text == '0':
        print("no sales found")
        return -1
    if driver.find_element(By.XPATH, "/html/body/main/main/div/div[2]/div[2]/div[1]/div[2]/table/tbody/tr[2]/td[4]").text == '0':
        print("no buyers found")
        return -2
    best_buy_price = driver.find_element(
        By.XPATH, "/html/body/main/main/div/div[2]/div[2]/div[2]/div[2]/div/table/tbody/tr[1]/td[3]")
    best_sell_price = driver.find_element(
        By.XPATH, "/html/body/main/main/div/div[2]/div[2]/div[2]/div[3]/div/table/tbody/tr[1]/td[3]")
    buy_price = float(best_buy_price.text.replace(
        ',', '/').replace('/', '').split(" ")[0])
    sell_price = float(best_sell_price.text.replace(
        ',', '/').replace('/', '').split(" ")[0])
    print(sell_price-buy_price)
    return sell_price-buy_price


# This function creates the first few elements of the csv file (even if the csv file doesn't exist)
def create_values(start, end, file='open_window/deals_by_item_id.csv'):
    profit = []
    item_ids = [i for i in range(start, end)]
    driver = webdriver.Firefox()
    for item_id in item_ids:
        profit.append(find_prices(item_id, driver=driver))

    dict = {'item_id': item_ids, 'profit': profit}
    driver.close()
    df = pd.DataFrame(dict)
    df.to_csv(file)
    return 0


# This function adds values to the bottom of the csv file (the csv file has to exist first)
def add_values(start, end, file='open_window/deals_by_item_id.csv'):
    field_names = ["", "item_id", "profit"]
    dict = {'item_id': 0, 'profit': 0.0}
    with open(file, 'a') as f_object:
        dictwriter_object = DictWriter(f_object, fieldnames=field_names)
        item_ids = [i for i in range(start, end)]
        driver = webdriver.Firefox()
        time.sleep(1)
        for item_id in item_ids:
            dict["item_id"] = item_id
            dict["profit"] = find_prices(item_id, driver=driver)
            dictwriter_object.writerow(dict)
    driver.close()
    f_object.close()
    return 0


def remove_first_column(file='open_window/deals_by_item_id.csv'):
    df = pd.read_csv(file)
    # If you know the name of the column skip this
    first_column = df.columns[0]
    # Delete first
    df = df.drop([first_column], axis=1)
    df.to_csv(file, index=False)
