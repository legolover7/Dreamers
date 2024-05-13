import contextlib
with contextlib.redirect_stdout(None):
    import pygame as pyg

from common.classes.display import Colors, Fonts, ColorTheme
from common.classes.globals import Globals
import common.modules.collider as collider
import common.modules.chunk_text as chunk_text

class IFBase:
    """The base/parent class of all Input Fields
    
    Attributes:
        x, y: Integer values of where the field is located on the screen
        width, height: Integer values of how large the field is
        default_text: The text that gets shown if no text is entered into the field
        font: The font of the text that is displayed
        
        display_surface: The surface that this field is drawn to, then which is drawn to the screen

        border_radius: The border radius of the field
        border_size: How large the size of the border is
        text_spacing: The additional spacing between lines of text
        line_spacing: The total space between lines of text
        char_width: The width of a single character
    """
    def __init__(self, rect: pyg.Rect, default_text: str, font: pyg.font.Font):
        # Set params
        self.x, self.y, self.width, self.height = rect
        self.default_text = default_text
        self.text_font = font

        self.display_surface = pyg.Surface((self.width, self.height))

        # Set defaults
        self.border_radius = 8
        self.border_size = 2
        self.text_spacing = 1
        self.line_spacing = self.text_font.size("A")[1] + self.text_spacing
        self.char_width = self.text_font.size(" ")[0]

    def draw_rect(self):
        """Draws the background/base of this input field"""
        self.display_surface.fill(ColorTheme.current_theme.background_color)
        pyg.draw.rect(self.display_surface, ColorTheme.current_theme.field_background_color, (0, 0, self.width, self.height), border_radius=self.border_radius)
        pyg.draw.rect(self.display_surface, ColorTheme.current_theme.field_border_color, (0 + self.border_size, 0 + self.border_size, self.width - self.border_size * 2, self.height - self.border_size * 2), border_radius=self.border_radius)

    def draw_text_line(self, line: str, position: int, color: tuple = ColorTheme.current_theme.text_color):
        """Draws the given line of text to this input field. Doesn't draw if it's off the screen"""
        if position < -1 or position > self.height / self.line_spacing:
            return
        self.display_surface.blit(self.text_font.render(line, True, color), (4, 4 + self.line_spacing * position))

    def draw_cursor(self, line: str, line_position: int, char_position: int):
        """Draws the cursor at the given line, offset to the given character position"""
        if Globals.cursor_frame > Globals.cursor_timeout or (Globals.cursor_frame % Globals.cursor_period < Globals.cursor_period / 2):
            horizontal_position = 4 + self.text_font.size(line[:char_position])[0]
            pyg.draw.rect(self.display_surface, ColorTheme.current_theme.cursor_color, (horizontal_position, 4 + line_position * self.line_spacing, 2, self.line_spacing - self.text_spacing * 2))

    def blit_to_screen(self, window: pyg.Surface):
        """Display this field to the screen"""
        window.blit(self.display_surface, (self.x, self.y))

    def check_mcollision(self, point: list=[0, 0]):
        """Returns true if the mouse cursor is colliding with this field"""
        m = point if point != [0, 0] else Globals.mouse_position
        return collider.collides_point(m, (self.x, self.y, self.width, self.height))

class IFBlock(IFBase):
    """An Input Field that allows for newline characters and scrolling
    
    Attributes:
        text: The current contents of the field
        scroll_offset: An integer representing how many pixels the content has been scrolled
        scroll_step: An integer representing how much to scroll by
        active: Whether or not his field is active
    """

    def __init__(self, rect: pyg.Rect, default_text: str, font: pyg.font.Font):
        super().__init__(rect, default_text, font)

        self.text = ""
        self.scroll_offset = 0
        self.scroll_step = 0.3
        self.active = False


    def draw(self, window: pyg.Surface):
        """Draws this Input Field Block"""
        self.draw_rect()

        if self.text != "":
            text = self.text
            text_color = ColorTheme.current_theme.text_color
        else:
            text = self.default_text
            text_color = ColorTheme.current_theme.dim_text_color

        self.text_lines = []
        temp_lines = chunk_text.split_lines(text)
        
        # Split the text into individual lines
        for line in temp_lines:
            if line == "":
                self.text_lines += [""]
            else:
                self.text_lines += chunk_text.chunk(line, content_width=self.width, char_width=self.char_width)
        
        # Display lines
        cursor_position = Globals.cursor_position
        drawn_cursor = False
        for i in range(len(self.text_lines)):
            current_line = self.text_lines[i]
            if self.active:
                # Calculate cursor position
                if len(current_line) < cursor_position:
                    cursor_position -= len(current_line)
                elif not drawn_cursor:
                    drawn_cursor = True
                    self.draw_cursor(current_line, i - self.scroll_offset, cursor_position)
            self.draw_text_line(current_line.replace("\r", ""), i - self.scroll_offset, text_color)

        if len(self.text_lines) > (self.height / self.line_spacing + 3 / self.line_spacing):
            self.draw_scrollbar()

        self.blit_to_screen(window)

    def scroll_content(self, direction: int, type=""):
        """Scrolls the content of this field in the given direction. Providing 'max' or 'min' will scroll to the max or min amount, respectively"""
        # Only allow scrolling if the lines of text go off screen
        # Min and max height are the minimum and maximum amount that the scrolled text can be offset by
        min_height, max_height = 0, len(self.text_lines) - (self.height / self.line_spacing) + 4 / self.line_spacing
        max_height = max(min_height, max_height)

        if type == "max": 
            self.scroll_offset = max_height
        elif type == "min":
            self.scroll_offset = min_height
        else:
            self.scroll_offset += self.scroll_step * direction
            self.scroll_offset = min(max(self.scroll_offset, min_height), max_height)

    def draw_scrollbar(self):
        max_height = len(self.text_lines) - (self.height / self.line_spacing) + 2 / self.line_spacing
        ratio = max_height / len(self.text_lines)
        if self.scroll_offset == 0:
            travel_percentage = 0
        else:
            travel_percentage = self.scroll_offset / len(self.text_lines)

        pyg.draw.rect(self.display_surface, Colors.white, (self.width - 6, 2 + travel_percentage * self.height, 2, self.height * (1 - ratio) - 4))

class IFBox(IFBase):
    def __init__(self, rect: pyg.Rect, default_text: str, font: pyg.font.Font, max_length = 0):
        super().__init__(rect, default_text, font)

        self.text = ""
        self.active = False
        self.max_length = max_length
        if max_length == -1:
            self.max_length = self.width // self.char_width
        self.max_length = int(self.max_length)

    def draw(self, window: pyg.Surface):
        self.draw_rect()
        
        # Text can't be longer than max_length if not 0
        if len(self.text) >= self.max_length  and self.max_length != 0:
            self.text = self.text[:self.max_length - 1]
            Globals.cursor_position -= 1

        if self.text != "":
            text = self.text
            text_color = ColorTheme.current_theme.text_color
        else:
            text = self.default_text
            text_color = ColorTheme.current_theme.dim_text_color

        text_lines = chunk_text.chunk(text, max_length=self.max_length)

        cursor_position = Globals.cursor_position
        for i in range(len(text_lines)):
            current_line = text_lines[i]
            if self.active:
                # Calculate cursor position
                if len(current_line) < cursor_position:
                    cursor_position -= len(current_line)
                else:
                    self.draw_cursor(current_line, i, cursor_position)
            self.draw_text_line(current_line, i, text_color)

        self.blit_to_screen(window)

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
        pyg.draw.rect(window, ColorTheme.current_theme.field_background_color, (self.x, self.y, self.width, self.height), border_radius=5)
        pyg.draw.rect(window, ColorTheme.current_theme.field_border_color, (self.x + 2, self.y + 2, self.width - 4, self.height - 4), border_radius=5)
        
        if self.text == "" and not self.active:
            window.blit(Fonts.font_20.render("Date of Dream", True, ColorTheme.current_theme.dim_text_color), (self.x + 4, self.y + 4))
        
        else:
            # Draw deliminators
            horizontal_position = self.x + 4
            split_format = self.format.split("/")
            for section in split_format:
                horizontal_position += Fonts.font_20.size(section)[0]
                if split_format.index(section) != len(split_format) - 1:
                    window.blit(Fonts.font_20.render("/", True, ColorTheme.current_theme.text_color), (horizontal_position, self.y + 4))
                horizontal_position += Fonts.font_20.size("/")[0]

            if self.active:
                self.cursor_position = Globals.cursor_position
            cursor_position = self.cursor_position
            current_offset = cursor_offset = current_text_offset = 0
            # Draw text
            for section in self.format.split("/"):
                char_width = Fonts.font_20.size("A")[0]
                date_portion = self.text[current_text_offset:current_text_offset + len(section)]
                window.blit(Fonts.font_20.render(date_portion, True, ColorTheme.current_theme.text_color), (self.x + 4 + char_width * current_offset, self.y + 4))
                
                if cursor_position >= len(section) - (1 if current_offset > 0 else 0):
                    cursor_offset += len(section) + 2
                    current_offset += len(section) + 1
                    cursor_position -= len(section) + 1
                    current_text_offset += len(section)

                # Draw cursor
                if self.active and not cursor_position >= len(section) - (1 if current_offset > 0 else 0):
                    pyg.draw.line(window, ColorTheme.current_theme.text_color, (self.x + 4 + char_width * (cursor_offset + cursor_position), self.y + 4), (self.x + 4 + char_width * (cursor_offset + cursor_position), self.y + self.height - 4))

    def check_mcollision(self, point: list=[0, 0]):
        m = point if point != [0, 0] else Globals.mouse_position
        return collider.collides_point(m, (self.x, self.y, self.width, self.height))