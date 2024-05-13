import pygame as pyg

from common.classes.display import Colors, ColorTheme, Fonts
from common.classes.globals import Globals
from common.classes.input_field import IFBox
from components.tab_control.tab_components import TabComponentBase

import common.modules.collider as collider

class SearchView(TabComponentBase):
    """The search pane of the tab view
    
    Attributes:
        history: The history of the past searches the user has entered
        search_index: Used for navigating previous searches 
        searchbar: An IFBox allowing the user to search for things
    """
    def __init__(self, position: tuple[int], size: tuple[int]):
        super().__init__(position, size)
        
        self.history = []
        self.search_index = 0
        
        self.searchbar = IFBox((50, 50, self.width - 200, 30), "Enter Search", Fonts.font_20, max_length=-1)

    def draw(self, window: pyg.Surface, mouse_position: list[int]):
        """Draws the different objects of this component"""
        self.draw_background()
        
        # Calculate relative mouse position
        mouse_position[0] = mouse_position[0] - self.x
        mouse_position[1] = mouse_position[1] - self.y

        # Draw searchbar and search history
        self._display_surface.blit(Fonts.font_24.render("Search for Terms:", True, ColorTheme.current_theme.text_color), (50, 20))
        self.searchbar.draw(self._display_surface)
        char_height = Fonts.font_24.size("A")[1]

        self._display_surface.blit(Fonts.font_24.render("Search History:", True, ColorTheme.current_theme.text_color), (50, 100))
        pyg.draw.rect(self._display_surface, ColorTheme.current_theme.field_border_color, (50, 130, self.width - 100, (char_height + 2) * 20), border_radius=8)
        pyg.draw.rect(self._display_surface, ColorTheme.current_theme.field_background_color, (52, 132, self.width - 104, (char_height + 2) * 20 - 4), border_radius=8)

        # Draw navigation arrows
        x = self.width - 130
        y = 50
        # Left
        if collider.collides_point(mouse_position, circle=(x + 7, y + 16, 13)):
            pyg.draw.circle(self._display_surface, Colors.dark_gray, (x + 7, y + 16), 13)
        pyg.draw.line(self._display_surface, Colors.white, (x, y + 15), (x + 14, y + 15))
        pyg.draw.line(self._display_surface, Colors.white, (x, y + 15), (x + 7, y + 8))
        pyg.draw.line(self._display_surface, Colors.white, (x, y + 15), (x + 7, y + 22))

        # Right
        if collider.collides_point(mouse_position, circle=(x + 39, y + 16, 13)):
            pyg.draw.circle(self._display_surface, Colors.dark_gray, (x + 39, y + 16), 13)
        pyg.draw.line(self._display_surface, Colors.white, (x + 32, y + 15), (x + 46, y + 15))
        pyg.draw.line(self._display_surface, Colors.white, (x + 46, y + 15), (x + 39, y + 8))
        pyg.draw.line(self._display_surface, Colors.white, (x + 46, y + 15), (x + 39, y + 22))

        # Draw search history links
        for i in range(min(20, len(self.history))):
            index = len(self.history) - i - 1

            if collider.collides_point(mouse_position, (55, 134 + i * (char_height + 2), self.width - 110, char_height + 2)):
                pyg.draw.rect(self._display_surface, ColorTheme.current_theme.selected_tab_color, (55, 134 + i * (char_height + 2), self.width - 110, char_height + 2), border_radius=4)

            self._display_surface.blit(Fonts.font_24.render(self.history[index], True, ColorTheme.current_theme.text_color), (60, 135 + i * (char_height + 2)))

        window.blit(self._display_surface, (self.x, self.y))

    def check_nav_arrow_clicked(self, mouse_position: list[int]):
        """Returns back/forward if the respective nav arrow was clicked"""

        x = self.width - 130
        y = 50
        if collider.collides_point(mouse_position, circle=(x + 7, y + 16, 13)) and self.search_index < len(self.history) - 1:
            return "back"
        if collider.collides_point(mouse_position, circle=(x + 39, y + 16, 13)) and self.search_index > 0:
            return "forward"

    def check_history_clicked(self, mouse_position: list[int]):
        """Returns an index if one of the search history items were clicked"""
        for i in range(min(20, len(self.history))):
            index = len(self.history) - i - 1
            char_height = Fonts.font_24.size("A")[1]

            if collider.collides_point(mouse_position, (55, 134 + (i + 1) * (char_height + 2), self.width - 110, char_height + 2)):
                return index
            
    def click(self, mouse_position: list):
        """Simulates a click in the search view component"""
        mouse_position[0] = mouse_position[0] - self.x
        mouse_position[1] = mouse_position[1] - self.y

        self.searchbar.active = False
        if self.searchbar.check_mcollision(mouse_position):
            self.searchbar.active = True
            Globals.cursor_position = len(self.searchbar.text)
            return
        
        nav = self.check_nav_arrow_clicked(mouse_position)
        if nav:
            # navigate_result(tab_view, results_view, nav)
            pass