import pygame as pyg
import json
import os

from common.classes.display import Colors, ColorTheme, Fonts
from common.classes.globals import Globals, FilePaths
from common.classes.buttons import Checkbox, Dropdown, ToolTip
from components.tab_control.tab_components import TabComponentBase


class SettingsView(TabComponentBase):
    def __init__(self, position: tuple, size: tuple):
        super().__init__(position, size)

        self.data = {
            "show_fps": False,
            "save_history": True,
            "confirm_log_delete": True,
            "bible_search": False,
            "color_theme": "Dark"
        }

        if os.path.isfile(FilePaths.settings):
            with open(FilePaths.settings, "r") as file:
                self.data = json.load(file)

        ColorTheme.change_theme(self.data["color_theme"])

        # Settings' tooltips
        fps_tt = ToolTip("Determines whether or not the FPS (Frames per Second) of the application is displayed.", Globals.FPS/2, 550)
        save_ttp = ToolTip("Determines whether or not search queries are saved.", Globals.FPS/2, 550)
        cfld_ttp = ToolTip("Determines whether or not the confirmation popup for the dream log deletion is shown.", Globals.FPS/2, 550)
        bbs_ttp = ToolTip("Determines whether or not the application will try to search for Bible verses.", Globals.FPS/2, 550)

        # Settings
        self.boxes = {
            "show_fps": Checkbox((20, 20, 20, 20), "Show FPS", Fonts.font_20, default_active=self.data["show_fps"], value="show_fps", left_align=True, tooltip=fps_tt),
            "save_history": Checkbox((20, 50, 20, 20), "Save Search History", Fonts.font_20, default_active=self.data["save_history"], value="save_history", left_align=True, tooltip=save_ttp),
            "confirm_log_delete": Checkbox((20, 80, 20, 20), "Show Dream Log Removal Confirmation", Fonts.font_20, default_active=self.data["confirm_log_delete"], value="confirm_log_delete", left_align=True, tooltip=cfld_ttp),
            "bible_search": Checkbox((20, 110, 20, 20), "Allow Bible Searches", Fonts.font_20, default_active=self.data["bible_search"], value="bible_search", left_align=True, tooltip=bbs_ttp),
        }

        self.dropdowns = {
            "color_theme": Dropdown((self.width - 110, 20, 90, 26), Fonts.font_20, ["Dark", "Light"])
        }
        self.dropdowns["color_theme"].selected_option = self.data["color_theme"]

    def draw(self, window: pyg.Surface, mouse_position: list[int]):
        """Draws the settings view component"""
        self.draw_background()

        mouse_position[0] -= self.x
        mouse_position[1] -= self.y

        for box in self.boxes.keys():
            self.boxes[box].draw(self._display_surface)

        text_width, text_height = Fonts.font_20.size("Special thanks to my girlfriend, without whom")
        self._display_surface.blit(Fonts.font_20.render("Special thanks to my girlfriend, without whom", True, Colors.gray), ((self.width - text_width) / 2 + 60, self.height - text_height * 2 - 2))
        text_width = Fonts.font_20.size("I wouldn't have been able to complete this project.")[0]
        self._display_surface.blit(Fonts.font_20.render("I wouldn't have been able to complete this project.", True, Colors.gray), ((self.width - text_width) / 2 + 60, self.height - text_height - 2))

        self._display_surface.blit(Fonts.font_20.render("(c) legolover7", True, Colors.gray), (5, self.height - text_height - 2))

        self._display_surface.blit(Fonts.font_20.render("v" + Globals.VERSION_NUMBER, True, Colors.gray), (5, self.height - text_height * 2 - 2))

        # Draw checkboxes
        for box in self.boxes:
            if self.boxes[box].tooltip != None and self.boxes[box].tooltip.current_delay >= self.boxes[box].tooltip.min_delay:
                self.boxes[box].tooltip.draw(self._display_surface, (self.boxes[box].x, self.boxes[box].y + self.boxes[box].height))


        self._display_surface.blit(Fonts.font_20.render("Color Theme:", True, ColorTheme.current_theme.text_color), (self.width - 250, 22))
        self.dropdowns["color_theme"].draw(self._display_surface, mouse_position)

        window.blit(self._display_surface, (self.x, self.y))

        
    def click(self, mouse_position: list):
        """Simulates a click in the settings view component"""
        mouse_position[0] -= self.x
        mouse_position[1] -= self.y

        for box_key in self.boxes.keys():
            box = self.boxes[box_key]
            if box.check_mcollision(mouse_position):
                box.active = not box.active
                self.data[box.value] = box.active
                return
            
        option = self.dropdowns["color_theme"].click(mouse_position)
        if option and not isinstance(option, bool):
            ColorTheme.change_theme(option)
            self.data["color_theme"] = option
        else:
            # tab_view.views["Dream Log"]
            # .sort_dropdown.active = False
            pass