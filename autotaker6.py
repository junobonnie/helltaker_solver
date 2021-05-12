# -*- coding: utf-8 -*-
"""
Created on Wed May 12 18:49:01 2021

@author: junob
"""
import pyautogui
import time as t

def move(direction, time = 0.1):
    pyautogui.press(direction)
    t.sleep(time)
    
t.sleep(5)
pyautogui.press('r')
t.sleep(5)

move('s')
move('d')
move('d', 1)
move('d')
move('w', 0.5)
move('w')
move('d')
move('d')
move('d')
move('w')
move('w')
move('a')
move('s')
move('s')
move('a', 0.5)
move('w')
move('a')
move('a')
move('s')
move('s')
move('s')
move('s')
move('a')
move('s')
move('a')
move('a')
move('a')
move('a')
move('a')
move('w')
move('w')
move('w', 1.7)
move('w')
move('a')
move('w')
move('w')
move('a', 0.8)
move('a')
move('w')
move('w')
move('d')
move('d')
move('w')