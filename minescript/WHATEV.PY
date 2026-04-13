import minescript as m # type: ignore
import keyboard as kb 
import pyautogui as pag
import time


while True:
    if kb.is_pressed('f6'):
        x = m.getblock("~1 ~-2 ~1")
        m.echo(x)