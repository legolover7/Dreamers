import pygame as pyg
pyg.init()

from common.classes.display import Colors, Fonts
from common.classes.globals import Globals
import common.modules.collider as collider
import common.modules.chunk_text as chunk_text

class Button:
    def __init__(self, rect, color, text, font, text_color):
        self.x, self.y, self.width, self.height = rect
        self.color = color
        self.text = text
        self.font = font
        self.text_color = text_color

    def draw(self, window, offset=0):
        back_color = [self.color[i] * 0.8 for i in range(len(self.color))]
        
        if not self.check_mcollision():
            pyg.draw.rect(window, back_color, (self.x+2, self.y+2 + offset, self.width, self.height), border_radius=5)
        color = back_color if self.check_mcollision() else self.color
        pyg.draw.rect(window, color, (self.x, self.y + offset, self.width, self.height), border_radius=5)

        text_width, text_height = self.font.size(self.text)
        window.blit(self.font.render(self.text, True, self.text_color), (self.x + (self.width - text_width)/2, self.y + (self.height - text_height)/2 + offset))

    def check_mcollision(self):
        return collider.collides_point(Globals.mouse_position, (self.x, self.y, self.width, self.height))
    
class ToolTip:
    def __init__(self, text: str, delay: int, max_width: int=0):
        self.text = text
        self.max_width = max_width
        if self.max_width == 0:
            self.max_width = Fonts.font_18.size(self.text)[0]

        self.max_width = min(self.max_width, Fonts.font_18.size(self.text)[0] + 10)

        self.displayed = False
        self.min_delay = delay
        self.current_delay = 0

    def draw(self, window: pyg.Surface, position: tuple):
        x, y = position

        text_lines = chunk_text.chunk(self.text, content_width=self.max_width, char_width=Fonts.font_18.size("A")[0])
        text_width, text_height = 0, Fonts.font_18.size("A")[1]
        for line in text_lines:
            line_width = Fonts.font_18.size(line)[0]
            if line_width > text_width:
                text_width = line_width
        
        pyg.draw.rect(window, Colors.dark_gray, (x, y, text_width + 6, (text_height + 2) * len(text_lines) + 4), border_radius=4)
        pyg.draw.rect(window, Colors.black, (x + 1, y + 1, text_width + 4, (text_height + 2) * len(text_lines) + 2), border_radius=4)

        for i in range(len(text_lines)):
            window.blit(Fonts.font_18.render(text_lines[i], True, Colors.white), (x + 3, y + 3 + (text_height + 2) * i))


class Checkbox:
    def __init__(self, rect, text, font, value="", default_active=False, left_align=False, tooltip: ToolTip=None):
        self.x, self.y, self.width, self.height = rect
        self.text = text
        self.font = font
        self.active = default_active
        self.left_align = left_align
        self.value = value
        self.tooltip = tooltip
    
    def draw(self, window, offset=0):
        color = Colors.green if self.active else Colors.gray

        text_width = self.font.size(self.text)[0]
        content_width = text_width + self.width

        if self.left_align:
            window.blit(self.font.render(self.text, True, Colors.white), (self.x, self.y + offset))

            pyg.draw.rect(window, Colors.gray, (self.x + text_width + 9, self.y - 1 + offset, self.width+2, self.height+2), border_radius=2)
            pyg.draw.rect(window, color, (self.x + text_width + 10, self.y + offset, self.width, self.height), border_radius=2)
        else:
            pyg.draw.rect(window, Colors.gray, (self.x-1, self.y-1 + offset, self.width+2, self.height+2), border_radius=2)
            pyg.draw.rect(window, color, (self.x, self.y + offset, self.width, self.height), border_radius=2)

            window.blit(self.font.render(self.text, True, Colors.white), (self.x - text_width -6, self.y + offset))

        # Show tooltip on hover
        if self.tooltip != None:
            if not collider.collides_point(Globals.mouse_position, (self.x, self.y, content_width + 10, self.height)):
                self.tooltip.current_delay = 0
            else:
                self.tooltip.current_delay = min(self.tooltip.min_delay, self.tooltip.current_delay + 1)

    def check_mcollision(self, offset=0):
        if self.left_align:
            text_width = self.font.size(self.text)[0]
            return collider.collides_point(Globals.mouse_position, (self.x + text_width + 10, self.y + offset, self.width, self.height))

        else:
            return collider.collides_point(Globals.mouse_position, (self.x, self.y + offset, self.width, self.height))

class Dropdown:
    def __init__(self, rect, font, color, options, text_color):
        self.x, self.y, self.width, self.height = rect
        self.color = color
        self.options = options
        self.font = font
        self.text_color = text_color
        self.active = False
        self.selected = options[0]

    def draw(self, window):
        if self.active:
            back_color = [self.color[i] * 0.8 for i in range(len(self.color))]
            highlight_color = [self.color[i] * 1.2 for i in range(len(self.color))]
            # Draw background
            pyg.draw.rect(window, self.color, (self.x-2, self.y-2, self.width, self.height + (24 * len(self.options))), border_radius=5)
            # Draw currently selected option
            text_width, text_height = self.font.size(self.selected)
            vertical_offset = self.y + (self.height - text_height)/2
            window.blit(self.font.render(self.selected, True, self.text_color), (self.x + (self.width - text_width - 20)/2, vertical_offset))
            vertical_offset += text_height + 2
            pyg.draw.rect(window, back_color, (self.x, vertical_offset, self.width - 4, 2))
            vertical_offset += 4

            # Draw list of options
            for option in self.options:
                text_width, text_height = self.font.size(option)
                # Highlight hovered option
                if collider.collides_point(Globals.mouse_position, (self.x, vertical_offset - 2, self.width - 8, text_height + 4)):
                    pyg.draw.rect(window, highlight_color, (self.x, vertical_offset - 2, self.width - 8, text_height + 4), border_radius=5)
                    
                window.blit(self.font.render(option, True, self.text_color), (self.x + (self.width - text_width - 20)/2, vertical_offset))
                vertical_offset += text_height + 2

        else:
            color = self.color
            if self.check_mcollision():
                color = [self.color[i] * 1.2 for i in range(len(self.color))]
            pyg.draw.rect(window, color, (self.x-2, self.y-2, self.width, self.height), border_radius=5)
            text_width, text_height = self.font.size(self.selected)
            window.blit(self.font.render(self.selected, True, self.text_color), (self.x + (self.width - text_width - 20)/2, self.y + (self.height - text_height)/2))

            # Draw down arrow
            pyg.draw.line(window, self.text_color, (self.x + self.width - 20, self.y + 8), (self.x + self.width - 15, self.y + self.height - 12), 1)
            pyg.draw.line(window, self.text_color, (self.x + self.width - 15, self.y + self.height - 12), (self.x + self.width - 10, self.y + 8), 1)

    
    def check_mcollision(self):
        return collider.collides_point(Globals.mouse_position, (self.x, self.y, self.width, self.height))
    
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
                if collider.collides_point(Globals.mouse_position, (self.x, vertical_offset - 2, self.width - 8, text_height + 4)):
                    self.selected = option
                    return option
                vertical_offset += text_height + 2