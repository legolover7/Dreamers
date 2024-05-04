import pygame as pyg
import copy

from common.classes.display import Colors, Fonts
from common.classes.globals import Globals

from common.classes.buttons import Button
from components.tab_control.tab_components import Tab, DefinitionView

class TabContainer:
    def __init__(self, tabs: list[Tab]):
        """Initializes the tab view with its available tabs/options"""
        self.current_search = None
        self.tabs = tabs
        self.view = tabs[0].text
        tabs[0].active = True
        self.clear_search_button = None

        # Tabcontainer components
        self.definition_view = DefinitionView()

    def draw(self, window, offset):
        """Draws the current tab view: search tab, description, etc."""
        x, y = offset
        width, height = Globals.WIDTH-x, Globals.HEIGHT
        
        if self.definition_view.clear_search_button == None:
            self.definition_view.clear_search_button = Button((x + width/2 - 100, Globals.HEIGHT - 50, 200, 40), Colors.red, "Clear Result", Fonts.font_20, Colors.white)

        # Draw background
        pyg.draw.rect(window, Colors.dark_black, (x, y, width, height), border_radius=8)
        pyg.draw.rect(window, Colors.black, (x+2, y+2, width-4, height-4), border_radius=8)
        pyg.draw.rect(window, Colors.dark_black, (x, y + 30, width, 4))

        # Draw tab buttons
        for tab in self.tabs:
            tab.draw(window)

        # Draw current view
        if self.view == "Definition" and self.current_search != None:
            self.definition_view.draw(window, (x, y), self.current_search)

        elif self.view == "Definition":
            text_width = Fonts.font_30.size("No result selected")[0]
            window.blit(Fonts.font_30.render("No result selected", True, Colors.white), (x + (width - text_width)/2, y + 70))

    def update_view(self, option):
        """Selects one of this object's tabs based on the option provided"""
        self.view = option
        for tab in self.tabs:
            tab.active = False
            if tab.text == option:
                tab.active = True