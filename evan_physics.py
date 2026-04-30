GRAVITY = 3.721 # m/s^2

def trigger_jump(mars_game):
    if not mars_game.is_jumping:
        mars_game.is_jumping = True
        # Jump velocity is scaled; in lower gravity, jump feels higher
        # Weakened bone density might lower this initial velocity
        mars_game.player_y_velocity = -15.0 * (mars_game.bone_density / 100.0)

def apply_gravity(dt, mars_game):
    if mars_game.is_jumping:
        # Apply gravity to velocity
        mars_game.player_y_velocity += GRAVITY * dt * 10  # Scaled for pixel movement
        
        # Apply velocity to position
        mars_game.player_y += mars_game.player_y_velocity
        
        # Ground collision
        if mars_game.player_y >= 0:
            mars_game.player_y = 0
            mars_game.is_jumping = False
            mars_game.player_y_velocity = 0
