import contextlib
with contextlib.redirect_stdout(None):
    import pygame as pyg

from common.classes.buttons import Button
from common.classes.display import Colors, Fonts
import common.modules.chunk_text as chunk_text
import common.modules.collider as collider

class Popup:
    def __init__(self, rect: tuple, text: str, text_margin: int=0):
        self.x, self.y, self.width, self.height = rect
        self.text = text
        self.text_margin = text_margin
        self.displayed = False
        self._display_surface = pyg.Surface((self.width, self.height))

        self.cancel_button = Button((20, self.height - 60, 120, 40), Colors.red, "Cancel", Fonts.font_20, Colors.white)
        self.confirm_button = Button((self.width - 140, self.height - 60, 120, 40), Colors.green, "Confirm", Fonts.font_20, Colors.white)

    def draw(self, window: pyg.Surface, mouse_position: list):
        # Draw background
        self._display_surface.fill(Colors.gray)
        pyg.draw.rect(self._display_surface, Colors.gray, (0, 0, self.width, self.height), border_radius=8)
        pyg.draw.rect(self._display_surface, Colors.black, (2, 2, self.width - 4, self.height - 4), border_radius=8)

        mouse_position[0] -= self.x
        mouse_position[1] -= self.y - 30

        # Draw text
        text = chunk_text.chunk(self.text, content_width=self.width-(self.text_margin*2), char_width=Fonts.font_20.size("A")[0])
        vertical_position = 10
        for line in text:
            text_width, text_height = Fonts.font_20.size(line)
            self._display_surface.blit(Fonts.font_20.render(line, True, Colors.white), ((self.width - text_width)/2, vertical_position))
            vertical_position += text_height + 2

        self.cancel_button.draw(self._display_surface, mouse_position)
        self.confirm_button.draw(self._display_surface, mouse_position)

        window.blit(self._display_surface, (self.x, self.y))

    def check_mcollision(self, mouse_position):
        return collider.collides_point(mouse_position, (self.x, self.y, self.width, self.height))

    def click(self, mouse_position):
        mouse_position[0] -= self.x
        mouse_position[1] -= self.y
        print(mouse_position, (self.cancel_button.x, self.cancel_button.y))

        if self.cancel_button.check_mcollision(mouse_position):
            return "Cancel"
        if self.confirm_button.check_mcollision(mouse_position):
            return "Confirm"