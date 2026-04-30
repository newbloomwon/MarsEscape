# Escape from Mars (Michael Systems Slice)

This repo now has a working vertical slice for Michael's roadmap scope:

- Sabatier console logic and UI trigger
- Mass-management inventory (sample payload increases methane requirement)
- Biological death clock (bone density + radiation)
- Dust/power maintenance loop
- Launch window and 3-stage ignition sequence wiring
- Keyboard astronaut controller with Mars gravity tuning hooks
- Collision obstacles and minimap view for movement tuning
- Save/load mission state for fast balancing iterations
- Difficulty presets with startup selector
- Real-time FPS/frame-time performance panel
- One-key mission restart after failure
- In-game balance tuning panel (no file edits required)

## Quick Start

Dependency note: this project uses pygame-ce for Python 3.14 compatibility on macOS.

1. Create and activate a Python environment.
1. Install dependency:

```bash
pip install -r requirements.txt
```

1. Run:

```bash
python main.py
```

At startup, choose difficulty using keys `1`, `2`, or `3`.

## Controls

- Run Sabatier: converts reactants using `CO2 + 4H2 -> CH4 + 2H2O`
- +1 kg Sample / Drop 1 kg: adjusts payload mass and launch fuel requirement
- Brush Solar Panels: reduces dust buildup and restores power
- Power Ignition -> Prime Ignition -> Launch: staged launch sequence
- Move Astronaut: `A/D` or arrow keys
- Jump: `SPACE`
- Save State: `F5`
- Load State: `F9`
- Difficulty Select: `1` Easy, `2` Standard, `3` Hard
- Collision Debug Overlay: `F3`
- Balance Panel Toggle: `F2`
- Balance Panel Controls: `UP/DOWN` select, `LEFT/RIGHT` tune
- Restart After Failure: `R`

## Project Files

- `main.py`: Pygame loop, HUD, and UI buttons
- `systems.py`: Game state and automated scientific systems
- `controller.py`: astronaut movement controller for low-G integration
- `config.py`: central tuning constants (physics + systems)
- `MICHAEL_ROADMAP_CHECKLIST.md`: roadmap task list with acceptance criteria
- `tests/test_core.py`: automated checks for chemistry, launch gating, and save/load
- `build_standalone.sh`: macOS standalone app build script
- `requirements-dev.txt`: packaging dependencies (PyInstaller)

## Run Tests

```bash
python -m unittest discover -s tests
```

## Standalone Build (macOS)

```bash
./build_standalone.sh
```

Output app bundle:

- `dist/EscapeFromMars.app`

## Current Scope vs PRD

Implemented now:

- Core mission loop and fail states
- Countdown launch window
- Fuel generation and constraints
- Bio-decay and radiation pressure

Next integration points for team merge:

- Evan: low-gravity movement and physical controller integration
- Roberto: environment visuals, blue sunset timing cue, and audio muffling
