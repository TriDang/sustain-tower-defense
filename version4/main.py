import pygame
import os

from enemy import Heatwave, PlasticWave
from tower import SolarPanel, RecyclingPlant, MangroveForest

WIDTH, HEIGHT = 800, 600
FPS = 60
BACKGROUND_COLOR = (20, 200, 30)

PATH_COLOR = (240, 230, 180)
PATH_WIDTH = 8

SHOT_COLOR = (255, 255, 0)
SHOT_WIDTH = 3
SHOT_DURATION_MS = 100

HEALTH_BAR_WIDTH = 50
HEALTH_BAR_HEIGHT = 6
HEALTH_BAR_COLOR = (220, 0, 0)
HEALTH_BAR_BG = (60, 60, 60)
HEALTH_BAR_OFFSET_Y = 10

STATE_TEXT_COLOR = (0, 0, 0)

pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sustainable Tower Defense - Version 4")
clock = pygame.time.Clock()

health_font = pygame.font.SysFont(None, 22)
state_font = pygame.font.SysFont(None, 72)

running = True
state = "RUNNING"   # RUNNING / WIN / LOSE
end_sound_played = False

path = [(50, 300), (250, 300), (250, 150), (550, 150), (550, 450), (750, 450)]
TARGET_POS = path[-1]

# ---- Load images ----
HEATWAVE_IMG = pygame.image.load(os.path.join("version4", "assets", "heatwave.png")).convert_alpha()
PLASTICWAVE_IMG = pygame.image.load(os.path.join("version4", "assets", "plastic_wave.png")).convert_alpha()

SOLAR_IMG = pygame.image.load(os.path.join("version4", "assets", "solar_panel.png")).convert_alpha()
RECYCLE_IMG = pygame.image.load(os.path.join("version4", "assets", "recycling_plant.png")).convert_alpha()
MANGROVE_IMG = pygame.image.load(os.path.join("version4", "assets", "mangrove_forest.png")).convert_alpha()

EARTH_IMG = pygame.image.load(os.path.join("version4", "assets", "earth.png")).convert_alpha()

# ---- Load sounds ----
sfx_attack = pygame.mixer.Sound(os.path.join("version4", "assets", "sfx_attack.wav"))
sfx_destroy = pygame.mixer.Sound(os.path.join("version4", "assets", "sfx_destroy.wav"))
sfx_win = pygame.mixer.Sound(os.path.join("version4", "assets", "sfx_win.wav"))
sfx_lose = pygame.mixer.Sound(os.path.join("version4", "assets", "sfx_lose.wav"))

# ---- Groups ----
enemies = pygame.sprite.Group()
towers = pygame.sprite.Group()

towers.add(
    SolarPanel(190, 200, SOLAR_IMG),
    RecyclingPlant(610, 210, RECYCLE_IMG),
    MangroveForest(490, 400, MANGROVE_IMG),
)

shots = []  # (start_pos, end_pos, expire_time_ms)

# ---- Spawn schedule ----
# Each item: (spawn_time_ms, enemy_type)
spawn_schedule = [
    (0, "HEATWAVE"),
    (1200, "PLASTICWAVE"),
    (2400, "HEATWAVE"),
    (3600, "PLASTICWAVE"),
]

spawn_index = 0
start_time = pygame.time.get_ticks()

def spawn_enemy(enemy_type):
    if enemy_type == "HEATWAVE":
        enemies.add(Heatwave(path, HEATWAVE_IMG))
    elif enemy_type == "PLASTICWAVE":
        enemies.add(PlasticWave(path, PLASTICWAVE_IMG))


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    now = pygame.time.get_ticks()
    elapsed = now - start_time

    if state == "RUNNING":
        # ---- Spawn enemies by schedule ----
        while spawn_index < len(spawn_schedule) and elapsed >= spawn_schedule[spawn_index][0]:
            _, enemy_type = spawn_schedule[spawn_index]
            spawn_enemy(enemy_type)
            spawn_index += 1

        # ---- Update enemies ----
        enemies.update()

        # ---- LOSE if any enemy reaches Earth ----
        for enemy in enemies:
            if enemy.reached_end:
                state = "LOSE"
                break

        # ---- Towers attack ----
        if state == "RUNNING":
            for tower in towers:
                if now - tower.last_attack_time < tower.cooldown_ms:
                    continue

                for enemy in list(enemies):
                    dx = enemy.rect.centerx - tower.rect.centerx
                    dy = enemy.rect.centery - tower.rect.centery
                    distance = (dx * dx + dy * dy) ** 0.5

                    if distance <= tower.range:
                        shots.append((tower.rect.center, enemy.rect.center, now + SHOT_DURATION_MS))
                        sfx_attack.play()

                        enemy.health -= tower.damage
                        tower.last_attack_time = now

                        if enemy.health <= 0:
                            enemies.remove(enemy)
                            sfx_destroy.play()

                        break  # one attack per cooldown

            # ---- WIN if all scheduled enemies have spawned and all are destroyed ----
            if spawn_index == len(spawn_schedule) and len(enemies) == 0:
                state = "WIN"

    # ---- End sound once ----
    if state == "WIN" and not end_sound_played:
        sfx_win.play()
        end_sound_played = True

    if state == "LOSE" and not end_sound_played:
        sfx_lose.play()
        end_sound_played = True

    # ---- Draw ----
    screen.fill(BACKGROUND_COLOR)

    pygame.draw.lines(screen, PATH_COLOR, False, path, PATH_WIDTH)

    earth_rect = EARTH_IMG.get_rect(center=TARGET_POS)
    screen.blit(EARTH_IMG, earth_rect)

    towers.draw(screen)
    enemies.draw(screen)

    # Draw shots
    shots = [s for s in shots if s[2] > now]
    for start_pos, end_pos, _expire in shots:
        pygame.draw.line(screen, SHOT_COLOR, start_pos, end_pos, SHOT_WIDTH)

    # Draw enemy health
    for enemy in enemies:
        health_percentage = max(0, enemy.health) / enemy.max_health
        # health bar position above enemy
        bar_x = enemy.rect.centerx - HEALTH_BAR_WIDTH // 2
        bar_y = enemy.rect.top - HEALTH_BAR_OFFSET_Y

        # background bar (optional but clearer)
        pygame.draw.rect(
            screen,
            HEALTH_BAR_BG,
            (bar_x, bar_y, HEALTH_BAR_WIDTH, HEALTH_BAR_HEIGHT),
        )

        # filled health bar (red)
        pygame.draw.rect(
            screen,
            HEALTH_BAR_COLOR,
            (bar_x, bar_y, int(HEALTH_BAR_WIDTH * health_percentage), HEALTH_BAR_HEIGHT),
        )

    # Draw WIN / LOSE
    if state in ("WIN", "LOSE"):
        msg = state_font.render(state, True, STATE_TEXT_COLOR)
        msg_rect = msg.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(msg, msg_rect)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()