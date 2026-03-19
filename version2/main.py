import pygame

WIDTH, HEIGHT = 800, 600
FPS = 60
BACKGROUND_COLOR = (20, 200, 30)
PATH_COLOR = (240, 230, 180)
PATH_WIDTH = 8

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sustainable Tower Defense - Version 2")

clock = pygame.time.Clock()
running = True

# Waypoint path (enemies move along these points)
path = [(50, 300), (250, 300), (250, 150), (550, 150), (550, 450), (750, 450)]

class Enemy(pygame.sprite.Sprite):
    def __init__(self, path, w, h, color=(200, 50, 50), speed=2):
        super().__init__()
        self.image = pygame.Surface((w, h))
        self.image.fill(color)
        self.rect = self.image.get_rect(center=path[0])

        self.path = path
        self.target_index = 1
        self.speed = speed

    def update(self):
        if self.target_index >= len(self.path):
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

# Enemy group with two enemies (different size, color, speed)
enemies = pygame.sprite.Group()
enemies.add(
    Enemy(path, w=40, h=30, color=(200, 50, 50), speed=3),   # faster, small red
    Enemy(path, w=60, h=40, color=(30, 30, 200), speed=1)    # slower, bigger blue
)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(BACKGROUND_COLOR)

    # Draw the path
    pygame.draw.lines(screen, PATH_COLOR, False, path, PATH_WIDTH)

    enemies.update()
    enemies.draw(screen)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
