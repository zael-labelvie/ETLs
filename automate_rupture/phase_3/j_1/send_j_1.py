import locale
import datetime
from datetime import date
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
locale.setlocale(locale.LC_ALL, 'fr_FR.UTF-8')
import pandas as pd


########################################################################################################## SEND EMAIL
yesterday = date.today() - datetime.timedelta(days=1)
yesterday = str(yesterday)
#yesterday = "2023-02-05"


def send():
    fromaddr = "z.elmaataoui@labelvie.ma"
    toaddr ="m.safouane@labelvie.ma","h.ramzi@labelvie.ma","l.sadiki@labelvie.ma","o.jdar@labelvie.ma","a.mekouar@labelvie.ma","a.azzal-digiup@labelvie.ma","panoramique.respmag@labelvie.ma","anfaplace.respmag@labelvie.ma","m.filali@labelvie.ma","a.bouhout@labelvie.ma","t.soumane@labelvie.ma", "r.benbada@labelvie.ma", "m.najim@labelvie.ma", "r.aoua@labelvie.ma", "s.rabouh@labelvie.ma", "r.amezoug@labelvie.ma","k.houmaidy@labelvie.ma", "w.azizi@labelvie.ma", "ecommerce.1@labelvie.ma","m.sammama@labelvie.ma","m.lagzili@labelvie.ma","k.mehrat@labelvie.ma","s.elyassini@labelvie.ma","a.khatimy@labelvie.ma","o.erriahi@labelvie.ma","m.hamchach@labelvie.ma","k.ahzoum@labelvie.ma","r.ghouati@labelvie.ma","s.elmounadi@labelvie.ma","a.moutaouakkil@labelvie.ma", "n.faroukh@labelvie.ma"

    #toaddr = "a.azzal-digiup@labelvie.ma",
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = ', '.join(toaddr)
    msg['Subject'] = "ETAT DE RUPTURE JOURNALIER - SQUAD ECOMMERCE : {}".format(yesterday)
    body = """
Bonjour, 

Veuillez trouver ci-joint le rapport journalier sur l'état de rupture de Bringo by Carrefour du {}.

Nb : Ce mail est envoyé automatiquement.

Bonne réception,
Zakariyae 
""".format(yesterday)
    msg.attach(MIMEText(body, 'plain'))
    #filename = "Financial_rapport - {}.csv".format(yesterday)
    filename = "Etat Rupture Journalier {}.xls".format(yesterday)
    #attachment = open("C:/Users/elmaa/OneDrive/Bureau/rapport_financier/Financial_rapport.csv", "rb")
    attachment = open("C:/Users/LAMIA/Desktop/rapport_rupture/Etat Rupture Journalier {}.xls".format(yesterday), "rb")
    p = MIMEBase('application', 'octet-stream')
    p.set_payload((attachment).read())
    encoders.encode_base64(p)
    p.add_header('Content-Disposition', "attachment; filename= %s" % filename)
    msg.attach(p)
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login(fromaddr, "Bouskoura2020!")
    text = msg.as_string()
    s.sendmail(fromaddr, toaddr, text)
    s.quit()

def fin_3():
    for i in range(10):
        print(".................................................. Done {}".format(i))
    print(".................................................. Done")



r = pd.read_csv(r"C:/Users/LAMIA/Desktop/rapport_rupture/size_j_1.csv")
data = pd.DataFrame(r)
value = data.iloc[-1,0]
if value != 0:
    send()
    fin_3()
else:
    print("NB : Le tableau est vide, nous ne pouvons pas envoyer le fichier !!!!!!!!!!!!")
