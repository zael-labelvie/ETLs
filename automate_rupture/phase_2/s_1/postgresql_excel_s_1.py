from sqlalchemy import create_engine
import pandas as pd
import datetime
from datetime import date
import os

# table s-1
today = datetime.date.today()
debut_semaine = today - datetime.timedelta(days=today.weekday(), weeks=1)
fin_semaine = today - datetime.timedelta(days=today.weekday(), weeks=1) + datetime.timedelta(days=6)
debut_semaine = '2022-09-01'
fin_semaine = '2022-12-31'

fi = "C:/Users/LAMIA/Desktop/rapport_rupture/Etat Rupture Journalier {}.xls".format(str(debut_semaine), str(fin_semaine))
def remove_file(file):
    try:
        os.remove(fi)
    except OSError as e:
        print(e)
    else:
        print("File is deleted successfully")
remove_file(fi)



#engine = create_engine('postgresql://squaduser:admin@172.16.3.116:5432/postgres')
engine = create_engine('postgresql://postgres:zael123456@localhost/Bringo')

# Import data sql to dataframe
df_vision_product = pd.read_sql_query('select * from "vision_product"',con=engine)
df_vision_commande = pd.read_sql_query('select * from "vision_commande"',con=engine)

print(df_vision_product['order_date'])
############################################ VISION PRODUIT
# add columns date_fin and time_fin
df_vision_product['date_fin'] = [d.date() for d in df_vision_product['delivery_date_end']]
df_vision_product['time_fin'] = [d.time() for d in df_vision_product['delivery_date_end']]
df_vision_product = df_vision_product.drop(labels='delivery_date_end', axis=1)
df_vision_product['date_fin'] = df_vision_product['date_fin'].astype(str)
df_vision_product['date_fin'] = df_vision_product['date_fin'].apply(lambda row: datetime.datetime.strptime(row, "%Y-%m-%d"))

#df_vision_product['date_debut'] = [d.date() for d in df_vision_product['order_start']]
#df_vision_product['time_debut'] = [d.time() for d in df_vision_product['order_start']]
#df_vision_product['date_debut'] = df_vision_product['date_debut'].astype(str)
#df_vision_product['date_debut'] = df_vision_product['date_debut'].apply(lambda row: datetime.datetime.strptime(row, "%Y-%m-%d"))

#table_j_1 = df_vision_product.loc[(df_vision_product['date_fin'] == yesterday)]
table_j_1 = df_vision_product[df_vision_product["order_date"].isin(pd.date_range(str(debut_semaine), str(fin_semaine)))]
print(table_j_1.columns)
#table_j_1 = table_j_1.loc[(table_j_1['store_internal_name'] == "Carrefour Dar Bouazza")]#########################################################


table_titre  = pd.DataFrame(columns=["Vision product du {} au {} ".format(str(debut_semaine), str(fin_semaine))])

table_j_1 = table_j_1.reset_index(drop=True)
table_j_1 = table_j_1[['number', 'order_date','product_name', 'unit_price','Code interne', 'Département', 'FAMILLE', 'RAYON',
       'SOUS FAMILLE', 'SSFAM', 'picker_state', 'quantity',
       'store_internal_name', 'magasin_type', 'user_picker',
       'quantity_replaced_tag', 'quantity_unfound_tag', 'quantity_found_tag']]
# table_j_1 = table_j_1[['number', 'product_name', 'unit_price', 'Code interne', 'Département', 'FAMILLE', 'RAYON',
#        'SOUS FAMILLE', 'SSFAM', 'picker_state', 'quantity',
#        'store_internal_name', 'magasin_type', 'user_picker',
#        'quantity_replaced_tag', 'quantity_unfound_tag', 'quantity_found_tag','date_debut', 'time_debut', 'picked', 'date_fin', 'time_fin']]

# table_j_1['date_fin'] = table_j_1['date_fin'].astype(str)
# table_j_1['date_debut'] = table_j_1['date_debut'].astype(str)

table_j_1['order_date'] = table_j_1['order_date'].astype(str)


table_j_1['unit_price'] = table_j_1['unit_price'].astype('str').str.replace(r'^(\d{2})$', '0\\1').str.replace(r'^(\d+)(\d{2})$', '\\1,\\2')
table_j_1['unit_price'] = table_j_1['unit_price'].apply(lambda row : row.replace(",", "."))

############################################ VISION COMMANDE
# add columns date_fin and time_fin
#df_vision_commande['date_fin'] = [d.date() for d in df_vision_commande['delivery_date_end']]
#df_vision_commande['time_fin'] = [d.time() for d in df_vision_commande['delivery_date_end']]
#df_vision_commande = df_vision_commande.drop(labels='delivery_date_end', axis=1)
df_vision_commande['to_date'] = df_vision_commande['to_date'].astype(str)
df_vision_commande['to_date'] = df_vision_commande['to_date'].apply(lambda row: datetime.datetime.strptime(row, "%Y-%m-%d"))


table_j_1_commande = df_vision_commande[df_vision_commande["to_date"].isin(pd.date_range(str(debut_semaine), str(fin_semaine)))]
table_titre_commande = pd.DataFrame(columns=["Vision commande du {} au {} ".format(str(debut_semaine), str(fin_semaine))])

table_j_1_commande = table_j_1_commande.reset_index(drop=True)
table_j_1_commande['to_date'] = table_j_1_commande['to_date'].astype(str)





# Rename colonne
table_j_1.rename(columns={'number' : 'Numéro de commande',
                          'order_date':'Date début',
                          'product_name' : 'Produit',
                          'unit_price':'Prix unitaire',
                          'Code interne':'Code interne',
                          'Département':'Département',
                          'FAMILLE':'Famille',
                          'RAYON':'Rayon',
                          'SOUS FAMILLE': 'Sous Famille',
                          'SSFAM':'SS Famille',
                          'picker_state':'Status produit',
                          'quantity':'Quantité',
                          'store_internal_name':'Magasin',
                          'user_picker': 'Préparateur',
                          'magasin_type':'Type magasin',
                          'quantity_replaced_tag':'Quantité de produit remplacé',
                          'quantity_unfound_tag':'Quantité de produit non trouvé',
                          'quantity_found_tag':'Quantité de produit trouvé',
                          #'date_debut':'Date début',
                          'time_debut':'Time début',
                          'picked':'Date préparation',
                          'date_fin':'Date fin',
                          'time_fin':'Time fin'},
                 inplace=True)


table_j_1_commande.rename(columns={'number' : 'Numéro de commande',
                          'to_date' : 'Date début',
                          'quantity_replaced':'Quantité de produit remplacé',
                          'quantity_unfound':'Quantité de produit non trouvé',
                          'quantity_found':'Quantité de produit trouvé',
                          'status_de_commande':'Status de commande',
                          'date_fin':'Date fin',
                          'time_fin': 'Time fin'},
                 inplace=True)

print(table_j_1)
table_j_1.index = table_j_1.index + 1
x0 = len(table_j_1) + 6
x1 = x0 + 2
#Export to excel
with pd.ExcelWriter("C:/Users/LAMIA/Desktop/rapport_rupture/Etat Rupture Journalier du {} au {}.xls".format(str(debut_semaine), str(fin_semaine))) as writer:
    table_titre.to_excel(writer, sheet_name="Sheet1", startcol=0)
    table_j_1.to_excel(writer, sheet_name="Sheet1", startrow=3, startcol=0)
    table_titre_commande.to_excel(writer, sheet_name="Sheet1", startrow=x0, startcol=0)
    table_j_1_commande.to_excel(writer, sheet_name="Sheet1", startrow=x1, startcol=0)


p =str(len(table_j_1))

file_object = open('C:/Users/LAMIA/Desktop/rapport_rupture/size_s_1.csv', 'a')
file_object.write("\n")
file_object.write(p)
file_object.close()





TCD = table_j_1[["Magasin","Date début","Produit",'Code interne',"Status produit","Quantité","Prix unitaire","Département", "Rayon", "Famille", "Sous Famille"]]
print(TCD)
TCD['Quantité'] = TCD['Quantité'].astype(float)
TCD['Prix unitaire'] = TCD['Prix unitaire'].astype(float)
TCD['Prix Total'] = TCD.apply(lambda x : x['Quantité'] * x["Prix unitaire"], axis=1)
table = TCD[["Magasin","Date début","Produit",'Code interne',"Status produit","Quantité","Prix unitaire","Prix Total","Département", "Rayon", "Famille", "Sous Famille"]]
#table = table.loc[(table['Magasin'] == "Carrefour Dar Bouazza")]#####################################

#table = pd.pivot_table(tcs, index=["Magasin","Produit","Code interne","Status produit"])
table = table[table['Status produit'] != 'found']
table = table.reset_index(drop=True)
table.index = table.index + 1






#Export to excel
with pd.ExcelWriter("C:/Users/LAMIA/Desktop/rapport_rupture/Etat Rupture Journalier du {} au {}.xls".format(str(debut_semaine), str(fin_semaine))) as writer:
    table_titre.to_excel(writer, sheet_name="Base", startcol=0)
    table_j_1.to_excel(writer, sheet_name="Base", startrow=3, startcol=0)
    table_titre_commande.to_excel(writer, sheet_name="Base", startrow=x0, startcol=0)
    table_j_1_commande.to_excel(writer, sheet_name="Base", startrow=x1, startcol=0)
    table_titre.to_excel(writer, sheet_name="Rupture", startcol=0)
    table.to_excel(writer, sheet_name="Rupture", startrow=2, startcol=0)
