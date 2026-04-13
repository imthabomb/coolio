import minescript as m # type: ignore
import threading
from minescript import EventQueue, EventType # type: ignore
from minescript_plus import Util
import urllib.request
import json
import time

# ---------------- Discord Webhook ----------------
WEBHOOK_URL = "butt"

def send_discord_message(message: str):
    """Send a message to Discord via webhook with proper headers."""
    try:
        data = json.dumps({"content": message}).encode("utf-8")
        headers = {
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0"
        }
        req = urllib.request.Request(WEBHOOK_URL, data=data, headers=headers)
        urllib.request.urlopen(req)
    except Exception as e:
        m.echo(f"Failed to send Discord message: {e}")

# ---------------- Core Variables ----------------
running = False
prev_pos = None
threshold = 20
stop_event = threading.Event()
bot_thread = None
current_pos = None
stop_reason = ""
warp_cooldown_until = 0  # Timestamp until which checks are paused

# ---------------- Helper Functions ----------------
def wait(ms: int):
    step = 50
    elapsed = 0
    while elapsed < ms and running and not stop_event.is_set():
        stop_event.wait(step / 1000.0)
        if not running:
            break
        elapsed += step

def position_updater():
    global current_pos
    while running and not stop_event.is_set():
        current_pos = m.player_position()
        stop_event.wait(0.05)

def monitor():
    global prev_pos, running, current_pos, stop_reason, warp_cooldown_until

    prev_pos = m.player_position()
    current_pos = prev_pos

    while running and not stop_event.is_set():
        # Skip checks during warp cooldown
        if time.time() < warp_cooldown_until:
            stop_event.wait(0.05)
            continue

        yaw_target = 0.0
        pitch_target = -58.50
        yaw0, pitch0 = m.player_orientation()

        if abs(yaw_target - yaw0) > 2.0 or abs(pitch_target - pitch0) > 2.0:
            stop_reason = "Yaw or pitch changed!"
            m.echo(stop_reason + " Stopping script.")
            running = False
            Util.play_sound(Util.get_soundevents().LIGHTNING_BOLT_THUNDER, Util.get_soundsource().WEATHER)
            stop_event.set()
            break

        pos = current_pos
        if pos is None:
            stop_event.wait(0.05)
            continue

        # Sudden movement check
        dx = abs(pos[0] - prev_pos[0])
        dy = abs(pos[1] - prev_pos[1])
        dz = abs(pos[2] - prev_pos[2])
        if dx > threshold or dy > threshold or dz > threshold:
            stop_reason = "Sudden position change detected!"
            m.echo(stop_reason + " Stopping script.")
            running = False
            Util.play_sound(Util.get_soundevents().LIGHTNING_BOLT_THUNDER, Util.get_soundsource().WEATHER)
            stop_event.set()
            break

        prev_pos = pos
        stop_event.wait(0.05)

def check_blocked():
    global prev_pos, running, stop_reason, warp_cooldown_until
    last_pos = m.player_position()
    stop_event.wait(2.7)

    while running and not stop_event.is_set():
        # Skip blocked check during warp cooldown
        if time.time() < warp_cooldown_until:
            last_pos = m.player_position()
            stop_event.wait(0.05)
            continue

        stop_event.wait(2.7)
        current_pos = m.player_position()
        dx = abs(current_pos[0] - last_pos[0])
        dy = abs(current_pos[1] - last_pos[1])
        dz = abs(current_pos[2] - last_pos[2])

        if dx < 0.01 and dy < 0.01 and dz < 0.01:
            stop_reason = "Player seems blocked by a block!"
            m.echo(stop_reason + " Stopping script.")
            running = False
            Util.play_sound(Util.get_soundevents().LIGHTNING_BOLT_THUNDER, Util.get_soundsource().WEATHER)
        last_pos = current_pos

# ---------------- Farming Logic ----------------
def farming():
    global running, prev_pos, stop_reason, warp_cooldown_until
    m.echo("Farming started...")
    running = True
    stop_event.clear()
    prev_pos = None
    stop_reason = ""

    m.player_set_orientation(yaw=0, pitch=-58.5)
    m.player_press_attack(True)
    m.player_press_forward(True)

    monitor_thread = threading.Thread(target=monitor, daemon=True)
    monitor_thread.start()
    blocked_thread = threading.Thread(target=check_blocked, daemon=True)
    blocked_thread.start()

    direction = True  # Initial movement direction
    start = m.player_position()[2]

    FINAL_X = 230
    FINAL_Z = 112.7

    while running and not stop_event.is_set():
        pos = m.player_position()
        current = pos[2]

        # ---------------- Warp Logic ----------------
        if abs(pos[0] - FINAL_X) < 1 and abs(pos[2] - FINAL_Z) < 1:
            m.echo("Final position reached! Warping back to start...")
            send_discord_message("Warped to the start")

            # Set 4-second cooldown to skip detection
            warp_cooldown_until = time.time() + 4.0

            # Stop all movement before warp
            m.player_press_forward(False)
            m.player_press_left(False)
            m.player_press_right(False)
            m.player_press_attack(False)

            stop_event.wait(0.5)  # settle motion
            m.execute("/warp garden")
            Util.play_sound(Util.get_soundevents().BELL_RESONATE, Util.get_soundsource().WEATHER)
            stop_event.wait(3.0)  # wait for warp to complete

            # Reset reference after warp
            new_pos = m.player_position()
            prev_pos = new_pos
            current_pos = new_pos
            direction = True
            start = new_pos[2]

            m.echo(f"Warp complete. New position: {new_pos}")

            # Resume movement
            m.player_set_orientation(yaw=0, pitch=-58.5)
            m.player_press_attack(True)
            m.player_press_forward(True)
            continue

        # ---------------- Farming Movement Logic ----------------
        if direction:
            m.player_press_right(True)
            if m.player_position()[2] >= start + 2:
                m.echo("Flipping left")
                m.player_press_right(False)
                direction = not direction
                stop_event.wait (2)
                m.echo("2 seconds passed")
                start = m.player_position()[2]
        else:
            m.player_press_left(True)
            if m.player_position()[2] >= start + 2:
                m.echo("Flipping right")
                m.player_press_left(False)
                direction = not direction
                stop_event.wait(2)
                m.echo("2 seconds passed")
                start = m.player_position()[2]
        stop_event.wait(0.05)

    running = False
    m.player_press_left(False)
    m.player_press_right(False)
    m.player_press_forward(False)
    m.player_press_attack(False)
    m.echo("Farming stopped.")

    # Send Discord message only if not stopped manually
    if stop_reason != "Stopped manually by player.":
        send_discord_message(f"{stop_reason} Probable macro check")

# ---------------- Event Queue ----------------
with EventQueue() as event_queue:
    event_queue.register_key_listener()
    m.echo("Press F6 to start farming, F7 to stop farming.")

    while True:
        event = event_queue.get()
        if event.type == EventType.KEY:
            if event.key == 295 and event.action == 1 and not running:
                bot_thread = threading.Thread(target=farming, daemon=True)
                bot_thread.start()
                pos_thread = threading.Thread(target=position_updater, daemon=True)
                pos_thread.start()
            elif event.key == 296 and event.action == 1 and running:
                stop_reason = "Stopped manually by player."
                m.echo(stop_reason + " Stopping farming.")
                stop_event.set()
                running = False
            elif event.key == 75:
                m.player_set_orientation(yaw=0, pitch=-58.5)
