# -*- coding: utf-8 -*-
"""
Created on Sun May 16 19:44:37 2021
ddwd
@author: junob
"""

import pyautogui
import time as t

def move(direction, time = 0.1):
    pyautogui.press(direction)
    t.sleep(time)
    
t.sleep(5)    
pyautogui.press('escape')
pyautogui.press('r')
t.sleep(3)

move('d')
move('d')
move('d')
move('d', 2.5)
move('a')
move('a')
move('a')
move('a')
move('a', 0.5)
move('a', 1)
move('w', 0.5)
move('w')
move('d')
move('d')
move('w', 0.5)
move('s', 4)
move('w', 0.3)
move('a')
move('a')
move('s')
move('s')
move('s')
move('s', 2.5)
move('w')
move('s', 0.5)
move('d')
move('d')
move('d')
move('d')
move('d')
move('d')
move('d', 5)
move('w', 0.5)
move('s', 2)
move('w')