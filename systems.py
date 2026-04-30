import json
from pathlib import Path

from config import (
    BASE_REQUIRED_METHANE,
    BONE_DECAY_RATE,
    DIFFICULTY_PRESETS,
    DUST_BUILDUP_RATE,
    INITIAL_CO2,
    INITIAL_H2,
    INITIAL_POWER,
    PAYLOAD_METHANE_PER_KG,
    POWER_DRAIN_BASE,
    POWER_DRAIN_DUST_FACTOR,
    RADIATION_RATE,
    SABATIER_CO2_NEEDED,
    SABATIER_H2_NEEDED,
    SABATIER_POWER_COST,
    SAVE_FILE_PATH,
    SOLAR_BRUSH_DUST_REDUCTION,
    SOLAR_BRUSH_POWER_RESTORE,
)


class EscapeFromMarsSystem:
    def __init__(self):
        self.is_alive = True
        self.final_message = ""
        self.status_message = "Build methane before the launch window closes."

        # Resource state
        self.co2 = INITIAL_CO2
        self.h2 = INITIAL_H2
        self.methane = 0.0
        self.h2o = 0.0

        # Environmental state
        self.power = INITIAL_POWER
        self.dust_buildup = 0.0

        # Human factors
        self.bone_density = 100.0
        self.radiation_exposure = 0.0

        # Payload and launch requirement
        self.science_samples_kg = 0.0
        self.base_required_methane = BASE_REQUIRED_METHANE

        # Ignition state
        self.ignition_powered = False
        self.ignition_primed = False
        self.launched = False

        self.difficulty_key = "standard"
        self.bio_decay_scale = 1.0
        self.radiation_scale = 1.0
        self.power_drain_scale = 1.0
        self.timer_drain_scale = 1.0
        self.required_methane_scale_runtime = 1.0

    def set_difficulty(self, difficulty_key):
        preset = DIFFICULTY_PRESETS.get(difficulty_key, DIFFICULTY_PRESETS["standard"])
        self.difficulty_key = difficulty_key if difficulty_key in DIFFICULTY_PRESETS else "standard"
        self.bio_decay_scale = float(preset["bio_decay_scale"])
        self.radiation_scale = float(preset["radiation_scale"])
        self.power_drain_scale = float(preset["power_drain_scale"])
        self.timer_drain_scale = 1.0
        self.required_methane_scale_runtime = 1.0
        self.base_required_methane = BASE_REQUIRED_METHANE * float(preset["required_methane_scale"])

    @property
    def required_methane(self):
        # Payload stress tradeoff: each 1 kg sample requires extra methane.
        return (
            self.base_required_methane * self.required_methane_scale_runtime
            + (self.science_samples_kg * PAYLOAD_METHANE_PER_KG)
        )

    def get_balance_snapshot(self):
        return {
            "bio": self.bio_decay_scale,
            "radiation": self.radiation_scale,
            "power": self.power_drain_scale,
            "timer": self.timer_drain_scale,
            "required": self.required_methane_scale_runtime,
        }

    def adjust_balance_param(self, key, delta):
        if key == "bio":
            self.bio_decay_scale = max(0.5, min(2.0, self.bio_decay_scale + delta))
            return f"Bio decay scale: {self.bio_decay_scale:.2f}"
        if key == "radiation":
            self.radiation_scale = max(0.5, min(2.0, self.radiation_scale + delta))
            return f"Radiation scale: {self.radiation_scale:.2f}"
        if key == "power":
            self.power_drain_scale = max(0.5, min(2.0, self.power_drain_scale + delta))
            return f"Power drain scale: {self.power_drain_scale:.2f}"
        if key == "timer":
            self.timer_drain_scale = max(0.5, min(2.0, self.timer_drain_scale + delta))
            return f"Timer drain scale: {self.timer_drain_scale:.2f}"
        if key == "required":
            self.required_methane_scale_runtime = max(
                0.7, min(1.8, self.required_methane_scale_runtime + delta)
            )
            return f"Required methane scale: {self.required_methane_scale_runtime:.2f}"
        return "Unknown balance parameter"

    def end_mission(self, message):
        self.is_alive = False
        self.final_message = f"Mission End: {message}"
        self.status_message = message

    def update_auto_systems(self, dt):
        if not self.is_alive:
            return

        # Dust builds continuously; dust lowers net solar power generation.
        self.dust_buildup = min(100.0, self.dust_buildup + dt * DUST_BUILDUP_RATE)
        power_drain = POWER_DRAIN_BASE + (self.dust_buildup / 100.0) * POWER_DRAIN_DUST_FACTOR
        self.power = max(0.0, self.power - power_drain * self.power_drain_scale * dt)

        # Bio-decay and radiation are always ticking in the background.
        self.bone_density = max(0.0, self.bone_density - BONE_DECAY_RATE * self.bio_decay_scale * dt)
        self.radiation_exposure = min(100.0, self.radiation_exposure + RADIATION_RATE * self.radiation_scale * dt)

        if self.bone_density <= 0.0:
            self.end_mission("Astronaut mobility failure from bone-density loss")
        elif self.radiation_exposure >= 100.0:
            self.end_mission("Lethal radiation dose reached")
        elif self.power <= 0.0:
            self.end_mission("Power depleted before launch")

    def run_sabatier_process(self):
        if not self.is_alive:
            return

        if self.power < 3.0:
            self.status_message = "Insufficient power for Sabatier cycle."
            return

        co2_needed = SABATIER_CO2_NEEDED
        h2_needed = SABATIER_H2_NEEDED

        if self.co2 < co2_needed or self.h2 < h2_needed:
            self.status_message = "Insufficient reactants (need CO2 and 4x H2)."
            return

        # Stoichiometric conversion: CO2 + 4H2 -> CH4 + 2H2O
        self.co2 -= co2_needed
        self.h2 -= h2_needed
        self.methane += 1.0
        self.h2o += 2.0
        self.power = max(0.0, self.power - SABATIER_POWER_COST)
        self.status_message = "Sabatier cycle complete: +1 CH4, +2 H2O."

    def collect_science_sample(self):
        if not self.is_alive:
            return
        self.science_samples_kg += 1.0
        self.status_message = "Collected +1 kg sample. Fuel requirement increased."

    def drop_science_sample(self):
        if not self.is_alive:
            return
        if self.science_samples_kg <= 0:
            self.status_message = "No samples to drop."
            return
        self.science_samples_kg -= 1.0
        self.status_message = "Dropped 1 kg sample. Fuel requirement reduced."

    def brush_solar_panels(self):
        if not self.is_alive:
            return
        self.dust_buildup = max(0.0, self.dust_buildup - SOLAR_BRUSH_DUST_REDUCTION)
        self.power = min(100.0, self.power + SOLAR_BRUSH_POWER_RESTORE)
        self.status_message = "Panels brushed. Dust reduced and power restored."

    def power_ignition(self):
        if not self.is_alive:
            return
        if self.power < 15.0:
            self.status_message = "Need >= 15% power to arm ignition."
            return
        self.ignition_powered = True
        self.status_message = "Ignition powered."

    def prime_ignition(self):
        if not self.is_alive:
            return
        if not self.ignition_powered:
            self.status_message = "Power ignition first."
            return
        if self.methane < self.required_methane * 0.85:
            self.status_message = "Not enough methane to safely prime."
            return
        self.ignition_primed = True
        self.status_message = "Ignition primed."

    def attempt_launch(self, launch_window_timer):
        if not self.is_alive:
            return
        if not self.ignition_powered or not self.ignition_primed:
            self.status_message = "Complete POWER and PRIME stages first."
            return
        if launch_window_timer <= 0:
            self.end_mission("Launch attempt failed: window closed")
            return
        if self.methane < self.required_methane:
            self.status_message = "Launch blocked: methane below requirement."
            return

        self.launched = True
        self.end_mission("SUCCESS - Starship has launched from Jezero Crater")

    def to_dict(self):
        return {
            "is_alive": self.is_alive,
            "final_message": self.final_message,
            "status_message": self.status_message,
            "co2": self.co2,
            "h2": self.h2,
            "methane": self.methane,
            "h2o": self.h2o,
            "power": self.power,
            "dust_buildup": self.dust_buildup,
            "bone_density": self.bone_density,
            "radiation_exposure": self.radiation_exposure,
            "science_samples_kg": self.science_samples_kg,
            "base_required_methane": self.base_required_methane,
            "ignition_powered": self.ignition_powered,
            "ignition_primed": self.ignition_primed,
            "launched": self.launched,
            "difficulty_key": self.difficulty_key,
            "bio_decay_scale": self.bio_decay_scale,
            "radiation_scale": self.radiation_scale,
            "power_drain_scale": self.power_drain_scale,
            "timer_drain_scale": self.timer_drain_scale,
            "required_methane_scale_runtime": self.required_methane_scale_runtime,
        }

    def load_dict(self, data):
        self.is_alive = bool(data.get("is_alive", True))
        self.final_message = str(data.get("final_message", ""))
        self.status_message = str(data.get("status_message", self.status_message))
        self.co2 = float(data.get("co2", self.co2))
        self.h2 = float(data.get("h2", self.h2))
        self.methane = float(data.get("methane", self.methane))
        self.h2o = float(data.get("h2o", self.h2o))
        self.power = float(data.get("power", self.power))
        self.dust_buildup = float(data.get("dust_buildup", self.dust_buildup))
        self.bone_density = float(data.get("bone_density", self.bone_density))
        self.radiation_exposure = float(data.get("radiation_exposure", self.radiation_exposure))
        self.science_samples_kg = float(data.get("science_samples_kg", self.science_samples_kg))
        self.base_required_methane = float(data.get("base_required_methane", self.base_required_methane))
        self.ignition_powered = bool(data.get("ignition_powered", False))
        self.ignition_primed = bool(data.get("ignition_primed", False))
        self.launched = bool(data.get("launched", False))
        self.set_difficulty(str(data.get("difficulty_key", self.difficulty_key)))
        self.bio_decay_scale = float(data.get("bio_decay_scale", self.bio_decay_scale))
        self.radiation_scale = float(data.get("radiation_scale", self.radiation_scale))
        self.power_drain_scale = float(data.get("power_drain_scale", self.power_drain_scale))
        self.timer_drain_scale = float(data.get("timer_drain_scale", self.timer_drain_scale))
        self.required_methane_scale_runtime = float(
            data.get("required_methane_scale_runtime", self.required_methane_scale_runtime)
        )

    def save_state(self, launch_window_timer, astronaut_state):
        payload = {
            "launch_window_timer": float(launch_window_timer),
            "game": self.to_dict(),
            "astronaut": astronaut_state,
        }
        with Path(SAVE_FILE_PATH).open("w", encoding="utf-8") as f:
            json.dump(payload, f, indent=2)

    def load_state(self):
        save_path = Path(SAVE_FILE_PATH)
        if not save_path.exists():
            return None, "No mission_state.json found yet."

        with save_path.open("r", encoding="utf-8") as f:
            payload = json.load(f)

        game_data = payload.get("game", {})
        self.load_dict(game_data)
        launch_window_timer = float(payload.get("launch_window_timer", 0.0))
        astronaut = payload.get("astronaut", {})
        return {
            "launch_window_timer": launch_window_timer,
            "astronaut": astronaut,
        }, "State loaded from mission_state.json"