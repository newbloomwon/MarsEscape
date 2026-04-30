import json
import tempfile
import unittest
from pathlib import Path

import systems
from systems import EscapeFromMarsSystem


class EscapeFromMarsTests(unittest.TestCase):
    def test_sabatier_stoichiometry(self):
        game = EscapeFromMarsSystem()
        game.co2 = 5.0
        game.h2 = 20.0
        game.methane = 0.0
        game.h2o = 0.0
        game.power = 50.0

        game.run_sabatier_process()

        self.assertAlmostEqual(game.co2, 4.0)
        self.assertAlmostEqual(game.h2, 16.0)
        self.assertAlmostEqual(game.methane, 1.0)
        self.assertAlmostEqual(game.h2o, 2.0)
        self.assertLess(game.power, 50.0)

    def test_launch_gating_requires_stages_and_fuel(self):
        game = EscapeFromMarsSystem()
        game.methane = game.required_methane + 1.0

        game.attempt_launch(120.0)
        self.assertFalse(game.launched)

        game.power_ignition()
        game.prime_ignition()
        game.attempt_launch(120.0)
        self.assertTrue(game.launched)
        self.assertFalse(game.is_alive)

    def test_save_and_load_integrity(self):
        game = EscapeFromMarsSystem()
        game.co2 = 77.0
        game.h2 = 150.0
        game.methane = 12.0
        game.science_samples_kg = 3.0
        game.set_difficulty("hard")

        astronaut_state = {
            "x": 600.0,
            "y": 250.0,
            "vx": 0.0,
            "vy": 1.0,
            "on_ground": False,
        }

        old_path = systems.SAVE_FILE_PATH
        with tempfile.TemporaryDirectory() as tmp:
            systems.SAVE_FILE_PATH = str(Path(tmp) / "state.json")

            game.save_state(3210.5, astronaut_state)

            loaded = EscapeFromMarsSystem()
            data, message = loaded.load_state()

            self.assertIsNotNone(data)
            self.assertIn("loaded", message.lower())
            self.assertAlmostEqual(loaded.co2, 77.0)
            self.assertAlmostEqual(loaded.h2, 150.0)
            self.assertAlmostEqual(loaded.methane, 12.0)
            self.assertAlmostEqual(loaded.science_samples_kg, 3.0)
            self.assertEqual(loaded.difficulty_key, "hard")
            self.assertAlmostEqual(data["launch_window_timer"], 3210.5)
            self.assertEqual(data["astronaut"]["y"], 250.0)

            with Path(systems.SAVE_FILE_PATH).open("r", encoding="utf-8") as f:
                payload = json.load(f)
            self.assertIn("game", payload)
            self.assertIn("astronaut", payload)

        systems.SAVE_FILE_PATH = old_path


if __name__ == "__main__":
    unittest.main()
