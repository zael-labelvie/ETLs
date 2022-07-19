import locale
import time
import webbrowser
import pyautogui
locale.setlocale(locale.LC_ALL, 'fr_FR.UTF-8')



webbrowser.open("https://redash-ro-live.bringo.ro/queries/23")
time.sleep(15)
pyautogui.keyDown("ctrl")
pyautogui.press("enter")
pyautogui.keyUp("ctrl")
time.sleep(5)
pyautogui.keyDown("ctrl")
pyautogui.press("enter")
pyautogui.keyUp("ctrl")
time.sleep(5)
pyautogui.keyDown("ctrl")
pyautogui.press("enter")
pyautogui.keyUp("ctrl")
