from sqlalchemy import create_engine
import pandas as pd
import datetime
from datetime import date
import os

## detecte j-1
yesterday_2 = date.today() - datetime.timedelta(days=2)
yesterday_2 = str(yesterday_2)


list_magasin = ["Carrefour Sidi Maarouf",
                "Carrefour Hyper Temara",
                "Carrefour Market Ain Sebaa",
                "Carrefour Gourmet Zears",
                "Carrefour Market Hassan 2",
                "Carrefour Market Anfa Place",
                "Carrefour Market Panoramique",
                "Carrefour Dar Bouazza",
                "Carrefour Hyper Salé"]

def remove_file(file):
    for i in list_magasin:
        try:
            os.remove("C:/Users/LAMIA/Desktop/rapport_rupture/{} {}.xlsx".format(i, yesterday_2))
        except OSError as e:
            print(e)
        else:
            print("File is deleted successfully")

remove_file(list_magasin)

## detecte j-1
yesterday = date.today() - datetime.timedelta(days=1)
yesterday = str(yesterday)
#yesterday = "2023-02-26"  # Utiliser pour le Weekend




## Acces BD
#engine = create_engine('postgresql://squaduser:admin@172.16.3.116:5432/postgres')
engine = create_engine('postgresql://postgres:zael123456@localhost/Bringo')

# Import data sql to dataframe
df_vision_product = pd.read_sql_query('select * from "vision_product"',con=engine)
df_vision_commande = pd.read_sql_query('select * from "vision_commande"',con=engine)

print(df_vision_product['order_date'])

#print(df_vision_product['order_date'])
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
table_j_1 = df_vision_product.loc[(df_vision_product['order_date'] == yesterday)]


table_titre  = pd.DataFrame(columns=["Vision produit J-1 : {}".format(yesterday)])

table_j_1 = table_j_1.reset_index(drop=True)
table_j_1 = table_j_1[['number', 'order_date','product_name', 'unit_price','Code interne', 'Département', 'FAMILLE', 'RAYON',
       'SOUS FAMILLE', 'SSFAM', 'picker_state', 'quantity',
       'store_internal_name', 'user_picker',
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


table_j_1_commande = df_vision_commande.loc[(df_vision_commande['to_date'] == yesterday)]
table_titre_commande = pd.DataFrame(columns=["Vision commande J-1 : {}".format(yesterday)])

table_j_1_commande = table_j_1_commande.reset_index(drop=True)
table_j_1_commande['to_date'] = table_j_1_commande['to_date'].astype(str)



# Rename colonne
table_j_1.rename(columns={'number' : 'N° commande',
                          'order_date':'Date',
                          'product_name' : 'Produit',
                          'unit_price':'Prix unitaire',
                          'Code interne':'Code interne',
                          'Département':'Département',
                          'FAMILLE':'Famille',
                          'RAYON':'Rayon',
                          'SOUS FAMILLE': 'Sous Famille',
                          'SSFAM':'SS Famille',
                          'picker_state':'Status PDT',
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




p =str(len(table_j_1))

file_object = open('C:/Users/LAMIA/Desktop/rapport_rupture/size_j_1.csv', 'a')
file_object.write("\n")
file_object.write(p)
file_object.close()


TCD = table_j_1[["Magasin","Date",'N° commande','Code interne',"Produit","Status PDT","Quantité","Prix unitaire","Département", "Rayon", "Famille", "Sous Famille"]]
#print(TCD)
TCD['Quantité'] = TCD['Quantité'].astype(float)
TCD['Prix unitaire'] = TCD['Prix unitaire'].astype(float)
TCD['Prix Total'] = TCD.apply(lambda x : x['Quantité'] * x["Prix unitaire"], axis=1)
table = TCD[["Magasin","Date",'N° commande','Code interne',"Produit","Status PDT","Quantité","Prix unitaire","Prix Total","Département", "Rayon", "Famille", "Sous Famille"]]

#table = pd.pivot_table(tcs, index=["Magasin","Produit","Code interne","Status produit"])
table = table[table['Status PDT'] != 'found']
table = table[table['Status PDT'] != 'new']
table = table.dropna(subset=['Status PDT'])
table['Status PDT'] = table['Status PDT'].replace("replaced","Remplacé")
table['Status PDT'] = table['Status PDT'].replace("unfound","Non trouvé")


######################################################################################

table_titre_commentaire = pd.DataFrame(columns=["Motif"])
table_titre_2 = pd.DataFrame(columns=["Vision Magasin J-1 : {}".format(yesterday)])


######################################################### generation des fichiers pour toutes les

size_l = []
for i in list_magasin:
    df_sidi_maarouf = table.loc[(table['Magasin'] == i)]
    recap_sidi_maaraouf = df_sidi_maarouf[["Magasin", "Status PDT"]]
    recap_sidi_maaraouf = recap_sidi_maaraouf.pivot_table(values="Status PDT", index="Magasin", columns="Status PDT", aggfunc=len, fill_value=0)

    df_sidi_maarouf = df_sidi_maarouf.reset_index(drop=True)
    df_sidi_maarouf.index = df_sidi_maarouf.index + 1

    # To_exel
    writer = pd.ExcelWriter('C:/Users/LAMIA/Desktop/rapport_rupture/{} {}.xlsx'.format(i, yesterday), engine='xlsxwriter')
    workbook  = writer.book


    y = len(df_sidi_maarouf)
    size_l.append(int(y))
    table_titre.to_excel(writer, sheet_name='Sheet1', startrow=0, startcol=0)
    df_sidi_maarouf.to_excel(writer, sheet_name='Sheet1', startrow=2)
    table_titre_commentaire.to_excel(writer, sheet_name='Sheet1', startrow=2, startcol=13)
    table_titre_2.to_excel(writer, sheet_name='Sheet1', startrow=y+5, startcol=0)
    recap_sidi_maaraouf.to_excel(writer, sheet_name='Sheet1', startrow=y+7, startcol=1)


    worksheet = writer.sheets['Sheet1']
    worksheet.set_column("B:C", 30)
    worksheet.set_column("C:D", 10)
    worksheet.set_column("D:E", 12)
    worksheet.set_column("E:F", 15)
    worksheet.set_column("F:G", 45)
    worksheet.set_column("G:H", 12)
    worksheet.set_column("H:I", 10)
    worksheet.set_column("I:J", 15)
    worksheet.set_column("J:K", 12)
    worksheet.set_column("K:L", 12)
    worksheet.set_column("L:M", 15)
    worksheet.set_column("M:N", 20)
    worksheet.set_column("N:O", 35)


    size = len(df_sidi_maarouf)
    print(size)
    for i in range(4,size+4):
        worksheet.data_validation('O{}'.format(i), {'validate': 'list', 'source': ['','STOCK FAUX', 'PRODUIT EN RESERVE', 'QUALITE', 'DLC PROCHE']})

    for i in range(4,size+4):
        worksheet.write("O{}".format(i), '')  # set cell value



    writer.save()
############################################


def somme(size_l):
    somme = 0
    for i in size_l:
        somme = somme + i
    return somme
somme_finale = somme(size_l)
print(somme_finale)

p =str(somme_finale)

file_object = open('C:/Users/LAMIA/Desktop/rapport_rupture/size_j_1.csv', 'a')
file_object.write("\n")
file_object.write(p)
file_object.close()
