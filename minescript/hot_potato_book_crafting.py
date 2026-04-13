import keyboard as kb 
import pyautogui as pag
import time


s1=[674, 580]
s2=[750, 576]
s3=[810, 573]
s4=[888, 576]
s5=[959, 570]
s6=[1030, 573]
s7=[1099, 574]
s8=[1175, 574]
s9=[1246, 575]
s10=[669, 643]
s11=[754, 648]
s12=[816, 645]
s13=[888, 651]
s14=[966, 649]
s15=[1026, 646]
s16=[1109, 651]
s17=[1170, 645]
s18=[1240, 646]
s19=[674, 712]
s20=[759, 722]
s21=[823, 715]
s22=[891, 716]
s23=[958, 719]
s24=[1013, 719]
s25=[1081, 708]
s26=[1182, 717]
s27=[1241, 714]
s28=[684, 824]
s29=[767, 803]
s30=[823, 808]
s31=[890, 807]
s32=[971, 801]
s33=[1030, 803]
s34=[1093, 806]
s35=[1174, 800]


def craft_book():
    kb.press('y')
    kb.release('y')
    time.sleep(0.1)
    pag.moveTo(748, 280)
    kb.write('/recipe hot potato book')
    time.sleep(0.3)
    kb.press('enter')
    kb.release('enter')
    time.sleep(0.4)
    pag.moveTo(741, 277)
    time.sleep(0.1)
    pag.click()
    time.sleep(0.1)
    pag.click()
    time.sleep(0.1)
    pag.moveTo(1020, 425)
    for _ in range(0, 35):
        pag.click()
        time.sleep(0.7)
    kb.press('escape')
    kb.release('escape')
    
def sell_items():
    pag.click()
    time.sleep(1)
    pag.moveTo(661, 923)
    time.sleep(0.1)
    pag.click()
    time.sleep(1)
    pag.moveTo(1183, 344)
    pag.click()
    time.sleep(0.4)
    pag.moveTo(743, 353)
    pag.click()
    time.sleep(0.3)
    pag.moveTo(965, 342)
    pag.click()

    



kb.wait('f6')
for i in range (0,21):
    if kb.is_pressed('space'):
        break
    else:
        craft_book()
        time.sleep(1)
        sell_items()
        time.sleep(1)