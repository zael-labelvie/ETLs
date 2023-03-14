import sys
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import pickle
import os
from google_auth_oauthlib.flow import Flow, InstalledAppFlow
from googleapiclient.discovery import build
import datetime
from google.auth.transport.requests import Request
from datetime import date





#token_drive_v3.pickle

#Delete file from directory
try:
    os.remove("C:/Users/LAMIA/PycharmProjects/ETLs/automate_rupture\pahse_2.1/upload_to_drive/dist/upload_to_drive/token_drive_v3.pickle")
except OSError as e:
    print(e)
else:
    print("File is deleted successfully")


########## Pour trouver le fichier client_secrets.json pyinstaller
def get_packaged_files_path():
    """Location of relative paths """
    if getattr(sys, 'frozen', False):
        path = sys._MEIPASS  # pylint: disable=no-member
    else:
        path = '.'

    return path

filepath = get_packaged_files_path()
client_secret_file = os.path.join(filepath, 'client_secrets.json')
print(client_secret_file)


########## Connexion API google drive
def Create_Service(client_secret_file, api_name, api_version, *scopes):
    print(client_secret_file, api_name, api_version, scopes, sep='-')
    CLIENT_SECRET_FILE = client_secret_file
    API_SERVICE_NAME = api_name
    API_VERSION = api_version
    SCOPES = [scope for scope in scopes[0]]
    print(SCOPES)

    cred = None
    pickle_file = f'token_{API_SERVICE_NAME}_{API_VERSION}.pickle'
    print("1")
    if os.path.exists(pickle_file):
        with open(pickle_file, 'rb') as token:
            cred = pickle.load(token)
    print("2")
    if not cred or not cred.valid:
        if cred and cred.expired and cred.refresh_token:
            cred.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
            print(CLIENT_SECRET_FILE)
            print("probleme here")
            cred = flow.run_local_server()
            print("probleme not here")
        with open(pickle_file, 'wb') as token:
            pickle.dump(cred, token)
            print("2.3")

    try:
        service = build(API_SERVICE_NAME, API_VERSION, credentials=cred, static_discovery=False)
        print(API_SERVICE_NAME, 'service created successfully')
        return service
    except Exception as e:
        print('Unable to connect.')
        print(e)
        return None

def convert_to_RFC_datetime(year=1900, month=1, day=1, hour=0, minute=0):
    dt = datetime.datetime(year, month, day, hour, minute, 0).isoformat() + 'Z'
    return dt

# table j-1
yesterday = date.today() - datetime.timedelta(days=1)
yesterday = str(yesterday)
#yesterday = "2023-02-26"


############### Accès
gauth = GoogleAuth()
drive = GoogleDrive(gauth)

CLIENT_SECRET_FILE = 'client_secrets.json'
API_NAME = 'drive'
API_VERSION = 'v3'
SCOPES = ['https://www.googleapis.com/auth/drive']
service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)


############# Move files to Directory Drive Archive

my_dict = {"1SBkSETdf2DrYWB7vRGDsRvrazKBEMBL5":"1miPaIxulYltLy25kdfNAjY0y_xTzRrd-",  ## zaer
           "14m-eYpslwcn1g6QfsfXqvgq3Kn3jm3iE":"1BDizafsbzjM0OlXwZ7QqijULQmOc29ym",  ## panoramique
            "1LB-v2eoZmjhzA6Bx5mkz3rp7fpmGkyLk":"1INcpkqnkjN_cJtSDBzitblEg6JmEdlgC", ## hassan2
            "1XFYUIJhbqT1ThJJIYetih6nU1jRCYWUM":"1XEJd19cLOiOGzZal69-9DnHQSU9LpYfk", ## anfaplace
            "1vApzqK43nqmz_ToN4kAoFwfkUqsxy7Md":"1BS8IdQYPUuZNLPUdBScj6mhm-4ufqC8d", ## ainsbaa
            "166jRV7IQd8yjZzmN-kI6MljWfySKqHlL":"15ZKq1qwhzPSJgSCzzv-Db5kq3-C00GTq", ## temara
            "1ChAPyKnvNZ7yk5EESSn_O064BCK2z812":"12HJhw2YQpW_rVSzrFAd5yJy0kBw_FMWz", ## sidi maarouf
            "1j-ek_I6MPRzi9yTOuddsXEd04c0SKoYA":"1YOFa1n5KAmTNfyQIcDzkIC45n4v-YvXd", ## darboazza
            "1WvU4-0s5EMCqHiyjhh-hBf9eNTm-_y6A":"1iYmbe5Pz4tbpVRhRDXxUzIzoZ-upnL9k"  ## Salé
           }
for source in my_dict :

    query = f"parents='{source}'"
    response = service.files().list(q=query).execute()
    files = response.get('files')
    nextPageToken = response.get('nextPageToken')

    while nextPageToken:
        response = service.files().list(q=query, pageToken=nextPageToken).execute()
        files.extend(response.get('files'))
        nextPageToken = response.get('nextPageToken')

    for f in files:
        if f['mimeType'] != 'application/vnd.google-apps.folder':
            service.files().update(
                fileId=f.get('id'),
                addParents=my_dict[source],
                removeParents=source
            ).execute()
            print("---------------------------------------")
            print("---------------------------------------")
            print("Move files to archive Done ! BRAVOO")
            print("---------------------------------------")
            print("---------------------------------------")
################################################### upload file to drive


# #### Panoramique
# upload_file = 'C:/Users/LAMIA/Desktop/rapport_rupture/Carrefour Market Panoramique {}.xlsx'.format(yesterday)
# gfile = drive.CreateFile({'parents': [{'id': '14m-eYpslwcn1g6QfsfXqvgq3Kn3jm3iE'}]})
# # Read file and set it as the content of this instance.
# gfile['title'] = 'Market Panoramique {}.xlsx'.format(yesterday)
# gfile.SetContentFile(upload_file)
# gfile.Upload() # Upload the file.
#
# #### Dar Bouazza
# upload_file = 'C:/Users/LAMIA/Desktop/rapport_rupture/Carrefour Dar Bouazza {}.xlsx'.format(yesterday)
# gfile = drive.CreateFile({'parents': [{'id': '1j-ek_I6MPRzi9yTOuddsXEd04c0SKoYA'}]})
# # Read file and set it as the content of this instance.
# gfile['title'] = 'Hyper Dar Bouazza {}.xlsx'.format(yesterday)
# gfile.SetContentFile(upload_file)
# gfile.Upload() # Upload the file.


# #### Anfaplace
# upload_file = 'C:/Users/LAMIA/Desktop/rapport_rupture/Carrefour Market Anfa Place {}.xlsx'.format(yesterday)
# gfile = drive.CreateFile({'parents': [{'id': '1XFYUIJhbqT1ThJJIYetih6nU1jRCYWUM'}]})
# # Read file and set it as the content of this instance.
# gfile['title'] = 'Market Anfaplace {}.xlsx'.format(yesterday)
# gfile.SetContentFile(upload_file)
# gfile.Upload() # Upload the file.
#
#
# #### Sidi Maaraouf
# upload_file = 'C:/Users/LAMIA/Desktop/rapport_rupture/Carrefour Sidi Maarouf {}.xlsx'.format(yesterday)
# gfile = drive.CreateFile({'parents': [{'id': '1ChAPyKnvNZ7yk5EESSn_O064BCK2z812'}]})
# # Read file and set it as the content of this instance.
# gfile['title'] = 'Hyper Sidi Maaraouf {}.xlsx'.format(yesterday)
# gfile.SetContentFile(upload_file)
# gfile.Upload() # Upload the file.
#
#
# #### Temara
# upload_file = 'C:/Users/LAMIA/Desktop/rapport_rupture/Carrefour Hyper Temara {}.xlsx'.format(yesterday)
# gfile = drive.CreateFile({'parents': [{'id': '166jRV7IQd8yjZzmN-kI6MljWfySKqHlL'}]})
# # Read file and set it as the content of this instance.
# gfile['title'] = 'Hyper Temara {}.xlsx'.format(yesterday)
# gfile.SetContentFile(upload_file)
# gfile.Upload() # Upload the file.
#
# #### Ainsebaa
# upload_file = 'C:/Users/LAMIA/Desktop/rapport_rupture/Carrefour Market Ain Sebaa {}.xlsx'.format(yesterday)
# gfile = drive.CreateFile({'parents': [{'id': '1vApzqK43nqmz_ToN4kAoFwfkUqsxy7Md'}]})
# # Read file and set it as the content of this instance.
# gfile['title'] = 'Market Ainsebaa {}.xlsx'.format(yesterday)
# gfile.SetContentFile(upload_file)
# gfile.Upload() # Upload the file.


#### Zaers
upload_file = 'C:/Users/LAMIA/Desktop/rapport_rupture/Carrefour Gourmet Zears {}.xlsx'.format(yesterday)
gfile = drive.CreateFile({'parents': [{'id': '1SBkSETdf2DrYWB7vRGDsRvrazKBEMBL5'}]})
# Read file and set it as the content of this instance.
gfile['title'] = 'Gourmet Zaers {}.xlsx'.format(yesterday)
gfile.SetContentFile(upload_file)
gfile.Upload()



# #### Hassan 2
# upload_file = 'C:/Users/LAMIA/Desktop/rapport_rupture/Carrefour Market Hassan 2 {}.xlsx'.format(yesterday)
# gfile = drive.CreateFile({'parents': [{'id': '1LB-v2eoZmjhzA6Bx5mkz3rp7fpmGkyLk'}]})
# # Read file and set it as the content of this instance.
# gfile['title'] = 'Market Hassan2 {}.xlsx'.format(yesterday)
# gfile.SetContentFile(upload_file)
# gfile.Upload() # Upload the file.
#
#
# #### Salé
# upload_file = 'C:/Users/LAMIA/Desktop/rapport_rupture/Carrefour Hyper Salé {}.xlsx'.format(yesterday)
# gfile = drive.CreateFile({'parents': [{'id': '1WvU4-0s5EMCqHiyjhh-hBf9eNTm-_y6A'}]})
# # Read file and set it as the content of this instance.
# gfile['title'] = 'Hyper Salé {}.xlsx'.format(yesterday)
# gfile.SetContentFile(upload_file)
# gfile.Upload() # Upload the file.


# upload_file_list = ['client_secrets.json']
# for upload_file in upload_file_list:
#     dfile = drive.CreateFile({'parents': [{'id': '1SBkSETdf2DrYWB7vRGDsRvrazKBEMBL5'}]})
#     # Read file and set it as the content of this instance.
#     dfile.SetContentFile(upload_file)
#     dfile.Upload() # Upload the file.