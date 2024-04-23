import pygame as pyg
pyg.init()

from common.classes.display import Colors
from common.classes.globals import Globals
from common.modules.collider import collides_point

class Button:
    def __init__(self, rect, color, text, font, text_color):
        self.x, self.y, self.width, self.height = rect
        self.color = color
        self.text = text
        self.font = font
        self.text_color = text_color

    def draw(self, offset=0):
        back_color = [self.color[i] * 0.8 for i in range(len(self.color))]
        
        if not self.check_mcollision():
            pyg.draw.rect(Globals.VID_BUFFER, back_color, (self.x+2, self.y+2 + offset, self.width, self.height), border_radius=5)
        color = back_color if self.check_mcollision() else self.color
        pyg.draw.rect(Globals.VID_BUFFER, color, (self.x, self.y + offset, self.width, self.height), border_radius=5)

        text_width, text_height = self.font.size(self.text)
        Globals.VID_BUFFER.blit(self.font.render(self.text, True, self.text_color), (self.x + (self.width - text_width)/2, self.y + (self.height - text_height)/2 + offset))

    def check_mcollision(self):
        return collides_point(Globals.mouse_position, (self.x, self.y, self.width, self.height))
    
class Checkbox:
    def __init__(self, rect, text, font):
        self.x, self.y, self.width, self.height = rect
        self.text = text
        self.font = font
        self.active = False
    
    def draw(self, offset=0):
        color = Colors.green if self.active else Colors.gray
        pyg.draw.rect(Globals.VID_BUFFER, Colors.gray, (self.x-1, self.y-1 + offset, self.width+2, self.height+2), border_radius=2)
        pyg.draw.rect(Globals.VID_BUFFER, color, (self.x, self.y + offset, self.width, self.height), border_radius=2)

        text_width = self.font.size(self.text)[0]
        Globals.VID_BUFFER.blit(self.font.render(self.text, True, Colors.white), (self.x - text_width -6, self.y + offset))

    def check_mcollision(self):
        return collides_point(Globals.mouse_position, (self.x, self.y, self.width, self.height))

class Dropdown:
    def __init__(self, rect, font, color, options, text_color):
        self.x, self.y, self.width, self.height = rect
        self.color = color
        self.options = options
        self.font = font
        self.text_color = text_color
        self.active = False
        self.selected = options[0]

    def draw(self):
        if self.active:
            back_color = [self.color[i] * 0.8 for i in range(len(self.color))]
            highlight_color = [self.color[i] * 1.2 for i in range(len(self.color))]
            # Draw background
            pyg.draw.rect(Globals.VID_BUFFER, self.color, (self.x-2, self.y-2, self.width, self.height + (24 * len(self.options))), border_radius=5)
            # Draw currently selected option
            text_width, text_height = self.font.size(self.selected)
            vertical_offset = self.y + (self.height - text_height)/2
            Globals.VID_BUFFER.blit(self.font.render(self.selected, True, self.text_color), (self.x + (self.width - text_width - 20)/2, vertical_offset))
            vertical_offset += text_height + 2
            pyg.draw.rect(Globals.VID_BUFFER, back_color, (self.x, vertical_offset, self.width - 4, 2))
            vertical_offset += 4

            # Draw list of options
            for option in self.options:
                text_width, text_height = self.font.size(option)
                # Highlight hovered option
                if collides_point(Globals.mouse_position, (self.x, vertical_offset - 2, self.width - 8, text_height + 4)):
                    pyg.draw.rect(Globals.VID_BUFFER, highlight_color, (self.x, vertical_offset - 2, self.width - 8, text_height + 4), border_radius=5)
                    
                Globals.VID_BUFFER.blit(self.font.render(option, True, self.text_color), (self.x + (self.width - text_width - 20)/2, vertical_offset))
                vertical_offset += text_height + 2


        else:
            color = self.color
            if self.check_mcollision():
                color = [self.color[i] * 1.2 for i in range(len(self.color))]
            pyg.draw.rect(Globals.VID_BUFFER, color, (self.x-2, self.y-2, self.width, self.height), border_radius=5)
            text_width, text_height = self.font.size(self.selected)
            Globals.VID_BUFFER.blit(self.font.render(self.selected, True, self.text_color), (self.x + (self.width - text_width - 20)/2, self.y + (self.height - text_height)/2))

            # Draw down arrow
            pyg.draw.line(Globals.VID_BUFFER, self.text_color, (self.x + self.width - 20, self.y + 8), (self.x + self.width - 15, self.y + self.height - 12), 1)
            pyg.draw.line(Globals.VID_BUFFER, self.text_color, (self.x + self.width - 15, self.y + self.height - 12), (self.x + self.width - 10, self.y + 8), 1)

    
    def check_mcollision(self):
        return collides_point(Globals.mouse_position, (self.x, self.y, self.width, self.height))
    
    def click(self):
        if not self.active and self.check_mcollision():
            self.active = True
        else:
            self.active = False
            if self.check_mcollision():
                return

            # Calculate starting position
            text_height = self.font.size(self.selected)[1]
            vertical_offset = self.y + (self.height - text_height)/2 + text_height + 6
            # Check if a given option was selected
            for option in self.options:
                text_height = self.font.size(option)[1]
                # Highlight hovered option
                if collides_point(Globals.mouse_position, (self.x, vertical_offset - 2, self.width - 8, text_height + 4)):
                    self.selected = option
                    return option
                vertical_offset += text_height + 2