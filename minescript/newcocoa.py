import minescript as m # type: ignore
import pynput
import threading
from minescript import EventQueue, EventType # type: ignore
from pynput.keyboard import Key, Controller
from minescript_plus import Util
import urllib.request
import json
import time

# ---------------- Core Variables ----------------
running = False
prev_pos = None
threshold = 20
stop_event = threading.Event()
bot_thread = None
current_pos = None
stop_reason = ""
warp_cooldown_until = 0  # Timestamp until which checks are paused
keyboard = Controller()
theyaw = 90
thepitch = -45
FINAL_X = -233
FINAL_Z = -81.5
currenty = None


#------------- farming time ----------------

def farming(stop_event):
    global running, warp_cooldown_until
    running = True
    m.echo("Farming started...")
    m.player_press_sneak(True)
    m.player_press_sneak(False)
    m.player_set_orientation(yaw=theyaw, pitch=thepitch)
    m.player_press_attack(True)
    m.player_press_backward(True)
    m.player_press_right(True)
    start_pos = m.player_position()
    direction = "back"

    # main loop: exit when stop_event is set or running becomes False
    while running and not stop_event.is_set():
        # reached final position?
        if abs(m.player_position()[0] - FINAL_X) < 0.5 and abs(m.player_position()[2] - FINAL_Z) < 0.5:
            m.player_press_backward(False)
            m.player_press_forward(False)
            m.player_press_left(False)
            m.player_press_right(False)
            m.echo("Reached final position. Stopping farming.")

            # to skip detection
            warp_cooldown_until = time.time() + 4.0

            # warp — use stop_event.wait so it can break early if stopped
            if stop_event.wait(0.5):
                break
            m.execute("/warp garden")
            if stop_event.wait(3.0):
                break

            # reset reference after warp
            start_pos = m.player_position()
            direction = "back"
            m.echo(f"Warp complete. New position: {start_pos}")

            # resume everything
            m.player_set_orientation(yaw=theyaw, pitch=thepitch)
            m.player_press_sneak(True)
            m.player_press_sneak(False)

        # check again for stop requests
        if stop_event.is_set():
            break
        m.player_position()[1] = currenty
        time.sleep(0.4)
        # movement logic
        if direction == "back":
            m.player_press_forward(False)
            m.player_press_backward(True)
            if currenty <= m.player_position()[1] + 0.5:
                m.echo("Flipping forward")
                m.player_press_backward(False)
                direction = "forward"
                stop_event.wait(0.9)
                m.echo("new position set")
                m.player_position()[1] = currenty
        elif direction == "forward":
            m.player_press_backward(False)
            m.player_press_forward(True)
            if currenty <= m.player_position()[1] + 0.5:
                m.echo("Flipping forward")
                m.player_press_backward(False)
                direction = "back"
                stop_event.wait(0.9)
                m.echo("new position set")
                m.player_position()[1] = currenty

        # small sleep to yield CPU and let checks be responsive
        time.sleep(0.05)

    # cleanup on exit
    m.player_press_backward(False)
    m.player_press_forward(False)
    m.player_press_left(False)
    m.player_press_right(False)
    m.player_press_attack(False)
    running = False
    m.echo("Farming stopped.")
# ---------------- Event Queue ----------------
# This loop listens for key events (F6 to start, F7 to stop) and manages the farming bot's lifecycle.
with EventQueue() as event_queue:
    event_queue.register_key_listener()
    m.echo("Press F6 to start farming, F7 to stop farming.")

    while True:
        event = event_queue.get()
        if event.type == EventType.KEY:
            if event.key == 295 and event.action == 1:
                stop_event.clear()
                bot_thread = threading.Thread(target=farming, args=(stop_event,), daemon=True)
                bot_thread.start()
            elif event.key == 296 and event.action == 1:
                stop_reason = "Stopped manually by player."
                m.echo(stop_reason + " Stopping farming.")
                stop_event.set()
                running = False
            elif event.key == 75:
                m.player_set_orientation(yaw = theyaw, pitch = thepitch)

