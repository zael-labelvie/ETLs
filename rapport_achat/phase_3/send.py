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
Today = date.today()
Today = str(Today)


def send():
    fromaddr = "z.elmaataoui@labelvie.ma"
    toaddr ="a.benkira@labelvie.ma","m.safouane@labelvie.ma","h.ramzi@labelvie.ma","l.sadiki@labelvie.ma","o.jdar@labelvie.ma","a.mekouar@labelvie.ma","a.azzal-digiup@labelvie.ma","panoramique.respmag@labelvie.ma","anfaplace.respmag@labelvie.ma","m.filali@labelvie.ma","a.bouhout@labelvie.ma","t.soumane@labelvie.ma", "r.benbada@labelvie.ma", "m.najim@labelvie.ma", "r.aoua@labelvie.ma", "s.rabouh@labelvie.ma", "r.amezoug@labelvie.ma","k.houmaidy@labelvie.ma", "w.azizi@labelvie.ma", "ecommerce.1@labelvie.ma","m.sammama@labelvie.ma","m.lagzili@labelvie.ma","k.mehrat@labelvie.ma","s.elyassini@labelvie.ma","a.khatimy@labelvie.ma","o.erriahi@labelvie.ma","m.hamchach@labelvie.ma","k.ahzoum@labelvie.ma","r.ghouati@labelvie.ma","s.elmounadi@labelvie.ma","a.ismaili-maltem@labelvie.ma","e.aba@labelvie.ma"
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = ', '.join(toaddr)
    msg['Subject'] = "RAPPORT ACHAT - SQUAD ECOMMERCE : {}".format(Today)
    body = """
Bonjour, 

Veuillez trouver ci-joint le rapport d'achat de Bringo by Carrefour du {}.

Nb : Ce mail est envoyé automatiquement.

Bonne réception,
Zakariyae 
""".format(Today)
    msg.attach(MIMEText(body, 'plain'))
    #filename = "Livraison_rapport - {}.xlsx".format(yesterday)
    filename = "Stock Price {}.xlsx".format(Today)
    #attachment = open("C:/Users/elmaa/OneDrive/Bureau/rapport_livraison/Livraison_rapport.xlsx", "rb")
    attachment = open("C:/Users/LAMIA/Desktop/rapport_achat/Stock Price {}.xlsx".format(Today), "rb")
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

r = pd.read_csv(r"C:/Users/LAMIA/Desktop/rapport_achat/size.csv")
data = pd.DataFrame(r)
value = data.iloc[-1,0]
if value != 0:
    send()
    fin_3()
else:
    print("NB : Le tableau est vide, nous ne pouvons pas envoyer le fichier !!!!!!!!!!!!")