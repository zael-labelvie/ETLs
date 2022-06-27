import pandas as pd
import numpy as np
import psycopg2
import sys
import os

####################################### EXTRACT DATA FROM STOCK_0
data = pd.read_excel(r"C:\Users\LAMIA\Desktop\carrefour_search\cs2.xlsx")
df = pd.DataFrame(data)


####################################### TRANSFORM DATA
try:
    df = df.fillna(0)
    df = df.iloc[:, 1:-1] # Drop last column
    df.insert(0, "date_fin", "31-03-2022", True)
    df["Number of Searches with 0 Results"] = df["Number of Searches with 0 Results"].astype(int)
    #df["Groceries Mp Products Search Results Number of searches with 0 results"] = df["Groceries Mp Products Search Results Number of searches with 0 results"].astype(int)
    df = df.drop_duplicates()
except:
    print('There is a problem in the values of the columns - ETL CARREFOUR SEARCH')



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
    #tmp_df = "./crf_daily.csv"
    tmp_df = "C:/Users/LAMIA/Desktop/traitement_c_search/carrefour_search.csv"
    df.to_csv(tmp_df, index_label='id', header=False, sep=";")
    f = open(tmp_df, 'r', encoding="utf8")
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
    cursor.execute("TRUNCATE table carrefour_search;")
    conn.commit()
    print("flash last data table has ben successfuly")
    cursor.close()

############## Suppression file stock_0
fileTest1 = r"C:\Users\LAMIA\Desktop\carrefour_search\cs.xlsx"

def remove_file(file):
    try:
        os.remove(fileTest1)
    except OSError as e:
        print(e)
    else:
        print("File is deleted successfully")


# -----------------------------------------------
# Main code
# -----------------------------------------------
conn = connect(param_dic)  # connect to the database
#flash_table()
copy_from_file(conn, df, 'carrefour_search') # copy the dataframe to SQL
remove_file(fileTest1)
conn.close()


