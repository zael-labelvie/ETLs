import pandas as pd
import psycopg2
from sqlalchemy import create_engine
import datetime
import locale
from datetime import datetime

locale.setlocale(locale.LC_ALL, 'fr_FR.UTF-8')

################################## Get Data From Redash API KEY #################################
#################################################################################################

################################## Get Data From Redash Financial Report Table #################################
data_Financial = pd.read_csv(
    'https://redash-ro-live.bringo.ro/api/queries/25/results.csv?api_key=aUA3BBBPc14s4HT5vJEY7yD4iliLNBYCOUxISVUE')
df_Financial = pd.DataFrame(data_Financial)

################################## Get Data From Redash Dim_Picking Table #################################
data_Picking = pd.read_csv(
    'https://redash-ro-live.bringo.ro/api/queries/54/results.csv?api_key=dUomgvFEoNON3wp0WIkgTkH8kkpWnDJD1id2lBOP')
df_Picking = pd.DataFrame(data_Picking)

################################## Get Data From Redash Dim_User_Active Table #################################
data_User_Active = pd.read_csv(
    'https://redash-ro-live.bringo.ro/api/queries/49/results.csv?api_key=UtTnmFHHnB7rUmGvjCUajqKRtUn3VK9uQ8PLj5bc')
df_User_Active = pd.DataFrame(data_User_Active)

################################## Get Data From Redash Dim_Orders_Sales_General Table #################################
data_Orders_Sales_General = pd.read_csv(
    'https://redash-ro-live.bringo.ro/api/queries/56/results.csv?api_key=f3LKKEeHx6T3xbvq9g8QgqPsSCqEFcpTErOXfmoL')
df_Orders_Sales_General = pd.DataFrame(data_Orders_Sales_General)

################################## Get Data From Redash Dim_Product1 Table #################################
data_Product1 = pd.read_csv(
    'https://redash-ro-live.bringo.ro/api/queries/58/results.csv?api_key=hjGs3EjbKqOMcFnkxY39at1saNBfqq6seQ6TxNcL')
df_Product1 = pd.DataFrame(data_Product1)

################################## Get Data From Redash Dim_Product Table #################################
data_Commandes_Livrees = pd.read_csv(
    'https://redash-ro-live.bringo.ro/api/queries/63/results.csv?api_key=HE3TLs2ypqW9kLjrWCVwHOYOkl2A7OsB2JploQo6')
df_Commandes_Livrees = pd.DataFrame(data_Commandes_Livrees)

################################## Get Data From Redash Dim_Product Table #################################
data_Product_Order = pd.read_csv(
    'https://redash-ro-live.bringo.ro/api/queries/66/results.csv?api_key=lAsIyrBt0Hf4u9CfKjObIOkDjH6Oe4lgvQUfhpvF')
df_Product_Order = pd.DataFrame(data_Product_Order)

################################## Get Data From Redash Dim_Orders_Items Table #################################
Orders_Items = pd.read_csv(
    'https://redash-ro-live.bringo.ro/api/queries/80/results.csv?api_key=NXdnWDtGFaMK0Xja5w3Dy8vhNmD3XdbEsxa6l0PX')
df_Orders_Items = pd.DataFrame(Orders_Items)

################################## Get Data From Redash Dim_Product Table #################################
Data_Product = pd.read_csv(
    'https://redash-ro-live.bringo.ro/api/queries/92/results.csv?api_key=b2e99OcizKDalDNoUrE7ey2IRiLEfyfyn5dhE0n0')
df_Product = pd.DataFrame(Data_Product)


################################## Get Data From Redash Financial Report Table #################################
data_assortiment = pd.read_excel(
    'C:/Users/LAMIA/Desktop/Assortiement/Assortiment_Bringo_28_07_22.xlsx')
df_assortiment = pd.DataFrame(data_assortiment)

################################## Get Data From Redash Orders Items Table #################################
data_Orders_Items = pd.read_csv(
    'https://redash-ro-live.bringo.ro/api/queries/564/results.csv?api_key=a9EyU8XugA53eqgKkvmptaNfDl3aZ1JDAVZRabqj')
df_Orders_Items = pd.DataFrame(data_Orders_Items)

#####################################################################################################
#################################################### Pre-processing #################################
##df_Financial["customer_id"] = pd.to_numeric(df_Financial["customer_id"])

df_Financial['customer_id'] = df_Financial['customer_id'].astype(int)

df_Financial['picking_finish_at'] = df_Financial['picking_finish_at'].astype(str)
df_Financial['delivery_date_end'] = df_Financial['delivery_date_end'].astype(str)

df_Picking['order_start'] = df_Picking['order_start'].astype(str)
df_Picking['order_date'] = df_Picking['order_date'].astype(str)
df_Picking['picker_selected'] = df_Picking['picker_selected'].astype(str)
df_Picking['picked'] = df_Picking['picked'].astype(str)
df_Picking['shopper_selected'] = df_Picking['shopper_selected'].astype(str)
df_Picking['store_paid'] = df_Picking['store_paid'].astype(str)
df_Picking['order_end'] = df_Picking['order_end'].astype(str)

df_Product1['order_date'] = df_Product1['order_date'].astype(str)

data_Orders_Sales_General['shipping_address_latitude'] = data_Orders_Sales_General['shipping_address_latitude'].astype(
    float)
data_Orders_Sales_General['shipping_addrINT64ess_latitude'] = data_Orders_Sales_General[
    'shipping_addrINT64ess_latitude'].astype(float)

data_Orders_Sales_General['shipping_address_latitude'] = data_Orders_Sales_General['shipping_address_latitude'].fillna(
    0)
data_Orders_Sales_General['shipping_addrINT64ess_latitude'] = data_Orders_Sales_General[
    'shipping_addrINT64ess_latitude'].fillna(0)

df_Financial["delivery_date_end"] = [x.replace("T", " ") for x in df_Financial["delivery_date_end"]]
df_Financial["picking_finish_at"] = [x.replace("T", " ") for x in df_Financial["picking_finish_at"]]
df_Commandes_Livrees["delivery_date_end"] = [x.replace("T", " ") for x in df_Commandes_Livrees["delivery_date_end"]]

df_Financial_New_Order_1491 = {'customer_id': '225', 'order_id': '2902', 'picking_finish_at': '2022-06-07 19:30:00',
                               'delivery_date_end': '2022-06-07 20:00:00', 'number': '1491', 'order_state': 'complete',
                               'payment_method': 'online_payment', 'amount_per_method': '283.51',
                               'store_internal_name': 'Carrefour Market Panoramique', 'store_external_id': '166',
                               'vendor_name': 'Carrefour Supermarket', 'product_price': '283.51',
                               'product_price_without_vat': '283.51', 'vat': '0.0', 'discount_total': '0.00',
                               'shipping_discount': '30.0', 'original_shipping_amount': '30.0',
                               'non_product_value': '0.0 ', 'shipping_value': ' 0.0 ', 'manipulation_value': ' 0.0 ',
                               'preparation_fee': ' 0.0 '}
df_Financial_New_Order_1492 = {'customer_id': '263', 'order_id': '2904', 'picking_finish_at': '2022-06-07 09:50:07',
                               'delivery_date_end': '2022-06-07 11:30:00', 'number': '1492', 'order_state': 'complete',
                               'payment_method': 'online_payment', 'amount_per_method': '202.18',
                               'store_internal_name': 'Carrefour Market Panoramique', 'store_external_id': '166',
                               'vendor_name': 'Carrefour Supermarket', 'product_price': '202.18',
                               'product_price_without_vat': '202.18', 'vat': '0.0', 'discount_total': '0.00',
                               'shipping_discount': '30.0', 'original_shipping_amount': '30.0',
                               'non_product_value': '0.0 ', 'shipping_value': ' 0.0 ', 'manipulation_value': ' 0.0 ',
                               'preparation_fee': ' 0.0 '}
df_Financial_New_Order_1015 = {'customer_id': '155', 'order_id': '1347', 'picking_finish_at': '2022-04-26 20:00:00',
                               'delivery_date_end': '2022-04-26 20:00:00', 'number': '1015', 'order_state': 'complete',
                               'payment_method': 'online_payment', 'amount_per_method': '283.51',
                               'store_internal_name': 'Carrefour Market Panoramique', 'store_external_id': '166',
                               'vendor_name': 'Carrefour Supermarket', 'product_price': '134.24',
                               'product_price_without_vat': '134.24', 'vat': '0.0', 'discount_total': '0.00',
                               'shipping_discount': '30.0', 'original_shipping_amount': '30.0',
                               'non_product_value': '0.0 ', 'shipping_value': ' 0.0 ', 'manipulation_value': ' 0.0 ',
                               'preparation_fee': ' 0.0 '}
df_Financial_New_Order_1089 = {'customer_id': '174', 'order_id': '1435', 'picking_finish_at': '2022-03-14 11:05:49',
                               'delivery_date_end': '2022-03-14 11:05:49', 'number': '1089', 'order_state': 'complete',
                               'payment_method': 'online_payment', 'amount_per_method': '202.18',
                               'store_internal_name': 'Carrefour Market Panoramique', 'store_external_id': '166',
                               'vendor_name': 'Carrefour Supermarket', 'product_price': '58.18',
                               'product_price_without_vat': '202.18', 'vat': '0.0', 'discount_total': '0.00',
                               'shipping_discount': '30.0', 'original_shipping_amount': '30.0',
                               'non_product_value': '0.0 ', 'shipping_value': ' 0.0 ', 'manipulation_value': ' 0.0 ',
                               'preparation_fee': ' 0.0 '}

df_Financial = df_Financial.append(df_Financial_New_Order_1491, ignore_index=True)
df_Financial = df_Financial.append(df_Financial_New_Order_1492, ignore_index=True)
df_Financial = df_Financial.append(df_Financial_New_Order_1015, ignore_index=True)
df_Financial = df_Financial.append(df_Financial_New_Order_1089, ignore_index=True)


######################### Missing value function of picking_finish_at #############################
###################################################################################################

def fx(x):
    if x['picking_finish_at'] == 'nan':
        return x['delivery_date_end']

    else:
        return x['picking_finish_at']


######################### Missing value function of shopper_selected #############################
##################################################################################################

def Px(x):
    if x['shopper_selected'] == 'nan':
        return x['picked']

    else:
        return x['shopper_selected']


def LG(x):
    if x['shipping_address_latitude'] == 0.000000:
        return x['shipping_addrINT64ess_latitude']

    else:
        return x['shipping_address_latitude']


######################### Missing value function of shipping_address_latitude #############################
##################################################################################################


df_Financial['picking_finish_at'] = df_Financial.apply(lambda x: fx(x), axis=1)

df_Picking['shopper_selected'] = df_Picking.apply(lambda x: Px(x), axis=1)

df_Orders_Sales_General['shipping_address_latitude'] = df_Orders_Sales_General.apply(lambda x: LG(x), axis=1)
# data_Orders_Sales_General['shipping_address_latitude'] = data_Orders_Sales_General['shipping_address_latitude'] + data_Orders_Sales_General['shipping_addrINT64ess_latitude']

df_Financial['picking_finish_at'] = df_Financial['picking_finish_at'].apply(
    lambda row: datetime.strptime(row, '%Y-%m-%d %H:%M:%S'))
df_Financial['delivery_date_end'] = df_Financial['delivery_date_end'].apply(
    lambda row: datetime.strptime(row, '%Y-%m-%d %H:%M:%S'))

df_Picking['order_date'] = df_Picking['order_date'].apply(lambda row: datetime.strptime(row, '%Y-%m-%d'))
df_Picking['order_start'] = df_Picking['order_start'].apply(lambda row: datetime.strptime(row, '%d/%m/%y %H:%M'))
df_Picking['picker_selected'] = df_Picking['picker_selected'].apply(
    lambda row: datetime.strptime(row, '%d/%m/%y %H:%M'))
df_Picking['picked'] = df_Picking['picked'].apply(lambda row: datetime.strptime(row, '%d/%m/%y %H:%M'))
df_Picking['shopper_selected'] = df_Picking['shopper_selected'].apply(
    lambda row: datetime.strptime(row, '%d/%m/%y %H:%M'))
df_Picking['store_paid'] = df_Picking['store_paid'].apply(lambda row: datetime.strptime(row, '%d/%m/%y %H:%M'))
df_Picking['order_end'] = df_Picking['order_end'].apply(lambda row: datetime.strptime(row, '%d/%m/%y %H:%M'))

df_Orders_Sales_General['placed_at'] = df_Orders_Sales_General['placed_at'].apply(
    lambda row: datetime.strptime(row, '%d/%m/%y %H:%M'))
df_Orders_Sales_General['updated_at'] = df_Orders_Sales_General['updated_at'].apply(
    lambda row: datetime.strptime(row, '%d/%m/%y %H:%M'))
df_Orders_Sales_General['checkout_complete_at'] = df_Orders_Sales_General['checkout_complete_at'].apply(
    lambda row: datetime.strptime(row, '%d/%m/%y %H:%M'))

df_Product1['order_date'] = df_Product1['order_date'].apply(lambda row: datetime.strptime(row, '%Y-%m-%d'))

df_Financial['customer_id'] = df_Financial['customer_id'].astype(int)
df_Financial['order_id'] = df_Financial['order_id'].astype(int)
df_Financial['number'] = df_Financial['number'].astype(int)
df_Financial['store_external_id'] = df_Financial['store_external_id'].astype(int)

df_Financial['amount_per_method'] = df_Financial['amount_per_method'].astype(float)
df_Financial['product_price'] = df_Financial['product_price'].astype(float)
df_Financial['product_price_without_vat'] = df_Financial['product_price_without_vat'].astype(float)
df_Financial['vat'] = df_Financial['vat'].astype(float)

df_Financial['discount_total'] = df_Financial['discount_total'].astype(float)
df_Financial['shipping_discount'] = df_Financial['shipping_discount'].astype(float)
df_Financial['product_price_without_vat'] = df_Financial['product_price_without_vat'].astype(float)
df_Financial['original_shipping_amount'] = df_Financial['original_shipping_amount'].astype(float)

df_Financial['non_product_value'] = df_Financial['non_product_value'].astype(float)
df_Financial['shipping_value'] = df_Financial['shipping_value'].astype(float)
df_Financial['manipulation_value'] = df_Financial['manipulation_value'].astype(float)
df_Financial['preparation_fee'] = df_Financial['preparation_fee'].astype(float)
# df_assortiment['Code EAN'] = df_assortiment['Code EAN'].astype(float)
##pd.to_numeric(df_assortiment['Code EAN'], errors='coerce')

print(df_assortiment)
print(df_assortiment.dtypes)

####################################### Add Tow Orders in Dataframe df_Financial ###################################


####################################### Connecting with postgresql database  #######################################

conn_string = 'postgresql://squaduser:admin@172.16.3.116:5432/postgres'
db = create_engine(conn_string)
conn = db.connect()

###################################  Create DataFrame §§ Chargement des Tables Postgresql ####################

# Create DataFrame of Financial Reporting in a Financial Table
df_Financial.to_sql('RD_Bringo_Finance', con=conn, if_exists='replace', index=False)

# Create DataFrame of Financial Reporting in a Financial Table
df_Picking.to_sql('Dim_Picking', con=conn, if_exists='replace', index=False)

# Create DataFrame of User_Active in a Dim_User_Active Table
df_User_Active.to_sql('Dim_User_Active', con=conn, if_exists='replace', index=False)

# Create DataFrame of User_Active in a Dim_User_Active Table
df_Orders_Sales_General.to_sql('Dim_df_Orders_Sales_General', con=conn, if_exists='replace', index=False)

# Create DataFrame of Dim_Product in a Dim_Product Table
df_Product1.to_sql('Dim_Product1', con=conn, if_exists='replace', index=False)

# Create DataFrame of Dim_Product_Items in a Dim_Product Table
df_Orders_Items.to_sql('Dim_Product_Items', con=conn, if_exists='replace', index=False)

# Create DataFrame of Dim_Product in a Dim_Product Table
df_Product.to_sql('Dim_Product', con=conn, if_exists='replace', index=False)

# Create DataFrame of Dim_Product in a Dim_Product Table
df_assortiment.to_sql('Dim_Assortiment', con=conn, if_exists='replace', index=False)

# Create DataFrame of Dim_Product in a Dim_Product Table
df_Orders_Items.to_sql('Dim_Order_Items', con=conn, if_exists='replace', index=False)

requete_drop_table_1 ="DROP TABLE Vision_Product"

requete_drop_table_2 ="DROP TABLE Vision_Commande"


requete_vision_product = """select distinct DOI.product_name, DOI.unit_price,DA."Code interne",DA."Département", DA."FAMILLE", DA."RAYON", DA."SOUS FAMILLE", DA."SSFAM",DPR.picker_state, RD.number, DP.order_start, DP.picked, RD.delivery_date_end ,DOI.quantity,RD.store_internal_name,DP.user_picker,CASE
           WHEN RD.store_internal_name in ('Carrefour Market Anfa Place','Carrefour Market Panoramique')
                THEN 'Market'
           WHEN RD.store_internal_name = 'Carrefour Dar Bouazza'
                THEN 'Hyper'
       END Magasin_Type  
into Vision_Product
from "RD_Bringo_Finance" RD, "Dim_Picking" DP, "Dim_Product" DPR, "Dim_Order_Items" DOI, "Dim_Assortiment" DA
where RD.number = DP.number
and DP.id = DPR.id
and DPR.id = DOI.order_id
and DPR.order_item_id = DOI.id
and DA."Libellé Bringo" = DOI.product_name
Order by RD.number desc
"""
#and picker_state in ('replaced', 'unfound')
requete_add_columns ="""ALTER TABLE vision_product ADD COLUMN Quantity_Replaced_Tag INTEGER;
ALTER TABLE vision_product ADD COLUMN Quantity_Unfound_Tag INTEGER;
ALTER TABLE vision_product ADD COLUMN Quantity_found_Tag INTEGER;"""

update_1 = """UPDATE vision_product
SET Quantity_Replaced_Tag = CASE WHEN picker_state like 'replaced'  THEN quantity ELSE 0 END"""

update_2 = """UPDATE vision_product
SET Quantity_Unfound_Tag = CASE WHEN picker_state like 'unfound'  THEN quantity ELSE 0 END"""

update_3 = """UPDATE vision_product
SET Quantity_found_Tag = CASE WHEN picker_state like 'found'  THEN quantity ELSE 0 END"""


requete_vision_commande = """select vision_product.number, vision_product.order_start, vision_product.delivery_date_end, sum(Quantity_Replaced_Tag) as Quantity_Replaced, sum(Quantity_Unfound_Tag) as Quantity_Unfound ,sum(Quantity_found_Tag) as Quantity_found ,CASE
           WHEN sum(Quantity_Unfound_Tag) = 0 and sum(Quantity_Replaced_Tag) = 0
                THEN 'Commande Complete'
           WHEN sum(Quantity_Unfound_Tag) = 0 and sum(Quantity_Replaced_Tag) > 0
                THEN 'Partiellement complete'
           WHEN sum(Quantity_Unfound_Tag) <> 0 THEN 'Commande Incomplete'
       END Status_De_Commande 
into Vision_Commande
from vision_product
group by  vision_product.number, vision_product.order_start, vision_product.delivery_date_end
order by vision_product.number DESC"""

conn = psycopg2.connect(conn_string)
conn.autocommit = True
cursor = conn.cursor()
try:
    cursor.execute(requete_drop_table_1)
    cursor.execute(requete_drop_table_2)
except:
    pass
cursor.execute(requete_vision_product)
cursor.execute(requete_add_columns)
cursor.execute(update_1)
cursor.execute(update_2)
cursor.execute(update_3)
cursor.execute(requete_vision_commande)
conn.commit()
conn.close()


