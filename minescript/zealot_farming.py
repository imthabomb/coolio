import time
import threading
import system.lib.minescript as m  
from system.lib.minescript import EventQueue, EventType
import pyautogui 
import keyboard
import random
import math


CONFIRM_YAW_PITCH = False # If it should manuallly correct at the end (If you need exact Yaw and Pitch



def look(target_yaw, target_pitch, duration=0.5, steps=70):
    sy, sp = m.player_orientation()

    def angle_diff(a, b):
        return (b - a + 180) % 360 - 180

    dy = angle_diff(sy, target_yaw)
    dp = target_pitch - sp

    if abs(dy) < 1.0 and abs(dp) < 1.0:
        m.player_set_orientation(target_yaw, target_pitch)
        return

    step_time = duration / steps

    power = 5

    for i in range(1, steps + 1):
        t = i / steps

        if t < 0.5:
            s = 0.5 * (2 * t) ** power
        else:
            s = 1 - 0.5 * (2 * (1 - t)) ** power

        jy = (1 - abs(0.5 - t) * 2) * 0.2

        m.player_set_orientation(
            sy + dy * s + random.uniform(-jy, jy),
            sp + dp * s + random.uniform(-jy * 0.7, jy * 0.7)
        )

        time.sleep(step_time)

    if CONFIRM_YAW_PITCH:
        m.player_set_orientation(target_yaw, target_pitch)

def trig_time(target_x, target_y, target_z):
    player_pos = m.player_position()  # Call the function to get the position
    dx = target_x - player_pos[0]
    dy = target_y - player_pos[1]
    dz = target_z - player_pos[2]
    horizontal_dist = math.sqrt(dx**2 + dz**2)
    pitch = math.atan2(dy, horizontal_dist) * (180 / math.pi)
    yaw = math.atan2(dx, dz) * (180.0 / math.pi)
    return yaw, pitch

def has_line_of_sight(start_pos, end_pos, steps=20):
    """
    Checks if the line between start_pos and end_pos is clear (no non-air blocks).
    start_pos and end_pos are tuples/lists: (x, y, z)
    steps: number of points to check along the line (higher = more accurate but slower)
    """
    m.echo("Line of sight started")
    dx = end_pos[0] - start_pos[0]
    dy = end_pos[1] - start_pos[1]
    dz = end_pos[2] - start_pos[2]
    distance = math.sqrt(dx**2 + dy**2 + dz**2)
    
    if distance == 0:
        return True  # Same position, trivially clear
    
    for i in range(1, steps + 1):
        t = i / steps
        x = start_pos[0] + dx * t
        y = start_pos[1] + dy * t
        z = start_pos[2] + dz * t
        
        block = m.get_block(int(x), int(y), int(z))
        if block != 'minecraft:air':
            return False  # Obstruction found
        m.echo("Line of sight ended")
    
    return True  # Clear line of sight


for e in m.entities():
    
    if "Zealot Bruiser" in e.name and has_line_of_sight(m.player_position(), e.position) == True:
        m.echo(f"{e.name} passed checks")
        Target_pitch, Target_yaw = trig_time(e.position[0], e.position[1], e.position[2])
        m.echo(f"target pitch ={Target_pitch} Target yaw ={Target_yaw}")
        look(Target_pitch, Target_yaw)
        
        m.player_press_use(True)
        m.player_press_use(False)
        m.echo ("clicked")

