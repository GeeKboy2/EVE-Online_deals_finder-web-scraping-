import requests
from bs4 import BeautifulSoup





transaction = 'sell'
item_id = '52250'
sell_url = 'https://www.eveworkbench.com/market/sell/item_id'.replace(
    'item_id', str(item_id))
buy_url = sell_url.replace('sell', 'buy')

#print(sell_url)
#print(buy_url)



def get_data(url):
    r = requests.get(url)
    # data = dict(r.json())
    data = r.text
    # print(data)
    return data


# get_data(url)

"""
def get_price(data):
    soup = BeautifulSoup(data, 'html.parser')
    games = soup.find_all('tr',{'class' : 'small'})
    for game in games:
        #print(game)
        #print(game.find('td', {'class': 'text-right'}.next_siblings))
    #print(int(float(game.find('td', {'class': 'text-right'}).text.replace('.','/').replace(',','.').replace('/',''))))
    print(game)
    return int(float(game.find('td', {'class': 'text-right'}).text.replace('.','/').replace(',','.').replace('/','')))
"""


def get_item_data(data):
    class item:  # class item
        # id and price are atributes of the item class
        def __init__(self, region, station, price, quantity, size, unknown, expire, last_seen):
            self.region = region
            self.station = station
            self.price = price
            self.quantity = quantity
            self.size = size
            self.unknown = unknown
            self.expire = expire
            self.last_seen = last_seen

        def __str__(self):
            return str(self.region)+" "+str(self.station)+" for ||"+str(self.price)+"|| ("+str(self.quantity)+") "+str(self.size)+" expires on "+str(self.expire)+" last seen "+str(self.last_seen)

    soup = BeautifulSoup(data, 'html.parser')
    games = soup.find_all('tr', {'class': 'small'})
    list_items = []
    for game in games:
        input = str(game)
        soupe = BeautifulSoup(input, features="lxml")

        chosen_item = item('', '', '', '', '', '', '', '')

        i = 0
        for br in soupe.findAll('td'):
            # print("_________________________________________________"," ".join(br.get_text().split()))
            i += 1
            if i % 8 == 1:
                chosen_item.region = " ".join(br.get_text().split())
            if i % 8 == 2:
                chosen_item.station = " ".join(br.get_text().split())
            if i % 8 == 3:
                chosen_item.price = int(float((" ".join(br.get_text().split())).replace(
                    '.', '/').replace(',', '.').replace('/', '')))
            if i % 8 == 4:
                chosen_item.quantity = int(
                    (" ".join(br.get_text().split())).split(" / ")[0])
            if i % 8 == 5:
                chosen_item.size = float(
                    (" ".join(br.get_text().split())).split(" ")[0])
            if i % 8 == 6:
                chosen_item.unknown = " ".join(br.get_text().split())
            if i % 8 == 7:
                chosen_item.expire = " ".join(br.get_text().split())
            if i % 8 == 0:
                chosen_item.last_seen = " ".join(br.get_text().split())
        list_items.append(chosen_item)
    return list_items[-1]


# get_item_data(get_data(sell_url))


def get_prices_for(item_id):
    sell_url = 'https://www.eveworkbench.com/market/sell/item_id'.replace(
        'item_id', str(item_id))
    buy_url = sell_url.replace('sell', 'buy')
    buy = get_item_data(get_data(buy_url))
    sell = get_item_data(get_data(sell_url))
    if type(buy.quantity) is str:
        #print(type(buy.quantity)) 
        return [0,0,0]

    print()
    print()
    print("From")
    print(buy)
    print("To")
    print(sell)
    print()

    quantity = min(buy.quantity, sell.quantity)
    #print(type(buy.quantity)) 
    print("You gain",float(sell.price)/float(buy.price),"buy", quantity,"items you need",(buy.size/buy.quantity)*quantity ,"m3 of space")
    return [sell.price/buy.price, quantity,(buy.size/buy.quantity)*quantity]


get_prices_for(52250)
get_prices_for(52358)
get_prices_for(52351)
"""
matrix=[]
for item_id in range(52250,52259):
    try:
        matrix.append(get_prices_for(item_id))
    except:
        #print(item_id)
        raise
        
        #continue
print(matrix)
"""
