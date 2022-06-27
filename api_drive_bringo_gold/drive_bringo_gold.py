import io
import sys
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import pickle
import os
from google_auth_oauthlib.flow import Flow, InstalledAppFlow
from googleapiclient.discovery import build
import datetime
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
from google.auth.transport.requests import Request


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
    # print(pickle_file)

    if os.path.exists(pickle_file):
        with open(pickle_file, 'rb') as token:
            cred = pickle.load(token)

    if not cred or not cred.valid:
        if cred and cred.expired and cred.refresh_token:
            cred.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
            cred = flow.run_local_server()

        with open(pickle_file, 'wb') as token:
            pickle.dump(cred, token)

    try:
        service = build(API_SERVICE_NAME, API_VERSION, credentials=cred)
        print(API_SERVICE_NAME, 'service created successfully')
        return service
    except Exception as e:
        print('Unable to connect.')
        print(e)
        return None

def convert_to_RFC_datetime(year=1900, month=1, day=1, hour=0, minute=0):
    dt = datetime.datetime(year, month, day, hour, minute, 0).isoformat() + 'Z'
    return dt


############### Accès
gauth = GoogleAuth()
drive = GoogleDrive(gauth)

CLIENT_SECRET_FILE = 'client_secrets.json'
API_NAME = 'drive'
API_VERSION = 'v3'
SCOPES = ['https://www.googleapis.com/auth/drive']
service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)

############### Extract files en se basant sur les IDs puis sorted title puis select ID
file_list = drive.ListFile({'q': "'1YZlQj-oE0vKlNpXyPFGuZfYWDWYcf_qc' in parents and trashed=false"}).GetList()
li =[]
print(li)
for file1 in file_list:
  li.append({'id': file1['id'], 'title' : file1['title']})
li.sort(key=lambda x: x.get('title'))

try:
    file_ids = [li[0].get('id')]
    file_names = ['bringo_gold.csv']
    for file_id, file_name in zip(file_ids, file_names):
        request = service.files().get_media(fileId=file_id)

        fh = io.BytesIO()
        downloader = MediaIoBaseDownload(fd=fh, request=request)
        done = False

        while not done:
            status, done = downloader.next_chunk()
            print('Download progress {0}'.format(status.progress() * 100))

        fh.seek(0)

        with open(os.path.join('C:/Users/LAMIA/Desktop/Bringo_gold', file_name), 'wb') as f:
            f.write(fh.read())
            f.close()
    li.clear()
except:
    print("Y a pas de fichiers dans le drive")

############# Move files to Directory Drive Archive
source_folder_id = '1YZlQj-oE0vKlNpXyPFGuZfYWDWYcf_qc'
target_folder_id = '1X1oB4yl9iwyQEhyIBunyHdZTV5JuoeCw'
query = f"parents='{source_folder_id}'"

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
            fileId = f.get('id'),
            addParents = target_folder_id,
            removeParents = source_folder_id
        ).execute()


