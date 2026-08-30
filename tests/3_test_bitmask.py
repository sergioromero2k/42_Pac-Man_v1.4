import pygame

# cell = UP | RIGHT | DOWN | LEFT
# print(cell)
# print(bin(cell))

# cell = 15
# cell &= ~RIGHT

# print(cell)
# print(bin(cell))


# def test_cell_starts_with_four_walls():
#     cell = UP | RIGHT | DOWN | LEFT
#     assert cell == 15


# def test_cell_has_right_wall():
#     cell = UP | RIGHT | DOWN | LEFT
#     assert cell & RIGHT


# def test_remove_right_wall():
#     cell = UP | RIGHT | DOWN | LEFT
#     cell &= ~RIGHT
#     assert not (cell & RIGHT)

UP = 1      # 0001
RIGHT = 2   # 0010
DOWN = 4    # 0100
LEFT = 8    # 1000

WIDTH = 600
HEIGHT = 400
CELL_SIZE = 40


def draw_cell(screen, cell, x, y):
    if cell & UP:
        pygame.draw.line(
            screen,
            "white",
            (x, y),
            (x + CELL_SIZE, y),
            3
        )

    if cell & RIGHT:
        pygame.draw.line(
            screen,
            "white",
            (x + CELL_SIZE, y),
            (x + CELL_SIZE, y + CELL_SIZE),
            3
        )

    if cell & DOWN:
        pygame.draw.line(
            screen,
            "white",
            (x, y + CELL_SIZE),
            (x + CELL_SIZE, y + CELL_SIZE),
            3
        )

    if cell & LEFT:
        pygame.draw.line(
            screen,
            "white",
            (x, y),
            (x, y + CELL_SIZE),
            3
        )


def main():
    pygame.init()

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Bitmask")

    clock = pygame.time.Clock()

    cell = UP | RIGHT | DOWN | LEFT

    # Quitamos la pared derecha
    cell &= ~RIGHT

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill("black")

        draw_cell(screen, cell, 100, 100)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()