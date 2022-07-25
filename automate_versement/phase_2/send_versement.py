import locale
import datetime
from datetime import date
import pandas as pd
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
locale.setlocale(locale.LC_ALL, 'fr_FR.UTF-8')


########################################################################################################## SEND EMAIL
yesterday = date.today() - datetime.timedelta(days=1)
yesterday = str(yesterday)
#yesterday = "2022-07-24"


def send():
    fromaddr = "z.elmaataoui@labelvie.ma"
    toaddr = "h.ramzi@labelvie.ma", "pointprodelivery@gmail.com", "A.zouheir@labelvie.ma", "badii.hachguer@gmail.com", "k.naciri@labelvie.ma"
    #toaddr = "a.azzal-digiup@labelvie.ma",
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = ', '.join(toaddr)
    msg['Subject'] = "RAPPORT VERSEMENT - SQUAD ECOMMERCE : {}".format(yesterday)
    body = """
Bonjour, 

Veuillez trouver ci-joint le rapport d'activité transactionnelle de Bringo by Carrefour du {}.

Nb : Ce mail est envoyé automatiquement.

Bonne réception,
Zakariyae 
""".format(yesterday)
    msg.attach(MIMEText(body, 'plain'))
    #filename = "Livraison_rapport - {}.xlsx".format(yesterday)
    filename = "Versement_rapport - {}.xls".format(yesterday)
    #attachment = open("C:/Users/elmaa/OneDrive/Bureau/rapport_livraison/Livraison_rapport.xlsx", "rb")
    attachment = open("C:/Users/LAMIA/Desktop/rapport_versement/Versement_rapport.xls", "rb")
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

def fin_3():
    for i in range(10):
        print(".................................................. Done {}".format(i))
    print(".................................................. Done")


r = pd.read_csv(r"C:/Users/LAMIA/Desktop/rapport_versement/size.csv")
data = pd.DataFrame(r)
value = data.iloc[-1,0]
if value != 0:
    send()
    fin_3()
else:
    print("NB : Le tableau est vide, nous ne pouvons pas envoyer le fichier !!!!!!!!!!!!")