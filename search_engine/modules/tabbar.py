import pygame as pyg
pyg.init()

from common.classes.display import Colors, Fonts
from common.classes.globals import Globals
from common.modules.collider import collides_point

def draw(window, offset):
    x, y = offset
    width, height = 50, Globals.HEIGHT

    pyg.draw.rect(window, Colors.dark_black, (x, y, width, height), border_radius=5)
    pyg.draw.rect(window, Colors.black, (x+2, y+2, width-4, height-4), border_radius=5)

    tab_height = height // 26
    tab_height -= 2

    vertical_offset = 2

    for i in range(26):
        extra_height = 1 if (i % 3 == 0) else 0
        rect_color = Colors.light_gray if collides_point(Globals.mouse_position, (x-1, vertical_offset-2, width, tab_height + extra_height)) else Colors.gray

        if i == 0:
            pyg.draw.rect(window, rect_color, (x+2, vertical_offset+1, width-4, tab_height), border_top_left_radius=5, border_top_right_radius=5)
        elif i == 25:
            pyg.draw.rect(window, rect_color, (x+2, vertical_offset, width-4, tab_height), border_bottom_left_radius=5, border_bottom_right_radius=5)
        else:
            pyg.draw.rect(window, rect_color, (x+2, vertical_offset, width-4, tab_height + extra_height))

        char = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"[i]
        text_width, text_height = Fonts.font_20.size(char)
        window.blit(Fonts.font_20.render(char, True, Colors.white), (x+2 + (width - text_width)/2, vertical_offset + (tab_height - text_height)/2))
        vertical_offset += tab_height + extra_height + 2