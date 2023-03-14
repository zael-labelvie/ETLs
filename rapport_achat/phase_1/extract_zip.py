import ftplib
import shutil
import os

FTP_HOST = "192.168.1.238"
FTP_USER = "selectftp"
FTP_PASS = "69!f%bHUY*2r"

print("Remove file from dierctory data_zip")
# Remove file from dossier data_zip
directory = "C:/Users/LAMIA/Desktop/data_zip"
files_in_directory = os.listdir(directory)
filtered_files = [file for file in files_in_directory if file.endswith(".zip")]
print("...")
for file in filtered_files:
    path_to_file = os.path.join(directory, file)
    os.remove(path_to_file)
# connect to the FTP server
print("Done")
print("Connect to server")
ftp = ftplib.FTP(FTP_HOST, FTP_USER, FTP_PASS)
print("...")
print("Done")
# force UTF-8 encoding
ftp.encoding = "utf-8"

# Dedection last file hypermarket et supermarket
file_name_hyper = sorted(ftp.nlst(), key=lambda x: ftp.voidcmd(f"MDTM {x}"))[-1]
file_name_super = sorted(ftp.nlst(), key=lambda x: ftp.voidcmd(f"MDTM {x}"))[-2]
print(file_name_hyper)

print("Download data from server")
# Upload file .zip hyper
with open(file_name_hyper, "wb") as file:
    # use FTP's RETR command to download the file
    ftp.retrbinary(f"RETR {file_name_hyper}", file.write)

# Upload file .zip super
with open(file_name_super, "wb") as file:
    # use FTP's RETR command to download the file
    ftp.retrbinary(f"RETR {file_name_super}", file.write)
print("Done")
print("Move file to directory data_zip")
shutil.move(f"C:/Users/LAMIA/PycharmProjects/ETLs/rapport_achat/phase_1/dist/{file_name_hyper}", "C:/Users/LAMIA/Desktop/data_zip")
shutil.move(f"C:/Users/LAMIA/PycharmProjects/ETLs/rapport_achat/phase_1/dist/{file_name_super}", "C:/Users/LAMIA/Desktop/data_zip")

# Remove all file ending with .ZIP
directory = "C:/Users/LAMIA/PycharmProjects/ETLs/rapport_achat/phase_1"
files_in_directory = os.listdir(directory)
filtered_files = [file for file in files_in_directory if file.endswith(".zip")]
for file in filtered_files:
    path_to_file = os.path.join(directory, file)
    os.remove(path_to_file)
print("Done")