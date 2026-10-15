"""Minimal arcade window: static test grid and a time-based game loop."""
import arcade

TILE_SIZE = 32
GRID_COLUMNS = 30
GRID_ROWS = 20
WINDOW_WIDTH = GRID_COLUMNS * TILE_SIZE
WINDOW_HEIGHT = GRID_ROWS * TILE_SIZE
WINDOW_TITLE = "Pac-Man"

GRID_COLOR = (40, 40, 120)
MARKER_COLOR = arcade.color.YELLOW
MARKER_SPEED = 160.0


class GameWindow(arcade.Window):
    """Opens the window, draws the grid and runs the update loop."""

    def __init__(self) -> None:
        """Creates the window and resets the loop timers."""
        super().__init__(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE)
        arcade.set_background_color(arcade.color.BLACK)
        self.marker_x: float = 0.0

    def on_draw(self) -> None:
        """Draws one frame."""
        self.clear()
        self._draw_grid()
        self._draw_marker()

    def on_update(self, delta_time: float) -> None:
        """Advances the game by delta_time seconds."""
        self.marker_x = (
            self.marker_x + MARKER_SPEED * delta_time
        ) % WINDOW_WIDTH

    def on_key_press(self, symbol: int, modifiers: int) -> None:
        """Closes the window when ESC is pressed."""
        if symbol == arcade.key.ESCAPE:
            self.close()

    def _draw_grid(self) -> None:
        """Draws the static test grid."""
        for column in range(GRID_COLUMNS + 1):
            x = column * TILE_SIZE
            arcade.draw_line(x, 0, x, WINDOW_HEIGHT, GRID_COLOR)
        for row in range(GRID_ROWS + 1):
            y = row * TILE_SIZE
            arcade.draw_line(0, y, WINDOW_WIDTH, y, GRID_COLOR)

    def _draw_marker(self) -> None:
        """Draws a square that moves at a constant speed."""
        arcade.draw_lrbt_rectangle_filled(
            self.marker_x,
            self.marker_x + TILE_SIZE,
            WINDOW_HEIGHT // 2,
            WINDOW_HEIGHT // 2 + TILE_SIZE,
            MARKER_COLOR,
        )


def run_window() -> None:
    """Creates the window and starts the arcade loop."""
    GameWindow()
    arcade.run()
