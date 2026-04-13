import keyboard as kb 
import pyautogui as pag
import time
import winsound


def cancel_order():
    pag.click()
    time.sleep(1)
    pag.moveTo(1022, 543)
    pag.click()
    time.sleep(1)
    pag.click()
    time.sleep(1)
    pag.moveTo(745, 288)
    pag.click()
    time.sleep(1)
    pag.moveTo(943, 346)
    pag.click()
    time.sleep(1)
    kb.press('escape')
    kb.release('escape')

    

def sell_items():
    pag.click()
    time.sleep(0.1)
    pag.moveTo(687, 927)
    time.sleep(0.5)
    pag.click()
    time.sleep(0.7)
    pag.moveTo(1183, 344)
    pag.click()
    time.sleep(0.7)
    pag.moveTo(743, 353)
    pag.click()
    time.sleep(0.7)
    pag.moveTo(965, 342)
    pag.click()


kb.wait('f6')
while True:
        for i in range (0,21):
                cancel_order()
                time.sleep(1)
                sell_items()
                time.sleep(1)
        time.sleep(60)
    