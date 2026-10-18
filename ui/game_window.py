"""Arcade window that shows the main menu."""
import arcade

from ui.menu import MainMenu

WINDOW_WIDTH = 960
WINDOW_HEIGHT = 640
WINDOW_TITLE = "Pac-Man"


class GameWindow(arcade.Window):
    """Opens the window and forwards drawing and keys to the menu."""

    def __init__(self) -> None:
        """Creates the window and the menu."""
        super().__init__(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE)
        arcade.set_background_color(arcade.color.BLACK)
        self.menu = MainMenu(self.width, self.height)

    def on_draw(self) -> None:
        """Draws one frame."""
        self.clear()
        self.menu.draw()

    def on_key_press(self, symbol: int, modifiers: int) -> None:
        """UP/DOWN move the selection, ENTER selects, ESC closes."""
        if symbol == arcade.key.UP:
            self.menu.move_up()
        elif symbol == arcade.key.DOWN:
            self.menu.move_down()
        elif symbol == arcade.key.ENTER:
            self._activate(self.menu.get_selected())
        elif symbol == arcade.key.ESCAPE:
            self.close()

    def _activate(self, option: str) -> None:
        """Runs the chosen option (only Exit does something for now)."""
        if option == "Exit":
            self.close()
        else:
            print(f"Selected: {option}")


def run_window() -> None:
    """Creates the window and starts the arcade loop."""
    GameWindow()
    arcade.run()
