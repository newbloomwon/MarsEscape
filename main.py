import pygame
import sys
from systems import EscapeFromMarsSystem
import evan_physics  # Mechanics & Physics Lead
import roberto_view  # Environment & Aesthetics Lead

def main():
    pygame.init()
    
    # 1. Initialize the shared state and systems
    # Michael: HUD, Sabatier, and Bio-Decay
    mars_game = EscapeFromMarsSystem()
    
    # Screen Setup
    screen = pygame.display.set_mode((1280, 720))
    pygame.display.set_caption("Escape from Mars: Sol 559")
    clock = pygame.time.Clock()

    # 2. Global Countdown Timer
    # Set for the Trans-Earth Injection window
    launch_window_timer = 5400 # 90 minutes in seconds

    while mars_game.is_alive:
        # Calculate Delta Time (seconds passed since last frame)
        dt = clock.tick(60) / 1000.0
        launch_window_timer -= dt

        # Check Win/Loss Condition on Timer
        if launch_window_timer <= 0:
            print("Mission Failure: Launch window closed.")
            mars_game.is_alive = False
            break

        # Event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            # Michael: Trigger Sabatier via UI click
            if event.type == pygame.MOUSEBUTTONDOWN:
                mars_game.run_sabatier_process()
                
            # Evan: Trigger Jump
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    evan_physics.trigger_jump(mars_game)
                # Test launch condition
                if event.key == pygame.K_RETURN:
                    if mars_game.methane_fuel >= 100:
                        print("Mission Success: Starship Launched!")
                        mars_game.is_alive = False
                    else:
                        print(f"Mission Failure: Insufficient fuel. (Methane: {mars_game.methane_fuel}/100)")

        # 3. Michael's Automated Logic
        # Ticks down bone density and radiation constantly
        mars_game.update_bio_decay(dt)

        # 4. Evan's Automated Logic
        # Implement 38% gravity (3.721 m/s²)
        evan_physics.apply_gravity(dt, mars_game)

        # 5. Roberto's Automated Logic
        # Render the Jezero Crater and Starship
        # If timer is low, trigger Blue Sunset Rayleigh scattering 
        roberto_view.render(screen, mars_game, launch_window_timer)

        pygame.display.flip()

    print("Game Over")

if __name__ == "__main__":
    main()
