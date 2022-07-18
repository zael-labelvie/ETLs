
import locale
import datetime
from datetime import date

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
locale.setlocale(locale.LC_ALL, 'fr_FR.UTF-8')


########################################################################################################## SEND EMAIL
yesterday = date.today() - datetime.timedelta(days=1)
yesterday = str(yesterday)
#yesterday = "2022-07-17"


def send():
    fromaddr = "z.elmaataoui@labelvie.ma"
    toaddr = "a.benkira@labelvie.ma", "m.abid@labelvie.ma", "b.alfaidy@labelvie.ma", "h.tadlaoui@labelvie.ma", "l.ezzahraoui@labelvie.ma", "c.elannab@labelvie.ma", "a.ghayour@labelvie.ma"
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
    attachment = open("C:/Users/elmaa/OneDrive/Bureau/rapport_financier/Financial_rapport.csv", "rb")
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