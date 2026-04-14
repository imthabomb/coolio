import math

def trig_time(target_x, target_y, target_z):
      # Call the function to get the position
    dx = target_x - 0
    dy = target_y - 0
    dz = target_z - 0

    horizontal_dist = math.sqrt(dx**2 + dz**2)
    pitch = math.atan2(dy, dx) * (180 / math.pi)
    yaw = math.atan2(dx, dz) * (180.0 / math.pi)
    return yaw, pitch
10
10


x=input("whats x")
y=input("whats y")
z=input("whats z")

print(trig_time(int(x), int(y), int(z)))