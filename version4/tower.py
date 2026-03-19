import pygame

class Tower(pygame.sprite.Sprite):
    def __init__(self, x, y, image, name, damage, range, cooldown_ms):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(center=(x, y))

        self.name = name
        self.damage = damage
        self.range = range
        self.cooldown_ms = cooldown_ms
        self.last_attack_time = 0


class SolarPanel(Tower):
    def __init__(self, x, y, image):
        super().__init__(x, y, image, "SOLAR", damage=3, range=170, cooldown_ms=180)


class RecyclingPlant(Tower):
    def __init__(self, x, y, image):
        super().__init__(x, y, image, "RECYCLE", damage=5, range=150, cooldown_ms=180)


class MangroveForest(Tower):
    def __init__(self, x, y, image):
        super().__init__(x, y, image, "MANGROVE", damage=7, range=120, cooldown_ms=220)