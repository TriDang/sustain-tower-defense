import pygame

WIDTH, HEIGHT = 800, 600
FPS = 60
BACKGROUND_COLOR = (20, 200, 30)

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sustainable Tower Defense - Version 1")

clock = pygame.time.Clock()
running = True

# Sprite as simple box
class Box(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h, color=(0, 0, 0)):
        super().__init__()
        self.image = pygame.Surface((w, h))
        self.image.fill(color)
        self.rect = self.image.get_rect(topleft=(x, y))


# One group with two sprites
boxes = pygame.sprite.Group()
boxes.add(
    Box(150, 200, 60, 40),
    Box(300, 260, 60, 40, color=(200, 0, 0))
)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(BACKGROUND_COLOR)

    # Draw all sprites in the group
    boxes.draw(screen)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
