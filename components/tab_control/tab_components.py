import pygame as pyg
import copy

from common.classes.buttons import Checkbox
from common.classes.input_field import InputField
from common.classes.display import Colors, Fonts
from common.classes.globals import Globals
from common.modules.collider import collides_point
import common.modules.chunk_text as chunk_text

class TabBar:
    def draw(self, window, offset):
        """Draws the A-Z tabbar vertically at the given location"""
        self.x, self.y = offset
        width, height = 50, Globals.HEIGHT

        pyg.draw.rect(window, Colors.dark_black, (self.x, self.y, width, height), border_radius=5)
        pyg.draw.rect(window, Colors.black, (self.x + 2, self.y + 2, width-4, height-4), border_radius=5)

        tab_height = height // 26
        tab_height -= 2

        vertical_offset = 2

        for i in range(26):
            extra_height = 1 if (i % 3 == 0) else 0
            rect_color = Colors.light_gray if collides_point(Globals.mouse_position, (self.x - 1, vertical_offset-2, width, tab_height + extra_height)) else Colors.gray

            if i == 0:
                pyg.draw.rect(window, rect_color, (self.x + 2, vertical_offset+1, width-4, tab_height), border_top_left_radius=5, border_top_right_radius=5)
            elif i == 25:
                pyg.draw.rect(window, rect_color, (self.x + 2, vertical_offset, width-4, tab_height), border_bottom_left_radius=5, border_bottom_right_radius=5)
            else:
                pyg.draw.rect(window, rect_color, (self.x + 2, vertical_offset, width-4, tab_height + extra_height))

            char = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"[i]
            text_width, text_height = Fonts.font_20.size(char)
            window.blit(Fonts.font_20.render(char, True, Colors.white), (self.x + 2 + (width - text_width)/2, vertical_offset + (tab_height - text_height)/2))
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

def draw_field_multiline(window, width, font, text: list, position, none_text="No description set"):
        """Draws lines of text starting at the given position"""
        x, y = position
        height = 8
        char_width, char_height = font.size("A")

        for i in range(len(text)):
            # Pop item out and insert corrent length lines, if line is too long
            temp = chunk_text.chunk(text[i], content_width=width, char_width=char_width)
            for line in temp:
                height += char_height + 2

        pyg.draw.rect(window, Colors.gray, (x, y, width, height), border_radius=4)
        pyg.draw.rect(window, Colors.dark_gray, (x + 2, y + 2, width - 4, height - 4), border_radius=4)
        y += 4

        # Draw lines of text
        for i in range(len(text)):
            # Pop item out and insert corrent length lines, if line is too long
            temp = chunk_text.chunk(text[i], content_width=width, char_width=char_width)
            for line in temp:
                window.blit(Fonts.font_24.render(line.strip(), True, Colors.white), (x + 5, y))
                y += char_height + 2

        return y


class Tab:
    def __init__(self, rect, text):
        self.x, self.y, self.width, self.height = rect
        self.text = text
        self.active = False

    def draw(self, window):
        """Draws the tabs corresponding to its parent tab view"""
        pyg.draw.rect(window, Colors.black, (self.x, self.y, self.width, self.height), border_top_left_radius=8, border_top_right_radius=8)
        color = Colors.light_gray if self.check_mcollision() else Colors.gray
        color = Colors.lighter_gray if self.active else color

        pyg.draw.rect(window, color, (self.x+2, self.y+2, self.width-4, self.height-2), border_top_left_radius=8, border_top_right_radius=8)

        text_width, text_height = Fonts.font_18.size(self.text)
        window.blit(Fonts.font_18.render(self.text, True, Colors.white), (self.x + (self.width - text_width)/2, self.y + 2 + (self.height - text_height)/2))

    def check_mcollision(self):
        return collides_point(Globals.mouse_position, (self.x, self.y, self.width, self.height))
    

class DefinitionView:
    def __init__(self):
        self.clear_search_button = None

    def draw(self, window, position, current_search):
        """Draws the definition view component"""
        # Get position to draw
        x, y = position
        field_width = 800

        keyword, description, related = current_search.get_data()
        window.blit(Fonts.font_30.render("Keyword:", True, Colors.white), (x + 40, y + 50))

        # Draw keyword text
        char_width, char_height = Fonts.font_24.size("A")
        pyg.draw.rect(window, Colors.gray, (x + 45, y + 95, field_width, char_height + 10), border_radius=4)
        pyg.draw.rect(window, Colors.dark_gray, (x + 47, y + 97, field_width - 4, char_height + 6), border_radius=4)

        window.blit(Fonts.font_24.render(keyword, True, Colors.white), (x + 50, y + 100))

        # Draw description
        window.blit(Fonts.font_30.render("Description:", True, Colors.white), (x + 40, y + 165))
        description_text = description.split(";")
        if len(description_text[0]) == 0:
            description_text = ["No description set"]

        # Format description
        temp_desc = copy.deepcopy(description_text)
        for i in range(len(temp_desc)):
            if temp_desc[i] != "No description set" and not str(i+1) in temp_desc[i]:
                temp_desc[i] = temp_desc[i].strip()
                temp_desc[i] = "(" + str(i+1) + ") " + temp_desc[i][0].capitalize() + temp_desc[i][1:]

        line_offset = y + 210
        line_offset = draw_field_multiline(window, field_width, Fonts.font_24, temp_desc, (x + 40, line_offset))

        # Draw related terms
        line_offset += 50
        window.blit(Fonts.font_30.render("Related Terms:", True, Colors.white), (x + 40, line_offset))
        line_offset += 40
        if len(related) == 0:
            related = ["No related links set"]
        
        # Format terms
        temp_related = copy.deepcopy(related)
        for i in range(len(temp_related)):
            if temp_related[i] != "No related terms set":
                temp_related[i] = "(" + str(i+1) + ") " + temp_related[i][0].capitalize() + temp_related[i][1:]
            
        line_offset = draw_field_multiline(window, field_width, Fonts.font_24, temp_related, (x + 40, line_offset), none_text="No related links set")

        # Draw references
        references = current_search.data["references"]
        if len(references) > 0:
            line_offset += 50
            window.blit(Fonts.font_30.render("References:", True, Colors.white), (x + 40, line_offset))
            line_offset += 40

            # Format references
            temp_reff = []
            for i in range(len(references)):
                temp_reff += references[i].split(";")

            for i in range(len(temp_reff)):
                if not str(i+1) in temp_reff[i]:
                    temp_reff[i] = "(" + str(i+1) + ") " + temp_reff[i][0].capitalize() + temp_reff[i][1:]
            
            line_offset = draw_field_multiline(window, field_width, Fonts.font_24, temp_reff, (x + 40, line_offset))
            
        # Draw page number
        line_offset += 30
        page = current_search.data["page_number"]
        text_width = -20
        if page != "":
            line_offset += 20
            text_width = Fonts.font_30.size("Page number: ")[0]
            window.blit(Fonts.font_30.render("Page number: ", True, Colors.white), (x + 40, line_offset))
            window.blit(Fonts.font_30.render(str(page), True, Colors.aqua), (x + 40 + text_width, line_offset))
            text_width += Fonts.font_30.size(str(page))[0]

        line_offset_h = text_width + 20
        attributes = ["Verb", "Noun", "Adjective"]
        for attribute in attributes:
            if current_search.data["is_" + attribute.lower()]:
                window.blit(Fonts.font_24.render(attribute, True, Colors.green), (x + 40 + line_offset_h, line_offset + 4))
                line_offset_h += Fonts.font_24.size(attribute + " ")[0]

        self.clear_search_button.draw()


class SearchView:
    def __init__(self, position):
        self.x, self.y = position
        self.width, self.height = Globals.WIDTH - self.x, Globals.HEIGHT - 50
        self.searchbar = InputField((self.x + 50, self.y + 50, self.width - 100, 30), Fonts.font_20, "Enter Search")
        self.history = []

    def draw(self, window):
        """Draws the search view component"""
        window.blit(Fonts.font_24.render("Search for Terms:", True, Colors.white), (self.x + 50, self.y + 20))
        self.searchbar.draw(None)
        char_height = Fonts.font_24.size("A")[1]

        window.blit(Fonts.font_24.render("Search History:", True, Colors.white), (self.x + 50, self.y + 100))
        pyg.draw.rect(window, Colors.gray, (self.x + 50, self.y + 130, self.width - 100, (char_height + 2) * 20), border_radius=8)
        pyg.draw.rect(window, Colors.black, (self.x + 52, self.y + 132, self.width - 104, (char_height + 2) * 20 - 4), border_radius=8)

        # Draw search history links
        for i in range(min(20, len(self.history))):
            index = len(self.history) - i - 1

            if collides_point(Globals.mouse_position, (self.x + 55, self.y + 134 + i * (char_height + 2), self.width - 110, char_height + 2)):
                pyg.draw.rect(window, Colors.gray, (self.x + 55, self.y + 134 + i * (char_height + 2), self.width - 110, char_height + 2), border_radius=4)

            window.blit(Fonts.font_24.render(self.history[index], True, Colors.white), (self.x + 60, self.y + 135 + i * (char_height + 2)))

    def check_history_clicked(self):
        for i in range(min(20, len(self.history))):
            index = len(self.history) - i - 1
            char_height = Fonts.font_24.size("A")[1]

            if collides_point(Globals.mouse_position, (self.x + 50, self.y + 129 + i * (char_height + 2), self.width - 100, char_height + 2)):
                return index
            
class SettingsView:
    def __init__(self, position):
        self.x, self.y = position
        self.width, self.height = Globals.WIDTH - self.x, Globals.HEIGHT - 50

        # Settings!
        self.boxes = {
            "show_fps": Checkbox((self.x + 20, self.y + 20, 20, 20), "Show FPS", Fonts.font_20, right_align=True),
            "save_history": Checkbox((self.x + 20, self.y + 50, 20, 20), "Save Search History", Fonts.font_20, True, right_align=True)
        }

    def draw(self, window):
        """Draws the settings view component"""
        for box in self.boxes.keys():
            self.boxes[box].draw(window)