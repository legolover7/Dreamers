import contextlib
with contextlib.redirect_stdout(None):
    import pygame as pyg

from common.classes.display import Colors, Fonts
from common.classes.globals import Globals

from common.classes.buttons import Button
from components.tab_control.tab_components import *
from common.classes.popup import Popup

class TabContainer:
    def __init__(self, tabs: list[Tab]):
        """Initializes the tab view with its available tabs/options"""
        self.current_search = None
        self.tabs = tabs
        self.view = tabs[0].text
        tabs[0].active = True
        self.clear_search_button = None
        self.popup = None

        # Tabcontainer components
        self.definition_view = DefinitionView()
        self.search_view = SearchView((Globals.WIDTH/2 + 50, 50))
        self.settings_view = SettingsView((Globals.WIDTH/2 + 50, 50))
        self.dream_log_view = DreamLogView((Globals.WIDTH/2 + 50, 50))

    def draw(self, window, offset):
        """Draws the current tab view: search tab, description, etc."""
        x, y = offset
        width, height = Globals.WIDTH-x, Globals.HEIGHT
        if self.popup == None:
            self.popup = Popup((x + width/2 - 200, y + height/2 - 90, 400, 180), "Are you sure you want to remove this dream log?", 60)

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
        if self.view == "Definition":
            if self.current_search != None:
                self.definition_view.draw(window, (x, y), self.current_search)
            else:
                text_width = Fonts.font_30.size("No result selected")[0]
                window.blit(Fonts.font_30.render("No result selected", True, Colors.white), (x + (width - text_width)/2, y + 70))

        elif self.view == "Search":
            self.search_view.draw(window)

        elif self.view == "Settings":
            self.settings_view.draw(window)

        elif self.view == "Dream Log":
            self.dream_log_view.draw(window)
            
        if self.popup.displayed:
            self.popup.draw(window)

    def update_view(self, option):
        """Selects one of this object's tabs based on the option provided"""
        self.view = option
        for tab in self.tabs:
            tab.active = False
            if tab.text == option:
                tab.active = True

        # Reset active fields
        self.search_view.searchbar.active = False
        self.dream_log_view.dream_input.active = False
