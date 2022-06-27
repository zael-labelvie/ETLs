import pandas as pd
import psycopg2
import sys
import os

####################################### EXTRACT DATA FROM STOCK_0
data = pd.read_csv(r"C:\Users\LAMIA\Desktop\Bringo_gold\bringo_gold.csv", delimiter=';')
df = pd.DataFrame(data)

####################################### TRANSFORM DATA
try:
    df = df.fillna(0)
    df['quantite'] = df['quantite'].astype(int)
    indexNames = df[df['quantite'] == 0].index
    df.drop(indexNames)
    df['libl_article']= df['libl_article'].replace("OLIV.V.DNY.BARA;37CL     ", "OLIV.V.DNY.BARA 37CL")
    df = df.drop_duplicates()
except:
    print('There is a problem in the values of the columns - ETL ORKAISSE GLOVO')



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
    tmp_df = "C:/Users/LAMIA/Desktop/traitement_bringo_gold/bringo_gold.csv"
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
    cursor.execute("TRUNCATE table bringo_gold;")
    conn.commit()
    print("flash last data table has ben successfuly")
    cursor.close()

############## Suppression file stock_0
fileTest3 = r"C:\Users\LAMIA\Desktop\Bringo_gold\bringo_gold.csv"

def remove_file(file):
    try:
        os.remove(fileTest3)
    except OSError as e:
        print(e)
    else:
        print("File is deleted successfully")


# ---------------------------------------------------
conn = connect(param_dic)  # connect to the database
#flash_table()
copy_from_file(conn, df, 'bringo_gold')
remove_file(fileTest3)
conn.close()


