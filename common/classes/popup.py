import pygame as pyg

from common.classes.buttons import Button
from common.classes.display import Colors, Fonts
from common.classes.globals import Globals
import common.modules.chunk_text as chunk_text
import common.modules.collider as collider

class Popup:
    def __init__(self, rect: tuple, text: str, text_margin: int=0):
        self.x, self.y, self.width, self.height = rect
        self.text = text
        self.text_margin = text_margin
        self.displayed = False

        self.cancel_button = Button((self.x + 20, self.y + self.height - 60, 120, 40), Colors.red, "Cancel", Fonts.font_20, Colors.white)
        self.confirm_button = Button((self.x + self.width - 140, self.y + self.height - 60, 120, 40), Colors.green, "Confirm", Fonts.font_20, Colors.white)

    def draw(self, window: pyg.Surface):
        pyg.draw.rect(window, Colors.gray, (self.x, self.y, self.width, self.height), border_radius=8)
        pyg.draw.rect(window, Colors.black, (self.x + 2, self.y + 2, self.width - 4, self.height - 4), border_radius=8)

        text = chunk_text.chunk(self.text, content_width=self.width-(self.text_margin*2), char_width=Fonts.font_20.size("A")[0])
        vertical_position = self.y + 10
        for line in text:
            text_width, text_height = Fonts.font_20.size(line)
            window.blit(Fonts.font_20.render(line, True, Colors.white), (self.x + (self.width - text_width)/2, vertical_position))
            vertical_position += text_height + 2

        self.cancel_button.draw(window)
        self.confirm_button.draw(window)

    def check_mcollision(self):
        return collider.collides_point(Globals.mouse_position, (self.x, self.y, self.width, self.height))