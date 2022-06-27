import time
import webbrowser
import pyautogui
import pandas as pd
import clipboard


##################################################################### Automatisation Extraction ID data
def detection_url():
    webbrowser.open("https://datastudio.google.com/u/0/reporting/3a5b92df-0acf-46b2-ac3a-f0e5e54a31b5/page/nEjoC")
    time.sleep(30)
    one= pyautogui.moveTo(1494, 374)
    pyautogui.click(one)

    time.sleep(1)
    two= pyautogui.moveTo(1545, 484)
    pyautogui.click(two)


    time.sleep(1)
    tree= pyautogui.moveTo(751, 600)
    pyautogui.click(tree)

    time.sleep(1)
    four= pyautogui.moveTo(1138, 738)
    pyautogui.click(four)

    time.sleep(40)
    five = pyautogui.moveTo(936, 58)
    pyautogui.click(five)
    pyautogui.hotkey('ctrl', 'c')

    six = pyautogui.moveTo(1918, 1054)
    pyautogui.click(six)

    df_links = "C:/Users/LAMIA/Desktop/Finance/links.csv"
    f = open(df_links, 'a')
    y = clipboard.paste()
    f.write(str(y))
    f.write("\n")
    f.close()


def fin_1():
    for i in range(10):
        print(".................................................. Done {}".format(i))
    print(".................................................. Done")


detection_url()
fin_1()