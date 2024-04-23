import pygame as pyg
pyg.init()

from common.classes.display import Colors, Fonts
from common.classes.globals import Globals

from common.modules.collider import collides_point

class Tab:
    def __init__(self, rect, text):
        self.x, self.y, self.width, self.height = rect
        self.text = text
        self.active = False

    def draw(self, window):
        pyg.draw.rect(window, Colors.black, (self.x, self.y, self.width, self.height), border_top_left_radius=8, border_top_right_radius=8)
        color = Colors.light_gray if self.check_mcollision() else Colors.gray
        color = Colors.lighter_gray if self.active else color

        pyg.draw.rect(window, color, (self.x+2, self.y+2, self.width-4, self.height-2), border_top_left_radius=8, border_top_right_radius=8)

        text_width, text_height = Fonts.font_18.size(self.text)
        window.blit(Fonts.font_18.render(self.text, True, Colors.white), (self.x + (self.width - text_width)/2, self.y + 2 + (self.height - text_height)/2))

    def check_mcollision(self):
        return collides_point(Globals.mouse_position, (self.x, self.y, self.width, self.height))

def draw(window, offset):
    x, y = offset
    width, height = Globals.WIDTH-x, Globals.HEIGHT

    pyg.draw.rect(window, Colors.dark_black, (x, y, width, height), border_radius=8)
    pyg.draw.rect(window, Colors.black, (x+2, y+2, width-4, height-4), border_radius=8)

    pyg.draw.rect(window, Colors.dark_black, (x, y + 30, width, 4))

    