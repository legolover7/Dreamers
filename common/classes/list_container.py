import pygame as pyg

from common.classes.display import Colors, Fonts
from common.classes.globals import Globals
from common.modules.collider import collides_point

class ListContent:
    def __init__(self, title: str, date_dreamed: str, date_entered: str, data=""):
        self.title = title 
        self.date_dreamed = date_dreamed
        self.date_entered = date_entered
        self.rect = ()
        self.data = data

    def draw(self, window, rect, type):
        if self.rect == ():
            self.rect = rect

        color = Colors.gray if self.check_mcollision() else Colors.dark_gray
        if type == "Top":
            pyg.draw.rect(window, Colors.gray, rect, border_top_left_radius=8, border_top_right_radius=8)
            pyg.draw.rect(window, color, (rect[0] + 1, rect[1] + 1, rect[2] - 2, rect[3] - 2), border_top_left_radius=8, border_top_right_radius=8)
        else:
            pyg.draw.rect(window, Colors.gray, rect)
            pyg.draw.rect(window, color, (rect[0] + 1, rect[1] + 1, rect[2] - 2, rect[3] - 2))

        window.blit(Fonts.font_20.render(self.title, True, Colors.white), (rect[0] + 2, rect[1] + 2))
        char_height = Fonts.font_20.size("A")[1]
        window.blit(Fonts.font_18.render("Date of Dream: " + self.date_dreamed + " | Date Modified: " + self.date_entered, True, Colors.lighter_gray), (rect[0] + 2, rect[1] + char_height + 2))

    def check_mcollision(self):
        if self.rect == ():
            return False
        return collides_point(Globals.mouse_position, self.rect)


class ListContainer:
    def __init__(self, rect: tuple, contents: list[ListContent] = []):
        self.x, self.y, self.width, self.height = rect
        self.contents = contents

    def draw(self, window):
        content_width, content_height = self.width - 4, 40

        pyg.draw.rect(window, Colors.gray, (self.x, self.y, self.width, self.height), border_radius=8)
        pyg.draw.rect(window, Colors.black, (self.x + 2, self.y + 2, self.width - 4, self.height - 4), border_radius=8)

        # Draw contents of list
        for i in range(len(self.contents)):
            item = self.contents[i]
            rect = (self.x + 2, self.y + 2 + i * content_height, content_width, content_height)

            type = "Middle"
            if i == 0: type = "Top"

            item.draw(window, rect, type)


    def check_click(self):
        for item in self.contents:
            if item.check_mcollision():
                return item