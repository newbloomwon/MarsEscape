import pygame

from config import BASE_MOVE_SPEED, JUMP_VELOCITY, MARS_GRAVITY_PX


class AstronautController:
    def __init__(self, play_area):
        self.play_area = play_area
        self.width = 24
        self.height = 42
        self.x = float(play_area.centerx)
        self.y = float(play_area.bottom - self.height)
        self.vx = 0.0
        self.vy = 0.0
        self.on_ground = True

    def try_jump(self):
        if self.on_ground:
            self.vy = -JUMP_VELOCITY
            self.on_ground = False

    def get_rect(self):
        return pygame.Rect(int(self.x), int(self.y), self.width, self.height)

    def update(self, dt, keys, bone_density, obstacles=None):
        if obstacles is None:
            obstacles = []

        move_scale = max(0.35, bone_density / 100.0)
        speed = BASE_MOVE_SPEED * move_scale

        self.vx = 0.0
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.vx = -speed
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.vx = speed

        self.vy += MARS_GRAVITY_PX * dt

        self.x += self.vx * dt

        current = self.get_rect()
        for obstacle in obstacles:
            if current.colliderect(obstacle):
                if self.vx > 0:
                    self.x = float(obstacle.left - self.width)
                elif self.vx < 0:
                    self.x = float(obstacle.right)
                current = self.get_rect()

        self.y += self.vy * dt
        self.on_ground = False

        current = self.get_rect()
        for obstacle in obstacles:
            if current.colliderect(obstacle):
                if self.vy > 0:
                    self.y = float(obstacle.top - self.height)
                    self.vy = 0.0
                    self.on_ground = True
                elif self.vy < 0:
                    self.y = float(obstacle.bottom)
                    self.vy = 0.0
                current = self.get_rect()

        min_x = float(self.play_area.left)
        max_x = float(self.play_area.right - self.width)
        if self.x < min_x:
            self.x = min_x
        elif self.x > max_x:
            self.x = max_x

        floor_y = float(self.play_area.bottom - self.height)
        if self.y >= floor_y:
            self.y = floor_y
            self.vy = 0.0
            self.on_ground = True

    def draw(self, screen):
        body = self.get_rect()
        visor = pygame.Rect(body.x + 4, body.y + 8, body.width - 8, 10)
        pygame.draw.rect(screen, (195, 210, 228), body, border_radius=6)
        pygame.draw.rect(screen, (80, 122, 162), visor, border_radius=3)

    def to_dict(self):
        return {
            "x": self.x,
            "y": self.y,
            "vx": self.vx,
            "vy": self.vy,
            "on_ground": self.on_ground,
        }

    def load_dict(self, data):
        self.x = float(data.get("x", self.x))
        self.y = float(data.get("y", self.y))
        self.vx = float(data.get("vx", 0.0))
        self.vy = float(data.get("vy", 0.0))
        self.on_ground = bool(data.get("on_ground", False))