# Michael Roadmap Checklist (Implementation + Acceptance)

## Phase 1: Foundation (7:45-8:00)

- [x] Establish shared GameState fields for fuel, power, health clocks, and launch status.
- [x] Add launch window countdown wiring in main loop.
- [x] Expose status messaging channel for team-wide debugging.

Acceptance criteria:
- HUD renders methane, required methane, power, dust, bone density, radiation, and timer.
- Mission ends when timer reaches zero.

## Phase 2: Systems Core (8:00-8:30)

- [x] Implement Sabatier process using stoichiometry: CO2 + 4H2 -> CH4 + 2H2O.
- [x] Add power constraints so chemistry depends on energy availability.
- [x] Implement sample payload tradeoff where extra sample mass increases methane requirement.
- [x] Add dust buildup and solar panel brushing loop.

Acceptance criteria:
- One Sabatier cycle consumes exact reactants and produces exact outputs.
- Sample collection changes launch fuel requirement in real time.
- Ignoring panel brushing leads to power pressure/failure.

## Phase 3: Bio-Decay and Failure Logic (8:30-8:50)

- [x] Add continuous bone density decay.
- [x] Add continuous radiation accumulation.
- [x] Trigger fail states for bio limits and power collapse.

Acceptance criteria:
- Bone density and radiation change every frame while mission is active.
- Mission ends with explicit reason when any lethal threshold is reached.

## Phase 4: Launch Sequence and Team Hand-off (8:50-9:00)

- [x] Wire three-stage launch sequence (Power -> Prime -> Launch).
- [x] Gate launch by required methane and launch-window validity.
- [x] Add simple astronaut controller hook for Evan's gravity tuning.
- [x] Add save/load for rapid balancing and test reruns.

Acceptance criteria:
- Launch cannot happen without powered and primed stages.
- Launch fails if methane is below requirement.
- Save file can restore mission values and astronaut position.

## Integration Notes for Team

- Evan integration point: movement constants in config.py and astronaut controller in controller.py.
- Roberto integration point: render over existing state values in main.py and react to timer thresholds.
- Shared authority source: systems.py for mission truth and validation.