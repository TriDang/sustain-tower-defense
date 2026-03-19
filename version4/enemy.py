import pygame

class Enemy(pygame.sprite.Sprite):
    def __init__(self, path, image, speed, health, enemy_type):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(center=path[0])

        self.path = path
        self.target_index = 1
        self.speed = speed
        self.health = health
        self.max_health = health
        self.type = enemy_type
        self.reached_end = False

    def update(self):
        if self.reached_end:
            return

        if self.target_index >= len(self.path):
            self.reached_end = True
            return

        target_x, target_y = self.path[self.target_index]
        x, y = self.rect.center

        # Snap to avoid overshoot (when speed > 1)
        if x < target_x:
            x = min(x + self.speed, target_x)
        elif x > target_x:
            x = max(x - self.speed, target_x)

        if y < target_y:
            y = min(y + self.speed, target_y)
        elif y > target_y:
            y = max(y - self.speed, target_y)

        self.rect.center = (x, y)

        if (x, y) == (target_x, target_y):
            self.target_index += 1
            if self.target_index >= len(self.path):
                self.reached_end = True


class Heatwave(Enemy):
    def __init__(self, path, image):
        super().__init__(path, image, speed=3, health=60, enemy_type="HEATWAVE")


class PlasticWave(Enemy):
    def __init__(self, path, image):
        super().__init__(path, image, speed=1, health=120, enemy_type="PLASTICWAVE")