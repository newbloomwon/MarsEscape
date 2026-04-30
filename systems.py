class EscapeFromMarsSystem:
    def __init__(self):
        self.is_alive = True
        
        # Biology Stats
        self.bone_density = 100.0
        self.radiation = 0.0
        
        # Resource Stats
        self.methane_fuel = 0.0
        self.power = 100.0
        self.h2_reserves = 100.0
        self.co2_reserves = 100.0
        
        # Physics State
        self.player_y = 0.0
        self.player_y_velocity = 0.0
        self.is_jumping = False
        
        # Inventory / Mass Limit
        self.scientific_samples_kg = 0.0

    def update_bio_decay(self, dt):
        # Bone density decays 1% per month, scaled down for gameplay purposes
        # Let's say 1 unit per minute
        self.bone_density -= (1.0 / 60.0) * dt
        
        # Radiation increases slowly
        self.radiation += (5.0 / 60.0) * dt
        
        if self.bone_density <= 0 or self.radiation >= 100:
            print("Mission Failure: Biological limits exceeded.")
            self.is_alive = False

    def run_sabatier_process(self):
        # CO2 + 4H2 -> CH4 + 2H2O
        if self.power >= 5 and self.h2_reserves >= 4 and self.co2_reserves >= 1:
            self.power -= 5
            self.h2_reserves -= 4
            self.co2_reserves -= 1
            self.methane_fuel += 10
            print("Sabatier Process Ran: +10 Methane")
        else:
            print("Cannot run Sabatier Process: Not enough resources or power.")
