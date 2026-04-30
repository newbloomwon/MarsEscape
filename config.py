SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

LAUNCH_WINDOW_SECONDS = 5400.0

# Physics tuning hooks
EARTH_GRAVITY_MPS2 = 9.807
MARS_GRAVITY_MPS2 = 3.721
MARS_GRAVITY_SCALE = MARS_GRAVITY_MPS2 / EARTH_GRAVITY_MPS2
MARS_GRAVITY_PX = 900.0 * MARS_GRAVITY_SCALE
BASE_MOVE_SPEED = 260.0
JUMP_VELOCITY = 430.0

# Systems tuning
INITIAL_CO2 = 120.0
INITIAL_H2 = 220.0
INITIAL_POWER = 100.0
BASE_REQUIRED_METHANE = 100.0
PAYLOAD_METHANE_PER_KG = 0.6

DUST_BUILDUP_RATE = 0.45
POWER_DRAIN_BASE = 0.22
POWER_DRAIN_DUST_FACTOR = 0.65

BONE_DECAY_RATE = 0.0028
RADIATION_RATE = 0.0075

SABATIER_CO2_NEEDED = 1.0
SABATIER_H2_NEEDED = 4.0
SABATIER_POWER_COST = 2.8

SOLAR_BRUSH_DUST_REDUCTION = 18.0
SOLAR_BRUSH_POWER_RESTORE = 8.0

SAVE_FILE_PATH = "mission_state.json"

DIFFICULTY_PRESETS = {
	"easy": {
		"label": "Easy",
		"launch_window_scale": 1.25,
		"bio_decay_scale": 0.75,
		"radiation_scale": 0.75,
		"power_drain_scale": 0.8,
		"required_methane_scale": 0.9,
	},
	"standard": {
		"label": "Standard",
		"launch_window_scale": 1.0,
		"bio_decay_scale": 1.0,
		"radiation_scale": 1.0,
		"power_drain_scale": 1.0,
		"required_methane_scale": 1.0,
	},
	"hard": {
		"label": "Hard",
		"launch_window_scale": 0.8,
		"bio_decay_scale": 1.3,
		"radiation_scale": 1.35,
		"power_drain_scale": 1.2,
		"required_methane_scale": 1.15,
	},
}