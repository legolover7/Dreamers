import contextlib
with contextlib.redirect_stdout(None):
    import pygame as pyg
import datetime
import copy
import json
import time
import os

from common.classes.buttons import *
from common.classes.input_field import *
from common.classes.display import Colors, Fonts
from common.classes.globals import Globals, FilePaths
from common.classes.list_container import *

from common.modules.collider import collides_point
import common.modules.chunk_text as chunk_text

class Tab:
    def __init__(self, rect, text):
        self.x, self.y, self.width, self.height = rect
        self.text = text
        self.active = False

    def draw(self, window: pyg.Surface, mouse_position: list):
        """Draws the tabs corresponding to its parent tab view"""
        pyg.draw.rect(window, Colors.black, (self.x, self.y, self.width, self.height), border_top_left_radius=8, border_top_right_radius=8)
        
        color = ColorTheme.current_theme.field_background_color
        if self.active:
            color = ColorTheme.current_theme.selected_tab_color
        elif self.check_mcollision(mouse_position):
            color = ColorTheme.current_theme.field_border_color

        pyg.draw.rect(window, color, (self.x+2, self.y+2, self.width-4, self.height-2), border_top_left_radius=8, border_top_right_radius=8)

        text_width, text_height = Fonts.font_18.size(self.text)
        window.blit(Fonts.font_18.render(self.text, True, Colors.white), (self.x + (self.width - text_width)/2, self.y + 2 + (self.height - text_height)/2))

    def check_mcollision(self, position):
        """Returns true if the mouse cursor is colliding with this tab"""
        return collides_point(position, (self.x, self.y, self.width, self.height))
    
class TabBar:
    def draw(self, window, offset):
        """Draws the A-Z tabbar vertically at the given location"""
        self.x, self.y = offset
        width, height = 50, Globals.HEIGHT

        pyg.draw.rect(window, ColorTheme.current_theme.background_border_color, (self.x, self.y, width, height), border_radius=5)
        pyg.draw.rect(window, ColorTheme.current_theme.background_color, (self.x + 2, self.y + 2, width-4, height-4), border_radius=5)

        tab_height = height // 26
        tab_height -= 2

        vertical_offset = 2

        for i in range(26):
            extra_height = 1 if (i % 3 == 0) else 0
            rect_color = ColorTheme.current_theme.field_background_color
            if collides_point(Globals.mouse_position, (self.x - 1, vertical_offset-2, width, tab_height + extra_height)):
                rect_color = ColorTheme.current_theme.field_border_color

            if i == 0:
                pyg.draw.rect(window, rect_color, (self.x + 2, vertical_offset+1, width-4, tab_height), border_top_left_radius=5, border_top_right_radius=5)
            elif i == 25:
                pyg.draw.rect(window, rect_color, (self.x + 2, vertical_offset, width-4, tab_height), border_bottom_left_radius=5, border_bottom_right_radius=5)
            else:
                pyg.draw.rect(window, rect_color, (self.x + 2, vertical_offset, width-4, tab_height + extra_height))

            char = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"[i]
            text_width, text_height = Fonts.font_20.size(char)
            window.blit(Fonts.font_20.render(char, True, ColorTheme.current_theme.text_color), (self.x + 2 + (width - text_width)/2, vertical_offset + (tab_height - text_height)/2))
            vertical_offset += tab_height + extra_height + 2
    
    def check_mcollision(self):
        """Checks the collision of the A-Z tabs"""
        width, height = 50, Globals.HEIGHT
        vertical_offset = 2
        tab_height = height // 26
        tab_height -= 2

        for i in range(26):
            extra_height = 1 if (i % 3 == 0) else 0
            if collides_point(Globals.mouse_position, (self.x-1, vertical_offset-2, width, tab_height + extra_height)):
                return i
            vertical_offset += tab_height + extra_height + 2

class TabComponentBase:
    """Base class for all of the tab components
    
    Attributes:
        x, y: Position of this component on screen
        width, height: Size of this component
        display_surface: The surface which this component draws to, which gets drawn to screen
    """
    def __init__(self, position: tuple, size: tuple):
        self.x, self.y = position
        self.width, self.height = size
        self._display_surface = pyg.Surface(size)

    def draw_background(self):
        self._display_surface.fill(ColorTheme.current_theme.field_background_color)
        pyg.draw.rect(self._display_surface, ColorTheme.current_theme.background_color, (2, 2, self.width - 4, self.height - 4), border_radius=8)

    def draw_field_multiline(self, field_width: int, font: pyg.font.Font, text: list, position: tuple):
        """Draws lines of text starting at the given position"""
        x, y = position
        field_height = 8
        char_width, char_height = font.size("A")

        # Get necessary size of field
        for i in range(len(text)):
            temp = chunk_text.chunk(text[i], content_width=field_width, char_width=char_width)
            for line in temp:
                field_height += char_height + 2

        pyg.draw.rect(self._display_surface, ColorTheme.current_theme.field_background_color, (x, y, field_width, field_height), border_radius=4)
        pyg.draw.rect(self._display_surface, ColorTheme.current_theme.field_border_color, (x + 2, y + 2, field_width - 4, field_height - 4), border_radius=4)
        y += 4

        # Draw lines of text
        for i in range(len(text)):
            temp = chunk_text.chunk(text[i], content_width=field_width, char_width=char_width)
            for line in temp:
                self._display_surface.blit(Fonts.font_24.render(line.strip(), True, ColorTheme.current_theme.text_color), (x + 5, y))
                y += char_height + 2

        return y