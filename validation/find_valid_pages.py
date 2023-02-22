from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time


def access_website(item_id):
    url = 'https://www.eveworkbench.com/market/sell/item_id'.replace(
        'item_id', str(item_id))
    driver = webdriver.Chrome()
    driver.get(url)
    # time.sleep(1)
    try:
        do_not_consent = driver.find_element(
            By.XPATH, "/html/body/div[7]/div[2]/div[1]/div[2]/div[2]/button[2]/p")
        do_not_consent.click()
    except:
        print("button not clicked")
        raise
    text = "Whoops! The page you are looking for could not be found!"
    elem = driver.find_element(By.XPATH, "//*[contains(text(), text)]")
    # print(elem)
    # extract the text from the element and search it
    if text not in elem.text:
        # print("Text not found on page!")
        return item_id
    # print("found text")
    return -1


list = []
for i in range(52250, 52259):
    if access_website(i) > 0:
        list.append(i)
        print(i)
