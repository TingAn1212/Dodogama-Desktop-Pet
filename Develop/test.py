import pyautogui
from time import sleep

while True:
    sleep(1)
    print(pyautogui.position().x,pyautogui.position().y)