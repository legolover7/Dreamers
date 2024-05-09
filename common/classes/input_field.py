import contextlib
with contextlib.redirect_stdout(None):
    import pygame as pyg

from common.classes.display import Colors, Fonts
from common.classes.globals import Globals
from common.modules.collider import collides_point
from common.modules.chunk_text import chunk

class InputField():
    def __init__(self, rect, font, default_text="Enter text", increases_upwards=False, title="", title_font=None, scrollable=False, center_text=True):
        self.x, self.y, self.width, self.height = rect
        self.default_text = default_text
        self.font = font
        self.text = ""
        self.increases_upwards = increases_upwards
        self.title = title
        self.title_font = title_font
        self.active = False
        self.scrollable = scrollable
        self.scroll_offset = 0
        self.center_text = center_text

    def draw(self, window, active=None, offset=0):
        # Get the field's text content and set its correct color
        text = self.text if self.text != "" or self == active else self.default_text
        color = Colors.white if self.text != "" else Colors.lighter_gray

        if self.title != "":
            text_height = self.title_font.size(self.title)[1]
            window.blit(self.title_font.render(self.title, True, Colors.white), (self.x, self.y - text_height - 4 + offset))

        # Split the field's text content by the maximum amount of character able to fit on a single line
        text_lines = chunk(text, content_width=self.width-5, char_width=self.font.size("|")[0])
        # Calculate the extra height that the field should be to account for multiple lines of text
        extra_height = max(0, (len(text_lines) - 1) * (self.font.size("A")[1] + 2))
        if self.scrollable: extra_height = 0
        
        # Display background
        pyg.draw.rect(window, Colors.gray, (self.x, self.y - (extra_height if self.increases_upwards else 0) + offset, self.width, self.height + extra_height), border_radius=5)
        pyg.draw.rect(window, Colors.dark_gray, (self.x+2, self.y+2 - (extra_height if self.increases_upwards else 0) + offset, self.width-4, self.height-4 + extra_height), border_radius=5)
        
        # Display the lines of text
        vertical_offset = -extra_height if self.increases_upwards else 0
        vertical_offset -= self.scroll_offset
        cursor_position = Globals.cursor_position
        
        # Displays cursor if the length of the message is 0
        if len(text_lines) == 0 and (Globals.cursor_frame > Globals.cursor_timeout or (Globals.cursor_frame % Globals.cursor_period < Globals.cursor_period / 2)):
            text_height = self.font.size("A")[1]
            pyg.draw.rect(window, Colors.white, (self.x + 4, self.y + vertical_offset + (self.height - text_height)/2 + offset, 2, text_height))

        for line in text_lines:
            # Display the current line, and increase the next line's offset
            text_height = self.font.size(line)[1]
            window.blit(self.font.render(line, True, color), (self.x + 4, self.y + vertical_offset + ((self.height - text_height)/2 if self.center_text else 5) + offset))
            
            # Draw cursor only on the current line
            if (self == active or self.active) and (Globals.cursor_frame > Globals.cursor_timeout or (Globals.cursor_frame % Globals.cursor_period < Globals.cursor_period / 2)):
                if cursor_position <= len(line):
                    text_width = self.font.size(line[:Globals.cursor_position])[0]
                    pyg.draw.rect(window, Colors.white, (self.x + 4 + (text_width), self.y + vertical_offset + ((self.height - text_height)/2 if self.center_text else 5) + offset, 2, text_height))
                else:
                    cursor_position -= len(line)

            vertical_offset += text_height + 2

    def check_mcollision(self, offset=0):
        return collides_point(Globals.mouse_position, (self.x, self.y + offset, self.width, self.height))
    
    def scroll_text_content(self, direction):
        """Adjusts the scroll offset for the input field, thereby scrolling the content"""
        scroll_amount = 10
        self.scroll_offset += scroll_amount * direction
        self.scroll_offset = max(0, self.scroll_offset)
        # Don't scroll if there's space left in the input field
        lines = chunk(self.text, content_width=self.width-5, char_width=self.font.size("A")[0])
        char_height = self.font.size("A")[1]
        if len(lines) < self.height / (char_height + 2):
            self.scroll_offset = 0

        self.scroll_offset = min(self.scroll_offset, len(lines) * (char_height + 2))

class DateInput:
    def __init__(self, rect: tuple, format: str):
        self.x, self.y, self.width, self.height = rect
        self.format = format
        self.active = False
        self.text = ""
        self.cursor_position = 0

    def draw(self, window: pyg.Surface):
        max_length = len("".join(self.format.split("/")))
        if len(self.text) > max_length:
            self.text = self.text[:max_length]
            Globals.cursor_position = len(self.text)

        # Draw box
        pyg.draw.rect(window, Colors.gray, (self.x, self.y, self.width, self.height), border_radius=5)
        pyg.draw.rect(window, Colors.dark_gray, (self.x + 2, self.y + 2, self.width - 4, self.height - 4), border_radius=5)
        
        if self.text == "" and not self.active:
            window.blit(Fonts.font_20.render("Date of Dream", True, Colors.lighter_gray), (self.x + 4, self.y + 4))
        
        else:
            # Draw deliminators
            horizontal_position = self.x + 4
            split_format = self.format.split("/")
            for section in split_format:
                horizontal_position += Fonts.font_20.size(section)[0]
                if split_format.index(section) != len(split_format) - 1:
                    window.blit(Fonts.font_20.render("/", True, Colors.white), (horizontal_position, self.y + 4))
                horizontal_position += Fonts.font_20.size("/")[0]

            if self.active:
                self.cursor_position = Globals.cursor_position
            cursor_position = self.cursor_position
            current_offset = cursor_offset = current_text_offset = 0
            # Draw text
            for section in self.format.split("/"):
                char_width = Fonts.font_20.size("A")[0]
                date_portion = self.text[current_text_offset:current_text_offset + len(section)]
                window.blit(Fonts.font_20.render(date_portion, True, Colors.white), (self.x + 4 + char_width * current_offset, self.y + 4))
                
                if cursor_position >= len(section) - (1 if current_offset > 0 else 0):
                    cursor_offset += len(section) + 2
                    current_offset += len(section) + 1
                    cursor_position -= len(section) + 1
                    current_text_offset += len(section)

                # Draw cursor
                if self.active and not cursor_position >= len(section) - (1 if current_offset > 0 else 0):
                    pyg.draw.line(window, Colors.white, (self.x + 4 + char_width * (cursor_offset + cursor_position), self.y + 4), (self.x + 4 + char_width * (cursor_offset + cursor_position), self.y + self.height - 4))

    def check_mcollision(self):
        return collides_point(Globals.mouse_position, (self.x, self.y, self.width, self.height))