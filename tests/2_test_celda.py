import pygame


class Cell:
    def __init__(self):
        self.up = True
        self.right = True
        self.down = True
        self.left = True

    def remove_wall(self, direction):
        if direction == "up":
            self.up = False
        elif direction == "right":
            self.right = False
        elif direction == "down":
            self.down = False
        elif direction == "left":
            self.left = False

    def draw(self, screen, x, y, size):
        if self.up:
            pygame.draw.line(screen, "white", (x, y), (x + size, y), 2)
        if self.right:
            pygame.draw.line(screen, "white", (x + size, y),
                             (x + size, y + size), 2)
        if self.down:
            pygame.draw.line(screen, "white", (x, y + size),
                             (x + size, y + size), 2)
        if self.left:
            pygame.draw.line(screen, "white", (x, y), (x, y + size), 2)


def test_new_cell_has_four_walls():
    cell = Cell()
    assert cell.up is True
    assert cell.right is True
    assert cell.down is True
    assert cell.left is True


def test_connect_cells():
    a = Cell()
    b = Cell()

    a.remove_wall("right")
    b.remove_wall("left")

    assert a.right is False
    assert b.left is False


def main() -> None:
    pygame.init()

    screen = pygame.display.set_mode((400, 400))
    clock = pygame.time.Clock()

    cell = Cell()
    cell.remove_wall("right")

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill("black")
        cell.draw(screen, 100, 100, 40)
        pygame.display.flip()
        clock.tick(60)


pygame.quit()


if __name__ == "__main__":
    main()
