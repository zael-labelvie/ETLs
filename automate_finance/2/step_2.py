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
import time
import webbrowser
import pyautogui
import pandas as pd
import clipboard
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
locale.setlocale(locale.LC_ALL, 'fr_FR.UTF-8')


########################################################################################################## SEND EMAIL
yesterday = date.today() - datetime.timedelta(days=1)
yesterday = str(yesterday)
yesterday = "2022-06-25"


def send():
    fromaddr = "z.elmaataoui@labelvie.ma"
    toaddr = "a.benkira@labelvie.ma", "m.abid@labelvie.ma", "b.alfaidy@labelvie.ma", "h.tadlaoui@labelvie.ma"
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = ', '.join(toaddr)
    msg['Subject'] = "RAPPORT FINANCIER - SQUAD ECOMMERCE : {}".format(yesterday)
    body = """
Bonjour, 

Veuillez trouver ci-joint le rapport d'activité transactionnelle de Bringo by Carrefour du {}.

Nb : Ce mail est envoyé automatiquement.

Bonne réception,
Zakariyae 
""".format(yesterday)
    msg.attach(MIMEText(body, 'plain'))
    filename = "Financial_rapport - {}.csv".format(yesterday)
    attachment = open("C:/Users/LAMIA/Desktop/Finance/Financial_rapport.csv", "rb")
    p = MIMEBase('application', 'octet-stream')
    p.set_payload((attachment).read())
    encoders.encode_base64(p)
    p.add_header('Content-Disposition', "attachment; filename= %s" % filename)
    msg.attach(p)
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login(fromaddr, "Triwakof2022")
    text = msg.as_string()
    s.sendmail(fromaddr, toaddr, text)
    s.quit()
send()

def fin_3():
    for i in range(10):
        print(".................................................. Done {}".format(i))
    print(".................................................. Done")

fin_3()