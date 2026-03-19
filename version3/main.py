import pygame

WIDTH, HEIGHT = 800, 600
FPS = 60
BACKGROUND_COLOR = (20, 200, 30)

PATH_COLOR = (240, 230, 180)
PATH_WIDTH = 8

# Tower settings
TOWER_RANGE = 150
TOWER_DAMAGE = 5
ATTACK_COOLDOWN_MS = 500

# Bullet settings
SHOT_COLOR = (255, 255, 0)
SHOT_WIDTH = 3
SHOT_DURATION_MS = 100  # how long the shot line stays visible

# Health text settings
HEALTH_TEXT_COLOR = (255, 255, 255)

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sustainable Tower Defense - Version 3")

clock = pygame.time.Clock()
running = True

# Font for enemy health (basic system font)
health_font = pygame.font.SysFont("Arial, Helvetica", 22)

# Waypoint path (enemies move along these points)
path = [(50, 300), (250, 300), (250, 150), (550, 150), (550, 450), (750, 450)]

# Tower image
SOLAR_IMG = pygame.image.load("version3/assets/solar_panel.png").convert_alpha()

class Enemy(pygame.sprite.Sprite):
    def __init__(self, path, w, h, color=(200, 50, 50), speed=2, health=60):
        super().__init__()
        self.image = pygame.Surface((w, h))
        self.image.fill(color)
        self.rect = self.image.get_rect(center=path[0])

        self.path = path
        self.target_index = 1
        self.speed = speed
        self.health = health

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


class Tower(pygame.sprite.Sprite):
    def __init__(self, x, y, image, damage=TOWER_DAMAGE, range=TOWER_RANGE):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(center=(x, y))

        self.damage = damage
        self.range = range
        self.last_attack_time = 0

# Enemy group with two enemies (different size, color, speed)
enemies = pygame.sprite.Group()
enemies.add(
    Enemy(path, w=40, h=30, color=(200, 50, 50), speed=3, health=50),   # faster, small red
    Enemy(path, w=60, h=40, color=(30, 30, 200), speed=1, health=100)   # slower, bigger blue
)

# Two towers placed near the path border
towers = pygame.sprite.Group()
towers.add(
    Tower(180, 230, SOLAR_IMG),
    Tower(620, 400, SOLAR_IMG)
)

# Active shots: (start_pos, end_pos, expire_time_ms)
shots = []

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    now = pygame.time.get_ticks()

    screen.fill(BACKGROUND_COLOR)

    # Draw the path
    pygame.draw.lines(screen, PATH_COLOR, False, path, PATH_WIDTH)

    # Update enemies
    enemies.update()

    # Tower attack logic (range check + cooldown)
    for tower in towers:
        if now - tower.last_attack_time < ATTACK_COOLDOWN_MS:
            continue

        for enemy in list(enemies):
            dx = enemy.rect.centerx - tower.rect.centerx
            dy = enemy.rect.centery - tower.rect.centery
            distance = (dx * dx + dy * dy) ** 0.5

            if distance <= tower.range:
                # Add a short-lived shot line (tower -> enemy)
                shots.append((tower.rect.center, enemy.rect.center, now + SHOT_DURATION_MS))

                enemy.health -= tower.damage
                tower.last_attack_time = now

                if enemy.health <= 0:
                    enemies.remove(enemy)
                break  # one attack per cooldown

    # Draw towers and enemies
    towers.draw(screen)
    enemies.draw(screen)

    # Draw shots and remove expired ones
    shots = [s for s in shots if s[2] > now]
    for start_pos, end_pos, _expire in shots:
        pygame.draw.line(screen, SHOT_COLOR, start_pos, end_pos, SHOT_WIDTH)

    # Draw enemy health text on top of each enemy box
    for enemy in enemies:
        text = health_font.render(str(enemy.health), True, HEALTH_TEXT_COLOR)
        text_rect = text.get_rect(center=enemy.rect.center)
        screen.blit(text, text_rect)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()