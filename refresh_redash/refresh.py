import locale
import time
import webbrowser
import pyautogui
locale.setlocale(locale.LC_ALL, 'fr_FR.UTF-8')
import datetime






log = open('C:/Users/LAMIA/Desktop/logs.txt', 'a')


log.write("\n")
log.write(datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S") + ' ---------> Lancement du Browser'+ "\n")
webbrowser.open("https://redash-ro-live.bringo.ro/queries/23")
time.sleep(15)

log.write(datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S") + ' ---------> Lancement 1er Refresh de la page'+ "\n")
pyautogui.keyDown("ctrl")
pyautogui.press("enter")
pyautogui.keyUp("ctrl")
time.sleep(5)

log.write(datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S") + ' ---------> Lancement 2er Refresh de la page'+ "\n")
pyautogui.keyDown("ctrl")
pyautogui.press("enter")
pyautogui.keyUp("ctrl")
time.sleep(5)

log.write(datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S") + ' ---------> Lancement 3er Refresh de la page'+ "\n")
pyautogui.keyDown("ctrl")
pyautogui.press("enter")
pyautogui.keyUp("ctrl")
log.write(datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S") + ' ---------> Fin de refreshement de la page'+ "\n")

