import pandas as pd
from zipfile import ZipFile
import os
from datetime import date

# Data assortiment
df_assort = pd.read_excel('C:/Users/LAMIA/Desktop/Assortiement/Liste des codes internes.xlsx')
df_assort = pd.DataFrame(df_assort)
df_assort = df_assort.rename(columns ={"Libellé Bringo" : "Libellé"})

#### Remove all file ending with .csv
# crf
directory = "C:/Users/LAMIA/Desktop/data_server/crf/"
files_in_directory = os.listdir(directory)
filtered_files = [file for file in files_in_directory if file.endswith(".csv")]
for file in filtered_files:
    path_to_file = os.path.join(directory, file)
    os.remove(path_to_file)
#hyp
directory = "C:/Users/LAMIA/Desktop/data_server/crh/"
files_in_directory = os.listdir(directory)
filtered_files = [file for file in files_in_directory if file.endswith(".csv")]
for file in filtered_files:
    path_to_file = os.path.join(directory, file)
    os.remove(path_to_file)


# Detect file endswith CRF.zip : Supermarket
directory = "C:/Users/LAMIA/Desktop/data_zip"
files_in_directory = os.listdir(directory)
filtered_files = [file for file in files_in_directory if file.endswith("CRF.zip")]
file_crf = filtered_files[0]
print(file_crf)
# Detect file endswith CRH.zip : hypermarket
directory = "C:/Users/LAMIA/Desktop/data_zip"
files_in_directory = os.listdir(directory)
filtered_files = [file for file in files_in_directory if file.endswith("CRH.zip")]
file_crh = filtered_files[0]
print(file_crh)


# dezippé le fichier : Supermarket
file = "C:/Users/LAMIA/Desktop/data_zip/{}".format(file_crf)
with ZipFile(file, 'r') as zip:
    zip.extractall("C:/Users/LAMIA/Desktop/data_server/crf")
# dezippé le fichier : hypermarket
file = "C:/Users/LAMIA/Desktop/data_zip/{}".format(file_crh)
with ZipFile(file, 'r') as zip:
    zip.extractall("C:/Users/LAMIA/Desktop/data_server/crh")

# Detect le fichier stock_price crf
directory = "C:/Users/LAMIA/Desktop/data_server/crf"
files_in_directory = os.listdir(directory)
filtered_files = [file for file in files_in_directory if file.startswith("stock_price")]
file_stock_price_crf = filtered_files[0]
# Detect le fichier stock_price crf
directory = "C:/Users/LAMIA/Desktop/data_server/crh"
files_in_directory = os.listdir(directory)
filtered_files = [file for file in files_in_directory if file.startswith("stock_price")]
file_stock_price_crh = filtered_files[0]

# Remove file
def remove_file(file):
    try:
        os.remove(fi)
    except OSError as e:
        print(e)
    else:
        print("File is deleted successfully")

fi = "C:/Users/LAMIA/Desktop/rapport_achat/stock_price_crf.xls"
remove_file(fi)
fi = "C:/Users/LAMIA/Desktop/rapport_achat/stock_price_crh.xls"
remove_file(fi)
fi = "C:/Users/LAMIA/Desktop/rapport_achat/stock_price_crf_crh.xls"
remove_file(fi)

# Lire le fichier sock_price crf
name_file = "C:/Users/LAMIA/Desktop/data_server/crf/{}".format(file_stock_price_crf)
# detect name of file start with "stock_price"
file = pd.read_csv(name_file, sep='|')
df_stock_price_crf = pd.DataFrame(file)
df_stock_price_crf.columns = ['internal_product_id',"is_on_stock","original_price","price","unit_measure","info_price","info_unit_measure","internal_store_id"]
df_stock_price_crf = df_stock_price_crf.rename(columns ={"internal_product_id":"Code interne", "is_on_stock":"Stock", "original_price":"Prix Permanant", "price":"Prix Promo","internal_store_id":"Id Magasin"})
df_stock_price_crf = df_stock_price_crf[["Code interne","Stock","Prix Permanant","Prix Promo","Id Magasin"]]
df_stock_price_crf = pd.merge(df_stock_price_crf, df_assort, how="left", on=["Code interne"])
df_stock_price_crf = df_stock_price_crf[["Id Magasin","Code interne","Libellé","Stock","Prix Permanant","Prix Promo"]]
df_stock_price_crf = df_stock_price_crf.reset_index(drop=True)
df_stock_price_crf.index = df_stock_price_crf.index + 1
df_stock_price_crf.to_excel("C:/Users/LAMIA/Desktop/rapport_achat/stock_price_crf.xlsx")
print(df_stock_price_crf)


# Lire le fichier sock_price crh
name_file = "C:/Users/LAMIA/Desktop/data_server/crh/{}".format(file_stock_price_crh)
# detect name of file start with "stock_price"
file = pd.read_csv(name_file, sep='|')
df_stock_price_crh = pd.DataFrame(file)
df_stock_price_crh.columns = ['internal_product_id',"is_on_stock","original_price","price","unit_measure","info_price","info_unit_measure","internal_store_id"]
df_stock_price_crh = df_stock_price_crh.rename(columns ={"internal_product_id":"Code interne", "is_on_stock":"Stock", "original_price":"Prix Permanant", "price":"Prix Promo","internal_store_id":"Id Magasin"})
df_stock_price_crh = df_stock_price_crh[["Code interne","Stock","Prix Permanant","Prix Promo","Id Magasin"]]
df_stock_price_crh = pd.merge(df_stock_price_crh, df_assort, how="left", on=["Code interne"])
df_stock_price_crh = df_stock_price_crh[["Id Magasin","Code interne","Libellé","Stock","Prix Permanant","Prix Promo"]]
df_stock_price_crh = df_stock_price_crh.reset_index(drop=True)
df_stock_price_crh.index = df_stock_price_crh.index + 1
df_stock_price_crh.to_excel("C:/Users/LAMIA/Desktop/rapport_achat/stock_price_crh.xlsx")
print(df_stock_price_crh)

Today = date.today()
Today = str(Today)

with pd.ExcelWriter("C:/Users/LAMIA/Desktop/rapport_achat/Stock Price {}.xlsx".format(Today)) as writer:
    df_stock_price_crf.to_excel(writer, sheet_name="SUPERMARKET", index=False)
    df_stock_price_crh.to_excel(writer, sheet_name="HYPERMARKET", index=False)



p =str(len(df_stock_price_crh))
print(p)
file_object = open('C:/Users/LAMIA/Desktop/rapport_achat/size.csv', 'a')
file_object.write("\n")
file_object.write(p)
file_object.close()