import numpy as np
import cv2
from time import time
from time import sleep
import win32gui
import win32ui
import win32con
import win32api
import pyautogui
import keyboard
import tkinter
import wmi
from skimage.metrics import structural_similarity as compare_ssim
from impwincap import WindowCapture
from enum import Enum



readyimg=cv2.imread("blueline.png")

athand=[]
#cv2.imshow("img",img) 
on=False
pressed=False
while True:
    if keyboard.is_pressed(","):
        print("IN")
        on=True
    if keyboard.is_pressed("ü"):
        on=False
        state=-1
    print("in loop")
    if on:
        img=pyautogui.screenshot()
        img=np.array(img)
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        #print(img)
        # 556 240    1351 975
        imgready=img[0:1070,0:601]
        result=cv2.matchTemplate(imgready,readyimg,cv2.TM_CCOEFF_NORMED)
        min_val,max_val,min_loc,max_loc=cv2.minMaxLoc(result)
        print("inside 0",max_val)
        if max_val>0.801:
            pyautogui.click(max_loc[0], max_loc[1])
            pyautogui.press('backspace')
            sleep(0.1)
            pyautogui.press('space') 
        if max_val<0.8:
            pyautogui.moveTo(1910,1008)
            sleep(0.2)
            pyautogui.mouseDown(button='left')
            pyautogui.mouseUp(button='left')
            pyautogui.mouseDown(button='left')
            sleep(2.5)
            pyautogui.mouseUp(button='left')
            
        #1910,1008
    

    #cv2.imshow("scre",img)
    if keyboard.is_pressed('x'):
        print("in")
        break
    if cv2.waitKey(1) == 27:
            break

"""
    if state!=stateremember:
        timer=time()
    if time()-timer>20:
        pyautogui.mouseUp(button='left')
        pyautogui.mouseDown(button='left')
        pyautogui.mouseUp(button='left')
        state=0
        
    stateremember=state"""
     



































    









