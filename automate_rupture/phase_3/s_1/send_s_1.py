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
today = datetime.date.today()
debut_semaine = today - datetime.timedelta(days=today.weekday(), weeks=1)
fin_semaine = today - datetime.timedelta(days=today.weekday(), weeks=1) + datetime.timedelta(days=6)
#debut_semaine = '2022-08-03'
#fin_semaine = '2022-08-07'


def send():
    fromaddr = "z.elmaataoui@labelvie.ma"
    toaddr ="a.benkira@labelvie.ma","m.safouane@labelvie.ma","h.ramzi@labelvie.ma","l.sadiki@labelvie.ma","o.jdar@labelvie.ma","a.mekouar@labelvie.ma","a.azzal-digiup@labelvie.ma","panoramique.respmag@labelvie.ma","anfaplace.respmag@labelvie.ma","m.filali@labelvie.ma","a.bouhout@labelvie.ma","t.soumane@labelvie.ma", "r.benbada@labelvie.ma", "m.najim@labelvie.ma", "r.aoua@labelvie.ma", "s.rabouh@labelvie.ma", "r.amezoug@labelvie.ma"
    #toaddr = "o.jdar@labelvie.ma",
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = ', '.join(toaddr)
    msg['Subject'] = "ETAT DE RUPTURE HEBDOMADAIRE - SQUAD ECOMMERCE : DU {} AU {}".format(str(debut_semaine), str(fin_semaine))
    body = """
Bonjour, 

Veuillez trouver ci-joint le rapport hebdomadaire sur l'état de rupture de Bringo by Carrefour du {} au {}.

Nb : Ce mail est envoyé automatiquement.

Bonne réception,
Zakariyae 
""".format(str(debut_semaine), str(fin_semaine))
    msg.attach(MIMEText(body, 'plain'))
    filename = "Etat Rupture Journalier du {} au {}.xls".format(str(debut_semaine), str(fin_semaine))
    attachment = open("C:/Users/LAMIA/Desktop/rapport_rupture/Etat Rupture Journalier du {} au {}.xls".format(str(debut_semaine), str(fin_semaine)), "rb")
    p = MIMEBase('application', 'octet-stream')
    p.set_payload((attachment).read())
    encoders.encode_base64(p)
    p.add_header('Content-Disposition', "attachment; filename= %s" % filename)
    msg.attach(p)
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login(fromaddr, "Bouskoura2020")
    text = msg.as_string()
    s.sendmail(fromaddr, toaddr, text)
    s.quit()

def fin_3():
    for i in range(10):
        print(".................................................. Done {}".format(i))
    print(".................................................. Done")




r = pd.read_csv(r"C:/Users/LAMIA/Desktop/rapport_rupture/size_s_1.csv")
data = pd.DataFrame(r)
value = data.iloc[-1,0]
if value != 0:
    send()
    fin_3()
else:
    print("NB : Le tableau est vide, nous ne pouvons pas envoyer le fichier !!!!!!!!!!!!")