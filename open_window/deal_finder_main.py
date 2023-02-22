from deal_finder_lib import *



# data = pd.read_csv(r'item_ids_list.csv')
# print(len(data))
# df = pd.DataFrame(data, columns=['item_id'])
# print(int(data.iloc[i][0]))
create_values(52230, 52240)

for i in range(52240, 52260, 10):
    add_values(i, i+10)
remove_first_column()
