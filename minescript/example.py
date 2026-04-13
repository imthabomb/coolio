import pyautogui # type: ignore
import keyboard as kb # type: ignore
arr = []

while True:
    kb.wait ('space')
    arr.append(pyautogui.position()[0])
    arr.append(pyautogui.position()[1])
    print(arr)  