import contextlib
with contextlib.redirect_stdout(None):
    import pygame as pyg

from common.classes.display import Colors, Fonts
from common.classes.globals import Globals

from common.classes.buttons import Button
from components.tab_control.tab_components import *
from common.classes.popup import Popup

from components.tab_control.definition_view import DefinitionView
from components.tab_control.dream_log_view import DreamLogView
from components.tab_control.search_view import SearchView
from components.tab_control.settings_view import SettingsView

class TabContainer:
    """Container for all of the different tab views
    
    Attributes:
        x, y: Position of this object
        width, height: Size of this object
        _display_surface: Screen that this object's components are drawn to
        current_search: The currently selected search, for definition view
        tabs: The tab icons for navigating the different views
        view: The currently selected view
        popup: Used for confirmation of dream log deletion
    """
    def __init__(self, position: tuple, size: tuple, tabs: list[Tab]):
        """Initializes the tab view with its available tabs/options"""
        self.x, self.y = position
        self.width, self.height = size
        self._display_surface = pyg.Surface(size)

        self.current_search = None
        self.tabs = tabs
        self.view = tabs[0].text
        tabs[0].active = True
        self.popup = Popup((self.width/2 - 200, self.height/2 - 90, 400, 180), "Are you sure you want to remove this dream log?", 60)

        # Tabcontainer components
        component_position = 0, 30
        component_size = Globals.WIDTH/2 - 50, Globals.HEIGHT - 30

        self.views = {
            "Search": SearchView(component_position, component_size),
            "Definition": DefinitionView(component_position, component_size),
            "Settings": SettingsView(component_position, component_size),
            "Dream Log": DreamLogView(component_position, component_size)
        }

    def draw(self, window: pyg.Surface, mouse_position: list):
        """Draws the current tab view: search tab, description, etc."""
        # Draw background
        pyg.draw.rect(self._display_surface, ColorTheme.current_theme.field_background_color, (0, 0, self.width, self.height), border_radius=8)
        pyg.draw.rect(self._display_surface, ColorTheme.current_theme.background_color, (2, 2, self.width - 4, self.height - 4), border_radius=8)
        pyg.draw.rect(self._display_surface, ColorTheme.current_theme.field_background_color, (0, 30, self.width, 4))

        # Calculate relative mouse position
        relative_mouse_position = copy.deepcopy(mouse_position)
        relative_mouse_position[0] -= self.x
        relative_mouse_position[1] -= self.y

        # Draw tab buttons
        for tab in self.tabs:
            tab.draw(self._display_surface, relative_mouse_position)

        self.views[self.view].draw(self._display_surface, relative_mouse_position)
            
        if self.views["Dream Log"].popup_displayed:
            self.popup.draw(self._display_surface, relative_mouse_position)

        window.blit(self._display_surface, (self.x, self.y))

    def update_view(self, option):
        """Selects one of this object's tabs based on the option provided"""
        self.view = option
        for tab in self.tabs:
            tab.active = False
            if tab.text == option:
                tab.active = True

        # Reset active fields
        self.views["Search"].searchbar.active = False
        self.views["Dream Log"].dream_input.active = False

    def check_mcollision(self, point):
        return collider.collides_point(point, (self.x, self.y, self.width, self.height))