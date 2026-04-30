import sys
import pygame

from config import DIFFICULTY_PRESETS, LAUNCH_WINDOW_SECONDS, SCREEN_HEIGHT, SCREEN_WIDTH
from controller import AstronautController
from systems import EscapeFromMarsSystem


def draw_text(screen, text, pos, font, color=(230, 235, 245)):
    surface = font.render(text, True, color)
    screen.blit(surface, pos)


def draw_button(screen, rect, label, font, enabled=True):
    base = (58, 86, 125) if enabled else (70, 70, 70)
    border = (150, 190, 220) if enabled else (105, 105, 105)
    pygame.draw.rect(screen, base, rect, border_radius=8)
    pygame.draw.rect(screen, border, rect, 2, border_radius=8)
    txt = font.render(label, True, (245, 250, 255) if enabled else (170, 170, 170))
    txt_rect = txt.get_rect(center=rect.center)
    screen.blit(txt, txt_rect)


def pick_difficulty(screen, clock, font_big, font_med):
    options = [
        (pygame.K_1, "easy", "1 - Easy"),
        (pygame.K_2, "standard", "2 - Standard"),
        (pygame.K_3, "hard", "3 - Hard"),
    ]

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                for key, preset, _label in options:
                    if event.key == key:
                        return preset

        screen.fill((18, 23, 31))
        draw_text(screen, "Select Difficulty", (470, 220), font_big)
        draw_text(screen, "Press 1, 2, or 3 to continue", (430, 266), font_med)

        y = 330
        for _key, preset, label in options:
            p = DIFFICULTY_PRESETS[preset]
            detail = (
                f"Window x{p['launch_window_scale']} | Bio x{p['bio_decay_scale']} | "
                f"Rad x{p['radiation_scale']} | Power x{p['power_drain_scale']}"
            )
            draw_text(screen, label, (450, y), font_med)
            draw_text(screen, detail, (450, y + 28), font_med)
            y += 90

        pygame.display.flip()
        clock.tick(30)


def draw_minimap(screen, map_rect, astronaut_zone, astronaut, obstacles):
    pygame.draw.rect(screen, (24, 35, 46), map_rect, border_radius=8)
    pygame.draw.rect(screen, (86, 110, 136), map_rect, 2, border_radius=8)

    scale_x = map_rect.width / astronaut_zone.width
    scale_y = map_rect.height / astronaut_zone.height

    for obstacle in obstacles:
        ox = map_rect.left + int((obstacle.x - astronaut_zone.x) * scale_x)
        oy = map_rect.top + int((obstacle.y - astronaut_zone.y) * scale_y)
        ow = max(2, int(obstacle.width * scale_x))
        oh = max(2, int(obstacle.height * scale_y))
        pygame.draw.rect(screen, (140, 120, 100), (ox, oy, ow, oh), border_radius=2)

    a = astronaut.get_rect()
    ax = map_rect.left + int((a.x - astronaut_zone.x) * scale_x)
    ay = map_rect.top + int((a.y - astronaut_zone.y) * scale_y)
    aw = max(2, int(a.width * scale_x))
    ah = max(2, int(a.height * scale_y))
    pygame.draw.rect(screen, (196, 216, 235), (ax, ay, aw, ah), border_radius=2)


def draw_difficulty_overlay(screen, game, preset, font_small):
    panel = pygame.Rect(520, 36, 450, 96)
    pygame.draw.rect(screen, (33, 47, 62), panel, border_radius=8)
    pygame.draw.rect(screen, (92, 126, 159), panel, 2, border_radius=8)
    draw_text(screen, f"Preset: {preset['label']} ({game.difficulty_key})", (534, 48), font_small)
    draw_text(
        screen,
        (
            f"Window x{preset['launch_window_scale']} | Bio x{preset['bio_decay_scale']} | "
            f"Radiation x{preset['radiation_scale']}"
        ),
        (534, 72),
        font_small,
    )
    draw_text(screen, f"Power Drain x{preset['power_drain_scale']}", (534, 96), font_small)


def draw_perf_overlay(screen, fps, frame_ms, font_small):
    panel = pygame.Rect(1040, 296, 180, 54)
    pygame.draw.rect(screen, (32, 45, 56), panel, border_radius=8)
    pygame.draw.rect(screen, (86, 110, 136), panel, 2, border_radius=8)
    draw_text(screen, f"FPS: {fps:.1f}", (1050, 307), font_small)
    draw_text(screen, f"Frame: {frame_ms:.2f} ms", (1050, 328), font_small)


def draw_balance_panel(screen, game, selected_index, font_small):
    panel = pygame.Rect(980, 360, 260, 158)
    pygame.draw.rect(screen, (36, 50, 64), panel, border_radius=8)
    pygame.draw.rect(screen, (126, 159, 192), panel, 2, border_radius=8)
    draw_text(screen, "Balance Tuning (F2)", (994, 370), font_small)
    draw_text(screen, "Up/Down select, Left/Right tune", (994, 392), font_small)

    snapshot = game.get_balance_snapshot()
    rows = [
        ("Bio", snapshot["bio"]),
        ("Rad", snapshot["radiation"]),
        ("Power", snapshot["power"]),
        ("Timer", snapshot["timer"]),
        ("Fuel Req", snapshot["required"]),
    ]
    for idx, (label, value) in enumerate(rows):
        color = (220, 235, 255) if idx == selected_index else (170, 185, 205)
        draw_text(screen, f"{label}: {value:.2f}", (994, 418 + idx * 20), font_small, color)


def run_session(screen, clock, font_small, font_med, font_big):
    pygame.init()
    pygame.display.set_caption("Escape from Mars | Michael Systems Slice")

    difficulty = pick_difficulty(screen, clock, font_big, font_med)

    game = EscapeFromMarsSystem()
    game.set_difficulty(difficulty)
    launch_window_timer = LAUNCH_WINDOW_SECONDS * DIFFICULTY_PRESETS[difficulty]["launch_window_scale"]
    astronaut_zone = pygame.Rect(520, 150, 700, 320)
    mini_map_rect = pygame.Rect(1040, 186, 180, 100)
    astronaut = AstronautController(astronaut_zone)
    obstacles = [
        pygame.Rect(610, 390, 160, 24),
        pygame.Rect(840, 335, 140, 20),
        pygame.Rect(1020, 285, 110, 18),
    ]
    debug_collision = False
    show_balance_panel = False
    balance_keys = ["bio", "radiation", "power", "timer", "required"]
    balance_index = 0

    btn_process = pygame.Rect(36, 600, 220, 50)
    btn_collect = pygame.Rect(276, 600, 220, 50)
    btn_drop = pygame.Rect(516, 600, 220, 50)
    btn_brush = pygame.Rect(756, 600, 220, 50)
    btn_power = pygame.Rect(996, 540, 240, 38)
    btn_prime = pygame.Rect(996, 588, 240, 38)
    btn_launch = pygame.Rect(996, 636, 240, 38)

    while game.is_alive:
        frame_ms = clock.tick(60)
        dt = frame_ms / 1000.0
        launch_window_timer -= dt * game.timer_drain_scale

        if launch_window_timer <= 0:
            game.end_mission("Missed trans-Earth injection window")

        game.update_auto_systems(dt)
        keys = pygame.key.get_pressed()
        astronaut.update(dt, keys, game.bone_density, obstacles=obstacles)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    astronaut.try_jump()
                elif event.key == pygame.K_F5:
                    game.save_state(launch_window_timer, astronaut.to_dict())
                    game.status_message = "Saved mission state to mission_state.json"
                elif event.key == pygame.K_F9:
                    data, message = game.load_state()
                    if data is not None:
                        launch_window_timer = float(data["launch_window_timer"])
                        astronaut.load_dict(data["astronaut"])
                    game.status_message = message
                elif event.key == pygame.K_F3:
                    debug_collision = not debug_collision
                    game.status_message = f"Collision debug {'ON' if debug_collision else 'OFF'}"
                elif event.key == pygame.K_F2:
                    show_balance_panel = not show_balance_panel
                    game.status_message = f"Balance panel {'ON' if show_balance_panel else 'OFF'}"
                elif event.key == pygame.K_UP and show_balance_panel:
                    balance_index = (balance_index - 1) % len(balance_keys)
                elif event.key == pygame.K_DOWN and show_balance_panel:
                    balance_index = (balance_index + 1) % len(balance_keys)
                elif event.key == pygame.K_LEFT and show_balance_panel:
                    message = game.adjust_balance_param(balance_keys[balance_index], -0.05)
                    game.status_message = message
                elif event.key == pygame.K_RIGHT and show_balance_panel:
                    message = game.adjust_balance_param(balance_keys[balance_index], 0.05)
                    game.status_message = message

            if event.type == pygame.MOUSEBUTTONDOWN:
                if btn_process.collidepoint(event.pos):
                    game.run_sabatier_process()
                elif btn_collect.collidepoint(event.pos):
                    game.collect_science_sample()
                elif btn_drop.collidepoint(event.pos):
                    game.drop_science_sample()
                elif btn_brush.collidepoint(event.pos):
                    game.brush_solar_panels()
                elif btn_power.collidepoint(event.pos):
                    game.power_ignition()
                elif btn_prime.collidepoint(event.pos):
                    game.prime_ignition()
                elif btn_launch.collidepoint(event.pos):
                    game.attempt_launch(launch_window_timer)

        screen.fill((22, 28, 36))
        pygame.draw.rect(screen, (35, 46, 58), (20, 20, 1240, 500), border_radius=10)
        pygame.draw.rect(screen, (42, 58, 74), (20, 540, 1240, 160), border_radius=10)

        draw_text(screen, "Escape from Mars - Systems Command", (36, 36), font_big)
        draw_text(screen, f"Timer: {max(0, launch_window_timer):.1f}s", (36, 84), font_med)
        draw_text(screen, f"Methane: {game.methane:.1f} / {game.required_methane:.1f}", (36, 124), font_med)
        draw_text(screen, f"CO2: {game.co2:.1f}", (36, 160), font_med)
        draw_text(screen, f"H2: {game.h2:.1f}", (36, 196), font_med)
        draw_text(screen, f"Water: {game.h2o:.1f}", (36, 232), font_med)
        draw_text(screen, f"Power: {game.power:.1f}%", (36, 268), font_med)
        draw_text(screen, f"Dust: {game.dust_buildup:.1f}%", (36, 304), font_med)
        draw_text(screen, f"Bone Density: {game.bone_density:.2f}%", (36, 340), font_med)
        draw_text(screen, f"Radiation: {game.radiation_exposure:.2f}%", (36, 376), font_med)
        draw_text(screen, f"Samples: {game.science_samples_kg:.1f} kg", (36, 412), font_med)

        draw_difficulty_overlay(screen, game, DIFFICULTY_PRESETS[game.difficulty_key], font_small)
        draw_text(screen, "Sabatier Reaction: CO2 + 4H2 -> CH4 + 2H2O", (520, 140), font_small)
        draw_text(screen, "Launch sequence: POWER -> PRIME -> LAUNCH", (520, 164), font_small)
        draw_text(
            screen,
            "Move: A/D or arrows | Jump: SPACE | Save: F5 | Load: F9 | Debug: F3 | Balance: F2",
            (520, 472),
            font_small,
        )

        pygame.draw.rect(screen, (30, 40, 53), astronaut_zone, border_radius=8)
        pygame.draw.rect(screen, (74, 98, 126), astronaut_zone, 2, border_radius=8)
        for obstacle in obstacles:
            pygame.draw.rect(screen, (128, 108, 89), obstacle, border_radius=4)
        astronaut.draw(screen)

        if debug_collision:
            for obstacle in obstacles:
                pygame.draw.rect(screen, (232, 118, 94), obstacle, 2)
            pygame.draw.rect(screen, (114, 226, 188), astronaut.get_rect(), 2)

        draw_minimap(screen, mini_map_rect, astronaut_zone, astronaut, obstacles)
        draw_perf_overlay(screen, clock.get_fps(), frame_ms, font_small)
        if show_balance_panel:
            draw_balance_panel(screen, game, balance_index, font_small)

        stages = [
            ("Powered", game.ignition_powered),
            ("Primed", game.ignition_primed),
            ("Launched", game.launched),
        ]
        for i, (label, active) in enumerate(stages):
            color = (90, 185, 125) if active else (140, 140, 140)
            draw_text(screen, f"{label}: {'YES' if active else 'NO'}", (996, 84 + i * 30), font_small, color)

        draw_button(screen, btn_process, "Run Sabatier", font_small)
        draw_button(screen, btn_collect, "+1 kg Sample", font_small)
        draw_button(screen, btn_drop, "Drop 1 kg", font_small)
        draw_button(screen, btn_brush, "Brush Solar Panels", font_small)

        draw_button(screen, btn_power, "Power Ignition", font_small)
        draw_button(screen, btn_prime, "Prime Ignition", font_small, enabled=game.ignition_powered)
        draw_button(
            screen,
            btn_launch,
            "Launch",
            font_small,
            enabled=game.ignition_powered and game.ignition_primed,
        )

        draw_text(screen, f"Status: {game.status_message}", (36, 556), font_small)

        if not game.is_alive:
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((8, 8, 8, 170))
            screen.blit(overlay, (0, 0))
            draw_text(screen, game.final_message, (120, 300), font_big)
            draw_text(screen, "Press R to restart or close window to exit.", (120, 350), font_med)

        pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                return "restart"


if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    font_small = pygame.font.SysFont("menlo", 18)
    font_med = pygame.font.SysFont("menlo", 24)
    font_big = pygame.font.SysFont("menlo", 32)

    while True:
        result = run_session(screen, clock, font_small, font_med, font_big)
        if result == "quit":
            break

    pygame.quit()
    sys.exit()