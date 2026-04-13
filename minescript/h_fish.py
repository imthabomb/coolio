from minescript import entities, player_press_use, echo, player,player_orientation # type: ignore
from time import sleep
import math

OldY = 9999 # cant be none becuz has to have a typ or smthg
NewRound = True

def CheckMovement(Y):
    while True:
        sleep(.05)
        for entity in entities():
            if entity.name == "Fishing Bobber":
                NewX, NewY, NewZ = entity.position
                if (NewY-Y)  < -.1:
                    return NewY, True
                return NewY, False
        return Y, False

while True:
    sleep(.1)
    if NewRound:
        player_press_use(True)
        player_press_use(False)
        NewRound = False
        sleep(3)

    OldY,Bite = CheckMovement(OldY)

    if Bite == True:
        player_press_use(True)
        player_press_use(False)
        NewRound = True
        sleep(.5) 