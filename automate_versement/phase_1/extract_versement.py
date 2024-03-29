import pandas as pd
import datetime
from datetime import date
import locale
import os
import time
import webbrowser
import pyautogui
from openpyxl.utils.dataframe import dataframe_to_rows

locale.setlocale(locale.LC_ALL, 'fr_FR.UTF-8')


#fi = "C:/Users/elmaa/OneDrive/Bureau/rapport_livraison/Livraison_rapport.xlsx"
fi = "C:/Users/LAMIA/Desktop/rapport_versement/Versement_rapport.xlsx"

def remove_file(file):
    try:
        os.remove(fi)
    except OSError as e:
        print(e)
    else:
        print("File is deleted successfully")


remove_file(fi)

## Read data from Redash

dat = pd.read_csv(
    'https://redash-ro-live.bringo.ro/api/queries/23/results.csv?api_key=geCGwjb5UX3vj5cWnFpSlwG7guEZv7aYpfybRUnN')
data = pd.DataFrame(dat)

data = data[data.order_state != 'canceled']
data = data[data.order_state != 'paid']

# delete order_test
order_test = [1802, 1218, 605, 599, 592, 584, 581, 580, 578, 559, 1191, 1189, 1184, 1183, 1182, 1154, 1146, 1142, 1136, 1133,
              1077, 1075, 1068, 1067, 1066, 1065, 1064, 1063, 1062, 1059, 1057, 1054, 1052, 1049, 1048, 1047, 1043,
              1042, 1041, 1040, 1039, 1035, 1033, 1032, 1031, 1016, 996, 995, 992, 991, 989, 987, 986, 980, 969, 968,
              967, 960, 961, 962, 968, 967, 969, 975, 977, 979, 1235, 1138, 1137, 1134, 1122, 1070, 1045, 1061, 1060,
              1218, 1191, 1184, 1183, 1182, 1154, 1148, 1146, 1142, 1133, 1134, 1136, 1137, 1138, 1077, 1075, 1070,
              1068, 1067, 1066, 1065, 1064, 1063, 1062, 1060, 1059, 1047, 1057, 1054, 1053, 1052, 1050, 1049, 1048,
              1045, 1044, 1043, 1042, 1041, 1040, 1039, 1035, 1033, 1032, 1031, 1016, 982, 983, 984, 1116, 1702, 1719,2227]
for i in order_test:
    data = data[data.number != i]

# Modifier type column date
data['picking_finish_at'] = data['picking_finish_at'].astype(str)
data['delivery_date_end'] = data['delivery_date_end'].astype(str)

data["delivery_date_end"] = [x.replace("T", " ") for x in data["delivery_date_end"]]
data["picking_finish_at"] = [x.replace("T", " ") for x in data["picking_finish_at"]]

df_Financial_New_Order_1491 = {'order_id': '2902', 'picking_finish_at': '2022-06-07 19:59:59',
                               'delivery_date_end': '2022-06-07 19:59:59', 'number': '1491', 'order_state': 'complete',
                               'payment_method': 'online_payment', 'amount_per_method': '283.51',
                               'store_internal_name': 'Carrefour Market Panoramique', 'store_external_id': '166',
                               'vendor_name': 'Carrefour Supermarket', 'product_price': '283.51',
                               'product_price_without_vat': '283.51', 'vat': '0.0', 'discount_total': '0.00',
                               'shipping_discount': '30.0', 'original_shipping_amount': '30.0',
                               'non_product_value': '0.0', 'shipping_value': '0.0', 'manipulation_value': '0.0',
                               'preparation_fee': '0.0'}
df_Financial_New_Order_1492 = {'order_id': '2904', 'picking_finish_at': '2022-06-07 23:38:07',
                               'delivery_date_end': '2022-06-07 23:38:07', 'number': '1492', 'order_state': 'complete',
                               'payment_method': 'online_payment', 'amount_per_method': '202.18',
                               'store_internal_name': 'Carrefour Market Panoramique', 'store_external_id': '166',
                               'vendor_name': 'Carrefour Supermarket', 'product_price': '202.18',
                               'product_price_without_vat': '202.18', 'vat': '0.0', 'discount_total': '0.00',
                               'shipping_discount': '30.0', 'original_shipping_amount': '30.0',
                               'non_product_value': '0.0', 'shipping_value': '0.0', 'manipulation_value': '0.0',
                               'preparation_fee': '0.0'}

data = data.append(df_Financial_New_Order_1491, ignore_index=True)
data = data.append(df_Financial_New_Order_1492, ignore_index=True)

def fx(x):
    if x['picking_finish_at'] == 'nan':
        return x['delivery_date_end']

    else:
        return x['picking_finish_at']

def Sx(x):
    if x['delivery_date_end'] == 'nan':
        return x['picking_finish_at']

    else:
        return x['delivery_date_end']


data['order_id'] = data['order_id'].astype(int)
data['number'] = data['number'].astype(int)
data['store_external_id'] = data['store_external_id'].astype(int)
data['amount_per_method'] = data['amount_per_method'].astype(float)
data['product_price'] = data['product_price'].astype(float)
data['product_price_without_vat'] = data['product_price_without_vat'].astype(float)
data['vat'] = data['vat'].astype(float)
data['discount_total'] = data['discount_total'].astype(float)
data['shipping_discount'] = data['shipping_discount'].astype(float)
data['product_price_without_vat'] = data['product_price_without_vat'].astype(float)
data['original_shipping_amount'] = data['original_shipping_amount'].astype(float)
data['non_product_value'] = data['non_product_value'].astype(float)
data['shipping_value'] = data['shipping_value'].astype(float)
data['manipulation_value'] = data['manipulation_value'].astype(float)
data['preparation_fee'] = data['preparation_fee'].astype(float)

data['picking_finish_at'] = data.apply(lambda x: fx(x), axis=1)
data['delivery_date_end'] = data.apply(lambda x: Sx(x), axis=1)

data['picking_finish_at'] = data['picking_finish_at'].apply(lambda row: row.replace(row[-8:], ""))
data['delivery_date_end'] = data['delivery_date_end'].apply(lambda row: row.replace(row[-8:], ""))

data['picking_finish_at'] = data['picking_finish_at'].apply(lambda row: row.rstrip())
data['delivery_date_end'] = data['delivery_date_end'].apply(lambda row: row.rstrip())

# print(data)
# xa = data[data['delivery_date_end'] == ""]
# print(xa[['picking_finish_at', 'delivery_date_end', 'number']])

data['picking_finish_at'] = data['picking_finish_at'].apply(lambda row: datetime.datetime.strptime(row, "%Y-%m-%d"))
data['delivery_date_end'] = data['delivery_date_end'].apply(lambda row: datetime.datetime.strptime(row, "%Y-%m-%d"))

data['Total'] = data['amount_per_method']
# table ne contient pas Delevry date == "canceled"
data = data[data.order_state != 'canceled']

# table j-1
yesterday = date.today() - datetime.timedelta(days=1)
yesterday = str(yesterday)
#yesterday = "2023-02-06"  # Utiliser pour le Weekend

table_j_1 = data.loc[(data['delivery_date_end'] == yesterday)]
table_j_1 = table_j_1[['delivery_date_end', 'number',
                       'order_state', 'payment_method',
                       'store_internal_name', 'vendor_name', 'Total']]
print(table_j_1)
table_j_1.rename(columns={'store_internal_name': 'Magasin'}, inplace=True)

##  jusqu'a j-1
df_jusqua_1 = data[data['delivery_date_end'] <= yesterday]
df_clear = df_jusqua_1


# Formules + DF j-1
Etakada_1 = table_j_1.groupby(['Magasin', 'payment_method'])['Total'].agg('sum')
Etakada_df_1 = pd.DataFrame(Etakada_1)


# Table name = titre
table_4 = pd.DataFrame(columns=["E-Takada CA : {}".format(yesterday)])

table_j_1['delivery_date_end'] = table_j_1['delivery_date_end'].astype(str)
table_j_1 = table_j_1.reset_index(drop=True)
# Export Data
table_j_1.index = table_j_1.index + 1

print(table_j_1)
print(Etakada_df_1)

df =  Etakada_df_1.reset_index().pivot('Magasin', 'payment_method', 'Total').fillna(0)

x1 = len(table_j_1) + 5

#with pd.ExcelWriter("C:/Users/elmaa/OneDrive/Bureau/rapport_livraison/Livraison_rapport.xlsx") as writer:
with pd.ExcelWriter("C:/Users/LAMIA/Desktop/rapport_versement/Versement_rapport {}.xls".format(yesterday)) as writer:
    table_4.to_excel(writer , sheet_name="Sheet1", startcol=0)
    table_j_1.to_excel(writer , sheet_name="Sheet1", startrow=2, startcol=1)
    try:
        df.to_excel(writer , sheet_name="Sheet1", startrow=x1, startcol=1)
    except:
        pass


p =str(len(table_j_1))
print(p)
file_object = open('C:/Users/LAMIA/Desktop/rapport_versement/size.csv', 'a')
file_object.write("\n")
file_object.write(p)
file_object.close()



