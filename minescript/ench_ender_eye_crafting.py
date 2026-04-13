import keyboard as kb 
import pyautogui as pag
import time


#slotx = None
#sloty = None
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
#def run(list):
#    for i in range(0,len(list), 2):
#        print(i)
#        for j in range(2):
#            kb.press('shift')
#        pag.click
#


#run(inv_r_1)



def run(slot):
    pag.moveTo(slot[0], slot[1])
    kb.press('shift')
    pag.click()
    time.sleep(0.1)
    pag.moveTo(1109, 373)
    time.sleep(0.1)
    pag.click()
    kb.release('shift')
    time.sleep(0.1)

    

def craft_eye():
    kb.press('escape')
    kb.release('escape')
    kb.press('y')
    kb.release('y')
    time.sleep(0.1)
    pag.moveTo(748, 280)
    kb.write('/recipe enchanted eye')
    time.sleep(0.1)
    kb.press('enter')
    kb.release('enter')
    time.sleep(0.1)
    pag.moveTo(741, 277)
    time.sleep(0.1)
    pag.click()
    time.sleep(0.1)
    pag.click()
    time.sleep(0.1)
    pag.moveTo(1020, 425)
    time.sleep(0.1)
    kb.press('shift')
    pag.click(button='right')
    kb.release('shift')
    time.sleep(0.1)
    pag.moveTo(1020, 425)
    pag.click()
    time.sleep(0.1)
    kb.press('escape')
    kb.release('escape')

def gfs(item):
    kb.press('y')
    kb.release('y')
    time.sleep(0.1)
    kb.write("/gfs " + item)
    time.sleep(0.1)
    kb.press('enter')
    kb.release('enter')

def go_back_to_craftin_menu():
    time.sleep(0.1)
    kb.press('y')
    kb.release('y')
    time.sleep(0.1)
    kb.write('/craft')
    kb.press('enter')
    kb.release('enter')

kb.wait('f6')
while True:
    if kb.is_pressed('space'):
        break
    else:
        run(s1)
        time.sleep(0.2)
        run(s2)
        time.sleep(0.2)
        run(s3)
        time.sleep(0.2)
        run(s4)
        time.sleep(0.2)
        run(s5)
        time.sleep(0.2)
        run(s6)
        time.sleep(0.2)
        run(s7)
        time.sleep(0.2)
        run(s8)
        time.sleep(0.2)
        run(s9)
        time.sleep(0.2)
        run(s10)
        time.sleep(0.2)
        run(s28)
        time.sleep(0.2)
        run(s29)
        time.sleep(0.2)
        run(s30)
        time.sleep(0.2)
        run(s31)
        time.sleep(0.2)
        run(s32)
        time.sleep(0.2)
        run(s33)
        time.sleep(0.2)
        run(s34)
        time.sleep(0.2)
        run(s35)
        time.sleep(0.2)
        craft_eye()
        time.sleep(0.2)
        gfs("BLAZE_ROD 1120")
        time.sleep(0.2)
        go_back_to_craftin_menu()
        time.sleep(2.0)
