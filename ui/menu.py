"""Main menu screen: static title and the four selectable options."""
import arcade

TITLE_SIZE = 50
SUBTITLE_SIZE = 18
OPTION_SIZE = 24
HINT_SIZE = 14

TITLE_COLOR = arcade.color.YELLOW
TEXT_COLOR = arcade.color.WHITE
SELECTED_COLOR = arcade.color.YELLOW
HINT_COLOR = arcade.color.GRAY

OPTIONS = ("Start Game", "View Highscores", "Instructions", "Exit")


class MainMenu:
    """Holds the menu options, the selected one, and draws the screen."""

    def __init__(self, width: int, height: int) -> None:
        """Builds the texts once for a window of width x height."""
        self.options: tuple[str, ...] = OPTIONS
        self.selected: int = 0
        center_x = width // 2
        self._title = self._text("PAC-MAN", center_x, height - 120,
                                 TITLE_COLOR, TITLE_SIZE)
        self._subtitle = self._text("MAIN MENU", center_x, height - 170,
                                    TEXT_COLOR, SUBTITLE_SIZE)
        self._hint = self._text("UP / DOWN -> Move    ENTER -> Select",
                                center_x, 40, HINT_COLOR, HINT_SIZE)
        self._option_texts = [
            self._text(option, center_x, height - 260 - 60 * index,
                       TEXT_COLOR, OPTION_SIZE)
            for index, option in enumerate(self.options)
        ]

    @staticmethod
    def _text(content: str, x: int, y: int,
              color: tuple[int, int, int, int] | tuple[int, int, int],
              size: int) -> arcade.Text:
        """Creates a centered text object (cheaper than draw_text)."""
        return arcade.Text(content, x, y, color, size, anchor_x="center")

    def draw(self) -> None:
        """Draws the menu, highlighting the selected option."""
        self._title.draw()
        self._subtitle.draw()
        for index, text in enumerate(self._option_texts):
            text.color = (SELECTED_COLOR if index == self.selected
                          else TEXT_COLOR)
            text.draw()
        self._hint.draw()

    def move_up(self) -> None:
        """Selects the previous option, wrapping to the last one."""
        self.selected = (self.selected - 1) % len(self.options)

    def move_down(self) -> None:
        """Selects the next option, wrapping to the first one."""
        self.selected = (self.selected + 1) % len(self.options)

    def get_selected(self) -> str:
        """Returns the text of the selected option."""
        return self.options[self.selected]
