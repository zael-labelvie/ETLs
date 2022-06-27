import os
import sys
import pickle
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import re
import locale
import datetime
from datetime import date
import pandas as pd
locale.setlocale(locale.LC_ALL, 'fr_FR.UTF-8')

######################################################### Remove last rapport
fi ="C:/Users/LAMIA/Desktop/Finance/Financial_rapport.csv"
def remove_file(file):
    try:
        os.remove(fi)
    except OSError as e:
        print(e)
    else:
        print("File is deleted successfully")

remove_file(fi)

########################################################## Import Data
df_links = "C:/Users/LAMIA/Desktop/Finance/links.csv"
df = pd.read_csv(df_links)
idx = df.iloc[-1][0]
id = idx.split('/')
id_file = id[5]


###################################################################### Traitement data
# Email a partager
email ="zael-140@rational-text-344109.iam.gserviceaccount.com"

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# Get the script path
srcDir = os.path.abspath(os.path.dirname(sys.argv[0]))

#### USER INPUT ####
credentialFile = os.path.join(srcDir, 'creds.json')
# The ID and range of a sample spreadsheet.
sheetID = id_file
dataRange = 'Feuille1'
#### END USER INPUT ####

def Create_Service(client_secret_file, api_service_name, api_version, *scopes):
    SCOPES = [scope for scope in scopes[0]]
    print(SCOPES)

    cred = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('../automate_finance/2/token.pickle'):
        with open('../automate_finance/2/token.pickle', 'rb') as token:
            cred = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.

    if not cred or not cred.valid:
        if cred and cred.expired and cred.refresh_token:
            cred.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(client_secret_file, SCOPES)
            cred = flow.run_local_server()

    with open('../automate_finance/2/token.pickle', 'wb') as token:
        pickle.dump(cred, token)

    try:
        service = build(api_service_name, api_version, credentials=cred)
        print(api_service_name, 'service created successfully')
        return service
    except Exception as e:
        print(e)
        return None


def get_google_sheet_data():
    """Shows basic usage of the Sheets API.
    Retruns the Google Sheet data as Pandas DataFrame.
    """
    service = Create_Service(credentialFile, 'sheets', 'v4', SCOPES)

    # Call the Sheets API
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=sheetID, range=dataRange).execute()
    values = result.get('values', [])

    if not values:
        print('No data found.')
        return None
    else:
        df = pd.DataFrame(values[1:], columns=values[0])
        return df

sheet_df = get_google_sheet_data()


# Modify name of columns
sheet_df = sheet_df[['Order date', 'Delivery date', 'Store code', 'Name of the store',
       'Name of the vendor', 'Invoice number', 'Payment mode', 'Order state', 'VAT',
        'Subtotal excl. VAT', 'Subtotal incl. VAT', 'Value of coupon incl. VAT', 'Coupon Service incl. VAT' ,'Fee 2 incl VAT', 'Fee 1 incl VAT']]

sheet_df = sheet_df.rename(columns={'Order date':'Order_date', 'Delivery date':'Delivery_date', 'Store code':'Store_code', 'Name of the store':'Name_of_the_store',
       'Name of the vendor':'Name_of_the_vendor', 'Invoice number':'Invoice_number', 'Payment mode':'Payment_mode', 'Order state':'Order_state',
        'Subtotal excl. VAT':'Subtotal_excl_VAT', 'Subtotal incl. VAT':'Subtotal_incl_VAT',
       'Value of coupon incl. VAT':'Value_of_coupon_incl_VAT','Coupon Service incl. VAT':'Coupon_Service_incl_VAT', 'Fee 2 incl VAT':'Fee2_incl_VAT', 'Fee 1 incl VAT':'Fee1_incl_VAT'})


# Modify type of columns
sheet_df['Subtotal_excl_VAT'] = sheet_df['Subtotal_excl_VAT'].apply(lambda x: x.replace(",","."))
sheet_df['Subtotal_excl_VAT'] =  [re.sub(r"\s+", "", x, flags=re.UNICODE) for x in sheet_df['Subtotal_excl_VAT']]
sheet_df['Subtotal_excl_VAT'] = sheet_df['Subtotal_excl_VAT'].astype(float)

sheet_df['Subtotal_incl_VAT'] = sheet_df['Subtotal_incl_VAT'].apply(lambda x: x.replace(",","."))
sheet_df['Subtotal_incl_VAT'] =  [re.sub(r"\s+", "", x, flags=re.UNICODE) for x in sheet_df['Subtotal_incl_VAT']]
sheet_df['Subtotal_incl_VAT'] = sheet_df['Subtotal_incl_VAT'].astype(float)

sheet_df['Value_of_coupon_incl_VAT'] = sheet_df['Value_of_coupon_incl_VAT'].apply(lambda x: x.replace(",","."))
sheet_df['Value_of_coupon_incl_VAT'] = sheet_df['Value_of_coupon_incl_VAT'].astype(float)

sheet_df['Fee2_incl_VAT'] = sheet_df['Fee2_incl_VAT'].apply(lambda x: x.replace(",","."))
sheet_df['Fee2_incl_VAT'] = sheet_df['Fee2_incl_VAT'].astype(float)

sheet_df['Fee1_incl_VAT'] = sheet_df['Fee1_incl_VAT'].apply(lambda x: x.replace(",","."))
sheet_df['Fee1_incl_VAT'] = sheet_df['Fee1_incl_VAT'].astype(float)

sheet_df['Coupon_Service_incl_VAT'] = sheet_df['Coupon_Service_incl_VAT'].apply(lambda x: x.replace(",","."))
sheet_df['Coupon_Service_incl_VAT'] = sheet_df['Coupon_Service_incl_VAT'].astype(float)

#sheet_df['fee2_livraison'] = 30

# Add column coupon
#sheet_df['Coupon_service'] = sheet_df['fee2_livraison'] - sheet_df['Fee2_incl_VAT']

# Add column Total
sheet_df['Total'] = sheet_df['Subtotal_incl_VAT'] + sheet_df['Fee1_incl_VAT'] + sheet_df['Fee2_incl_VAT'] - sheet_df['Coupon_Service_incl_VAT'] - sheet_df['Value_of_coupon_incl_VAT']

# delete colum
#sheet_df = sheet_df.drop(columns="Fee2_incl_VAT")


# modify the format of value for colum order_date
sheet_df['Delivery_date'] = sheet_df['Delivery_date'].apply(lambda row : row.replace(",", ""))
sheet_df['Delivery_date'] = sheet_df['Delivery_date'].apply(lambda row : row.replace(".", ""))
sheet_df['Delivery_date'] = sheet_df['Delivery_date'].apply(lambda row : row.replace("avr", "avril"))
sheet_df['Delivery_date'] = sheet_df['Delivery_date'].apply(lambda row : row.replace("janv", "janvier"))
sheet_df['Delivery_date'] = sheet_df['Delivery_date'].apply(lambda row : row.replace("févr", "février"))
sheet_df['Delivery_date'] = sheet_df['Delivery_date'].apply(lambda row : row.replace("juill", "juillet"))
sheet_df['Delivery_date'] = sheet_df['Delivery_date'].apply(lambda row : row.replace("sept", "septembre"))
sheet_df['Delivery_date'] = sheet_df['Delivery_date'].apply(lambda row : row.replace("oct", "octobre"))
sheet_df['Delivery_date'] = sheet_df['Delivery_date'].apply(lambda row : row.replace("nov", "novembre"))
sheet_df['Delivery_date'] = sheet_df['Delivery_date'].apply(lambda row : row.replace("déc", "décembre"))
sheet_df['Delivery_date'] = sheet_df['Delivery_date'].apply(lambda row : row.replace(row[-8:], ""))
sheet_df['Delivery_date'] = sheet_df['Delivery_date'].apply(lambda row : row.rstrip())
print(sheet_df['Delivery_date'])
sheet_df['Delivery_date'] = sheet_df['Delivery_date'].apply(lambda row : datetime.datetime.strptime(row, "%d %B %Y"))
sheet_df['Delivery_date'] = sheet_df['Delivery_date'].astype(str)
sheet_df['Invoice_number'] = sheet_df['Invoice_number'].astype(int)

# Probleme date today
sheet_df['Delivery_date'] = sheet_df['Delivery_date'].apply(lambda row: row.replace(str(date.today()), str(date.today() - datetime.timedelta(days=1))))

# Supprimer les ordres de test
order_test = [1218,605,599,592,584,581,580,578,559,1191,1189,1184,1183,1182,1154,1146,1142,1136,1133,1077,1075,1068,1067,1066,1065,1064,1063,1062,1059,1057,1054,1052,1049,1048,1047,1043,1042,1041,1040,1039,1035,1033,1032,1031,1016,996,995,992,991,989,987,986,980,969,968,967]
for i in order_test:
    sheet_df = sheet_df[sheet_df.Invoice_number!=i]

#table ne contient pas Delevry date == "canceled"
sheet_df = sheet_df.drop(columns='Order_date')
df_clear = sheet_df[sheet_df.Order_state!='canceled']
print(df_clear.columns)
# Table J-1
#yesterday = date.today() - datetime.timedelta(days=1)
#yesterday = str(yesterday)
yesterday = "2022-05-22"  # Utiliser pour le Weekend
table_j_1 = df_clear.loc[(df_clear['Delivery_date'] == yesterday)]
print(df_clear)

## Rectification manuelle

df_jusqua_1 = df_clear[df_clear['Delivery_date'] <= yesterday]
df_clear = df_jusqua_1

# Formules + DF
Etakada = df_clear.groupby(['Payment_mode'])['Total'].agg('sum')
Etakada_df = pd.DataFrame(Etakada)
Labelvie = df_clear.groupby(['Payment_mode'])['Subtotal_excl_VAT'].agg('sum')
Labelvie_df = pd.DataFrame(Labelvie)
Labelvie_df = Labelvie_df.rename(columns={"Subtotal_excl_VAT":"Total"})

# Formules + DF j-1
Etakada_1 = table_j_1.groupby(['Payment_mode'])['Total'].agg('sum')
Etakada_df_1 = pd.DataFrame(Etakada_1)
Labelvie_1 = table_j_1.groupby(['Payment_mode'])['Subtotal_excl_VAT'].agg('sum')
Labelvie_df_1 = pd.DataFrame(Labelvie_1)
Labelvie_df_1 = Labelvie_df_1.rename(columns={"Subtotal_excl_VAT":"Total"})

# Table name = titre
table_1 = pd.DataFrame(columns=["Rapport Financial {}".format(str(date.today()))])
table_6 = pd.DataFrame(columns=["Rapport Financial J-1 : {}".format(yesterday)])
table_2 = pd.DataFrame(columns=["E-Takada CA Total"])
table_3 = pd.DataFrame(columns=["LabelVie CA Total"])
table_4 = pd.DataFrame(columns=["E-Takada CA J-1"])
table_5 = pd.DataFrame(columns=["LabelVie CA J-1"])
one_line = pd.DataFrame(columns=None, data=None)
# Export data
#dfs = [table_1, df_clear, table_6,table_j_1, table_4,Etakada_df_1, table_5, Labelvie_df_1, table_2,Etakada_df, table_3,Labelvie_df]

dfs = [table_6,one_line, table_j_1, one_line, one_line,table_4,one_line,Etakada_df_1,one_line,one_line, table_5,one_line, Labelvie_df_1,one_line,one_line, table_2,one_line,Etakada_df,one_line,one_line, table_3,one_line, Labelvie_df]
for i in dfs:
    y = i.to_csv("C:/Users/LAMIA/Desktop/Finance/Financial_rapport.csv", mode="a", sep=";", index= True, header=True)

