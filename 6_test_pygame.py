import pygame

pygame.init()

WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption("My first Game Loop")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (50, 100, 200)

executing = True
while executing:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            executing = False

    screen.fill(WHITE)
    pygame.draw.rect(
        screen,
        BLUE,
        (300, 200, 200, 150)
    )

    pygame.display.flip()

pygame.quit()
