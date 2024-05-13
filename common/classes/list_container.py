import contextlib
with contextlib.redirect_stdout(None):
    import pygame as pyg

from common.classes.display import Colors, ColorTheme, Fonts
from common.classes.globals import Globals
from common.modules.collider import collides_point

class ListContent:
    def __init__(self, title: str, date_dreamt: str, date_modified: str, data=""):
        self.title = title 
        self.date_dreamt = date_dreamt
        self.date_modified = date_modified
        self.rect = ()
        self.data = data

    def draw(self, window: pyg.Surface, rect, type: str, mouse_position: list):
        if self.rect != rect:
            self.rect = rect

        color = ColorTheme.current_theme.field_border_color if self.check_mcollision(mouse_position) else ColorTheme.current_theme.field_background_color
        if type == "Top":
            pyg.draw.rect(window, Colors.gray, rect, border_top_left_radius=8, border_top_right_radius=8)
            pyg.draw.rect(window, color, (rect[0] + 1, rect[1] + 1, rect[2] - 2, rect[3] - 2), border_top_left_radius=8, border_top_right_radius=8)
        else:
            pyg.draw.rect(window, Colors.gray, rect)
            pyg.draw.rect(window, color, (rect[0] + 1, rect[1] + 1, rect[2] - 2, rect[3] - 2))

        window.blit(Fonts.font_20.render(self.title, True, ColorTheme.current_theme.cursor_color), (rect[0] + 2, rect[1] + 2))
        char_height = Fonts.font_20.size("A")[1]
        window.blit(Fonts.font_18.render("Date of Dream: " + self.date_dreamt + " | Date Modified: " + self.date_modified, True, Colors.lighter_gray), (rect[0] + 2, rect[1] + char_height + 2))

    def check_mcollision(self, mouse_position: list=[0, 0]):
        m = mouse_position if mouse_position != [0, 0] else Globals.mouse_position
        if self.rect == ():
            return False
        return collides_point(m, self.rect)


class ListContainer:
    def __init__(self, rect: tuple, contents: list[ListContent]=[]):
        self.x, self.y, self.width, self.height = rect
        self.contents = contents

    def draw(self, window: pyg.Surface, mouse_position: list):
        content_width, content_height = self.width - 4, 40

        pyg.draw.rect(window, Colors.gray, (self.x, self.y, self.width, self.height), border_radius=8)
        pyg.draw.rect(window, ColorTheme.current_theme.background_color, (self.x + 2, self.y + 2, self.width - 4, self.height - 4), border_radius=8)

        # Draw contents of list
        for i in range(len(self.contents)):
            item = self.contents[i]
            rect = (self.x + 2, self.y + 2 + i * content_height, content_width, content_height)

            type = "Middle"
            if i == 0: type = "Top"

            item.draw(window, rect, type, mouse_position)

    def check_click(self, mouse_position: list):
        """Checks if one of the list content items were clicked"""
        for item in self.contents:
            if item.check_mcollision(mouse_position):
                return item