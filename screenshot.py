### SCREENSHOT SECTION ###
import pyautogui
import time
import os
import webbrowser
from alerts import enviar_email

folder = "screenshots"

def screenshot(usertime):
    print("Start fun. Screenshot")
    print(usertime)
    #usertime=input("Enter the appropriate timer to take the screenshot: ")
    p = 1
    while True:
        print("Start while")
        x = "ScreenShot" + str(p) + ".png"
        sshot = pyautogui.screenshot()
        print("!!!!")
        print(x)
        sshot.save(os.path.join(folder,x))
        enviar_email(os.path.join(folder,x))
        p += 1
        min = int(usertime)*60
        time.sleep(min)
        pass
    print("END fun. ScreenShot")

def useropenfile():
    webbrowser.open(folder)

