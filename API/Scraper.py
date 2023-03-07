import requests
import pandas as pd
import numpy as np

def get_data(type_id):
    endpoint = f"https://evetycoon.com/api/v1/market/orders/{type_id}"
    response = requests.get(endpoint)
    if response.status_code == 200:
        data = response.json()
    else:
        print(f"Error {response.status_code}: {response.reason}")
        return None
    orders = [order for order in data.get("orders", []) if order.get("volumeRemain") != 0]
    orders.sort(key=lambda x: x.get("price", 0))
    return orders

def get_groups():
    endpoint = f"https://evetycoon.com/api/v1/market/groups"
    response = requests.get(endpoint)
    if response.status_code == 200:
        data = response.json()
    else:
        print(f"Error {response.status_code}: {response.reason}")
        return None
    groups = [element.get("marketGroupID") for element in data]
    return groups

def find_best_seller(orders, removed=None):
    if removed is None:
        removed = []
    for order in orders:
        if order["orderId"] not in removed and not order["isBuyOrder"]:
            return order
    return None

def find_best_buyer(orders, removed=None):
    if removed is None:
        removed = []
    for order in reversed(orders):
        if order["orderId"] not in removed and order["isBuyOrder"]:
            return order
    return None

def split_buy_sell(orders):
    buy_orders = [order for order in orders if order["isBuyOrder"]]
    sell_orders = [order for order in orders if not order["isBuyOrder"]]
    return buy_orders, sell_orders

def in_budget(orders, budget):
    budget_limited = [order for order in orders if not order["isBuyOrder"] or order["price"] <= budget]
    return budget_limited

def info_sale(type_id):
    orders = get_data(type_id)
    if not orders:
        return None
    buy_orders, sell_orders = split_buy_sell(orders)
    
    if not buy_orders or not sell_orders:
        return None
    best_buy_order = buy_orders[-1]
    best_sell_order = sell_orders[0]
    #print(best_sell_order)
    #print(best_buy_order)
    if  best_buy_order["price"] <best_sell_order["price"]:
        return None
    profit_margin = (-best_sell_order["price"] + best_buy_order["price"]) / best_buy_order["price"]
    return [profit_margin, -best_sell_order["price"]+ best_buy_order["price"], best_sell_order["orderId"], best_buy_order["orderId"]]

def sales_matrix(file,number_of_deals=-1):
    data = pd.read_csv(file, header=None)
    item_ids = data.iloc[:, 0].tolist()
    if number_of_deals==-1:
        number_of_deals=len(item_ids)
    M = np.zeros((number_of_deals, 5))
    i=-1
    for idx, item_id in enumerate(item_ids):
        info = info_sale(item_id)
        #print(item_id,info)
        if not info:
            continue
        i+=1
        if i==number_of_deals :
            break
        M[i, 0] = item_id
        M[i, 1] = info[0]
        M[i, 2] = info[1]
        M[i, 3] = info[2]
        M[i, 4] = info[3]

    return M

M=sales_matrix("item_IDs_list.csv",number_of_deals=5)
print("item_id\tgain_margin\tgain_value\tsellOrderID\tbuyOrderID")
print(M)

print(info_sale(33440))