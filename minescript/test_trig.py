def trig_time(target_x, target_y, target_z):
    player_pos = m.player_position()  # Call the function to get the position
    dx = target_x - player_pos[0]
    dy = target_y - player_pos[1]
    dz = target_z - player_pos[2]
    horizontal_dist = math.sqrt(dx**2 + dz**2)
    pitch = math.atan2(dy, horizontal_dist) * (180 / math.pi)
    yaw = math.atan2(dx, dz) * (180.0 / math.pi)
    return yaw, pitch


trig_time(input(), input(), input())