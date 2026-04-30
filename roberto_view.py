import pygame

# Colors
MARS_DIRT = (180, 80, 40)
SKY_DAY = (200, 150, 120)
SKY_SUNSET_BLUE = (100, 150, 220)
WHITE = (255, 255, 255)
STARSHIP_SILVER = (192, 192, 192)
PLAYER_COLOR = (50, 200, 50)

def render(screen, mars_game, launch_window_timer):
    # Determine Sky Color based on time left (Sunset Blue effect)
    # Let's say if timer is under 5 minutes (300 seconds), sky turns blue
    if launch_window_timer <= 300:
        # Interpolate between Day and Sunset Blue? Or just snap.
        current_sky = SKY_SUNSET_BLUE
    else:
        current_sky = SKY_DAY

    screen.fill(current_sky)

    # Draw Ground (Jezero Crater)
    ground_rect = pygame.Rect(0, 600, 1280, 120)
    pygame.draw.rect(screen, MARS_DIRT, ground_rect)

    # Draw Starship
    ship_rect = pygame.Rect(1000, 200, 150, 400)
    pygame.draw.rect(screen, STARSHIP_SILVER, ship_rect)

    # Draw Player
    # Ground is at y=600, player height = 50. So base y is 550.
    player_base_y = 550
    player_rect = pygame.Rect(200, player_base_y + mars_game.player_y, 40, 50)
    pygame.draw.rect(screen, PLAYER_COLOR, player_rect)

    # Render HUD
    font = pygame.font.SysFont(None, 36)
    
    hud_texts = [
        f"Timer: {int(launch_window_timer)}s",
        f"Bone Density: {mars_game.bone_density:.1f}%",
        f"Radiation: {mars_game.radiation:.1f}%",
        f"Methane: {mars_game.methane_fuel}/100",
        f"Power: {mars_game.power}",
        f"H2: {mars_game.h2_reserves} | CO2: {mars_game.co2_reserves}",
        "Controls: SPACE to Jump | MOUSE CLICK for Sabatier | ENTER to Launch"
    ]

    for i, text in enumerate(hud_texts):
        text_surface = font.render(text, True, WHITE)
        screen.blit(text_surface, (20, 20 + i * 40))
