import pygame as pyg
import copy

from common.classes.buttons import Button
from common.classes.display import Colors, ColorTheme, Fonts
from components.tab_control.tab_components import TabComponentBase


class DefinitionView(TabComponentBase):
    """The definition pane of the tab view
    
    Attributes:
        clear_search_button: The button to clear the current definition
        split_semis: Determines whether to split the definition on semicolons
    """
    def __init__(self, position: tuple, size: tuple):
        super().__init__(position, size)
        self.clear_search_button = Button((self.width/2 - 100, self.height - 50, 200, 30), Colors.red, "Clear Definition", Fonts.font_20, Colors.white)
        self.split_semis = True

        self.current_search = None

    def draw(self, window: pyg.Surface, mouse_position: list[int]):
        """Draws the different objects of this component"""
        self.draw_background()
        mouse_position[0] -= self.x
        mouse_position[1] -= self.y
        
        field_width = 800
        if self.current_search is None:
            text_width = Fonts.font_30.size("No Definition Selected")[0]
            self._display_surface.blit(Fonts.font_30.render("No Definition Selected", True, ColorTheme.current_theme.text_color), (self.width/2 - text_width/2, 20))
            window.blit(self._display_surface, (self.x, self.y))
            return
        
        keyword, description, related = self.current_search.get_data()
        self._display_surface.blit(Fonts.font_30.render("Keyword:", True, ColorTheme.current_theme.text_color), (40, 50))

        # Draw keyword text
        char_height = Fonts.font_24.size("A")[1]
        pyg.draw.rect(self._display_surface, ColorTheme.current_theme.field_background_color, (45, 95, field_width, char_height + 10), border_radius=4)
        pyg.draw.rect(self._display_surface, ColorTheme.current_theme.field_border_color, (47, 97, field_width - 4, char_height + 6), border_radius=4)

        self._display_surface.blit(Fonts.font_24.render(keyword, True, ColorTheme.current_theme.text_color), (50, 100))

        # Draw description
        self._display_surface.blit(Fonts.font_30.render("Description:", True, ColorTheme.current_theme.text_color), (40, 165))
        if self.split_semis:
            description_text = description.split(";")
        else:
            description_text = [description]
        if len(description_text[0]) == 0:
            description_text = ["No description set"]

        # Format description
        temp_desc = copy.deepcopy(description_text)
        for i in range(len(temp_desc)):
            if temp_desc[i] != "No description set" and not str(i+1) in temp_desc[i]:
                temp_desc[i] = temp_desc[i].strip()
                temp_desc[i] = "(" + str(i+1) + ") " + temp_desc[i][0].capitalize() + temp_desc[i][1:]

        line_offset = 210
        line_offset = self.draw_field_multiline(field_width, Fonts.font_24, temp_desc, (40, line_offset))

        # Draw related terms
        if related:
            line_offset += 50
            self._display_surface.blit(Fonts.font_30.render("Related Terms:", True, ColorTheme.current_theme.text_color), (40, line_offset))
            line_offset += 40
            if len(related) == 0:
                related = ["No related links set"]
            
            # Format terms
            temp_related = copy.deepcopy(related)
            for i in range(len(temp_related)):
                if temp_related[i] != "No related terms set":
                    temp_related[i] = temp_related[i][0].capitalize() + temp_related[i][1:] 
                    temp_related[i] += "," if i != len(temp_related) - 1 else ""
                
            line_offset = self.draw_field_multiline(field_width, Fonts.font_24, [" ".join(temp_related)], (40, line_offset))

        # Draw references
        references = self.current_search.data["references"]
        if len(references) > 0:
            line_offset += 50
            self._display_surface.blit(Fonts.font_30.render("References:", True, ColorTheme.current_theme.text_color), (40, line_offset))
            line_offset += 40

            # Format references
            temp_reff = []
            for i in range(len(references)):
                temp_reff += references[i].split(";")

            for i in range(len(temp_reff)):
                if not "(" + str(i+1) + ")" in temp_reff[i]:
                    space = " " if temp_reff[i][0] != " " else ""
                    temp_reff[i] = "(" + str(i+1) + ")" + space + temp_reff[i][0].capitalize() + temp_reff[i][1:]
            
            line_offset = self.draw_field_multiline(field_width, Fonts.font_24, temp_reff, (40, line_offset))
            
        # Draw page number
        line_offset += 30
        page = self.current_search.data["page_number"]
        text_width = -20
        if page != "":
            line_offset += 20
            text_width = Fonts.font_30.size("Page number: ")[0]
            self._display_surface.blit(Fonts.font_30.render("Page number: ", True, ColorTheme.current_theme.text_color), (40, line_offset))

            if ColorTheme.current_theme == ColorTheme.dark_mode:
                self._display_surface.blit(Fonts.font_30.render(str(page), True, Colors.aqua), (40 + text_width, line_offset))
            else:
                self._display_surface.blit(Fonts.font_30.render(str(page), True, Colors.dark_aqua), (40 + text_width, line_offset))

            text_width += Fonts.font_30.size(str(page))[0]

        line_offset_h = text_width + 20
        attributes = ["Verb", "Noun", "Adjective"]
        for attribute in attributes:
            if self.current_search.data["is_" + attribute.lower()]:
                self._display_surface.blit(Fonts.font_24.render(attribute, True, Colors.green), (40 + line_offset_h, line_offset + 4))
                line_offset_h += Fonts.font_24.size(attribute + " ")[0]

        self.clear_search_button.draw(self._display_surface, mouse_position)

        window.blit(self._display_surface, (self.x, self.y))

    def click(self, position: list):
        """Simulates a click in the definition view component"""
        position[0] = position[0] - self.x
        position[1] = position[1] - self.y

        if self.clear_search_button.check_mcollision(position):
            self.current_search = None
            # results_view.update_search()
            return