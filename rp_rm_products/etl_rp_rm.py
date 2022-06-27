import pandas as pd
import psycopg2
import sys
import os

####################################### EXTRACT DATA FROM STOCK_0
data = pd.read_excel(r"C:\Users\LAMIA\Desktop\Glovo_externe\rrd.xlsx")
df = pd.DataFrame(data)


####################################### TRANSFORM DATA
df = df.fillna(0)
try:
    df = df.drop(columns=["Is Scheduled (Yes / No)"])
    df['Store Name'] = df['Store Name'].replace(['Carrefour Market Salé', 'Carrefour Market Beauséjour'],
                                                ['Carrefour Market Sale', 'Carrefour Market Beausejour'])
    df['Store Store Name'] = df['Store Store Name'].map('{}, Maroc'.format)
except:
    pass
df['Orders IN'] = df['Orders IN'].astype(int)
df.drop(df[df['Activation Local Date'] == 0].index, inplace = True)
df = df.drop_duplicates()



####################################### LOAD DATA
param_dic = {
    "host"      : "localhost",
    "database"  : "labelvie",
    "user"      : "postgres",
    "password"  : "zael123456"
}
def connect(params_dic):
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params_dic)
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        sys.exit(1)
    print("Connection successful")
    return conn


def copy_from_file(conn, df, table):
    """
    Here we are going save the dataframe on disk as
    a csv file, load the csv file
    and use copy_from() to copy it to the table
    """
    # Save the dataframe to disk
    #tmp_df = "./rp_rm_products.csv"
    tmp_df = "C:/Users/LAMIA/Desktop/traitement_rdd/rp_rm_products.csv"
    df.to_csv(tmp_df, index_label='id', header=False, sep=";")
    f = open(tmp_df, 'r')
    cursor = conn.cursor()
    try:
        cursor.copy_from(f, table, sep=";")
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error: %s" % error)
        conn.rollback()
        cursor.close()
        return 1
    print("copy_from_file() done")
    cursor.close()

def flash_table():
    cursor = conn.cursor()
    cursor.execute("TRUNCATE table rp_rm_products;")
    conn.commit()
    print("flash last data table has ben successfuly")
    cursor.close()


############## Suppression file stock_0
fileTest2 = r"C:\Users\LAMIA\Desktop\Glovo_externe\rrd.xlsx"

def remove_file(file):
    try:
        os.remove(fileTest2)
    except OSError as e:
        print(e)
    else:
        print("File is deleted successfully")

# -----------------------------------------------
# Main code
# -----------------------------------------------
conn = connect(param_dic)  # connect to the database
#flash_table()
copy_from_file(conn, df, 'rp_rm_products')
remove_file(fileTest2)
conn.close()

