import pygame as pyg
import datetime
import json
import time
import os

from common.classes.buttons import Button, Dropdown
from common.classes.display import Colors, ColorTheme, Fonts
from common.classes.globals import Globals
from common.classes.input_field import IFBlock, IFBox, DateInput
from common.classes.globals import FilePaths
from common.classes.list_container import ListContainer, ListContent
from components.tab_control.tab_components import TabComponentBase

class DreamLogView(TabComponentBase):
    def __init__(self, position: tuple, size: tuple):
        super().__init__(position, size)
        self.popup_displayed = False
        self.confirm_delete = False

        # Fields/buttons
        self.dream_input = IFBlock((20, 20, self.width - 40, self.height / 2 - 100), "Enter dream", Fonts.font_24)
        self.dream_title = IFBox((20, self.height / 2 - 60, 400, 30), "Enter title", Fonts.font_20, max_length=-1)
        self.date_input = DateInput((450, self.height / 2 - 60, 200, 30), "MM/DD/YYYY")
        self.save_button = Button((665, self.height / 2 - 65, 100, 40), Colors.green, "Save", Fonts.font_20, Colors.white)
        self.delete_button = Button((780, self.height / 2 - 65, 100, 40), Colors.red, "Remove", Fonts.font_20, Colors.white)

        # Filter drowdown
        self.sort_dropdown = Dropdown((440, self.height/2, 180, 25), Fonts.font_18, ["Select a filter", "Date Modified", "Date Dreamt", "Alpha (A-Z)", "Alpha (Z-A)"])
        
        self.list_container = ListContainer((20, self.height / 2 + 30, self.width * 0.66, self.height / 2 - 40), [])
        self.term_container = ListContainer((self.width * 0.7, self.height / 2 + 30, self.width * 0.25, self.height / 2 - 40), [])

        # Get saved dreams
        if os.path.isfile(FilePaths.logs):
            with open(FilePaths.logs, "r") as infile:
                data = json.load(infile)["dreams"]
                for log in data:
                    self.list_container.contents.append(ListContent(log["title"], log["date_dreamed"], log["date_modified"], log["data"]))

    def draw(self, window: pyg.Surface, mouse_position: list[int]):
        self.draw_background()

        # Calculate relative mouse position
        mouse_position[0] = mouse_position[0] - self.x
        mouse_position[1] = mouse_position[1] - self.y

        self.dream_input.draw(self._display_surface,)
        self.dream_title.draw(self._display_surface)
        self.date_input.draw(self._display_surface)
        self.save_button.draw(self._display_surface, mouse_position)
        self.delete_button.draw(self._display_surface, mouse_position)
        self.list_container.draw(self._display_surface, mouse_position)
        self.sort_dropdown.draw(self._display_surface, mouse_position)

        self._display_surface.blit(Fonts.font_24.render("Saved Dreams:", True, ColorTheme.current_theme.text_color), (20, self.height / 2))

        if len(self.term_container.contents) > 0:
            self.term_container.draw(self._display_surface)
            self._display_surface.blit(Fonts.font_24.render("Current Terms:", True, ColorTheme.current_theme.text_color), (self.width * 0.7, self.height / 2))

        window.blit(self._display_surface, (self.x, self.y))
    
    def save_dream(self):
        """Saves the text in the input fields into a list content object"""
        if self.dream_input.text.strip() != "" and self.dream_title.text.strip() != "" and len(self.date_input.text) == 8:
            current_date = time.strftime("%m/%d/%Y")
            temp = ""
            date_dreamt = self.date_input.text
            for chunk in self.date_input.format.split("/")[:-1]:
                temp += date_dreamt[:len(chunk)] + "/"
                date_dreamt = date_dreamt[len(chunk):]
            temp += date_dreamt
            # Check if the title already exists
            for item in self.list_container.contents:
                if item.title == self.dream_title.text:
                    item.data = self.dream_input.text
                    item.date_modified = current_date
                    item.date_dreamt = temp
                    return
            self.list_container.contents.append(ListContent(self.dream_title.text, temp, current_date, self.dream_input.text))
            return True

    def sort_dreams(self, option):
        """Sorts the saved dreams based on the option provided"""
        if option == "Alpha (A-Z)":
            self.list_container.contents.sort(key=lambda dream: dream.title)

        elif option == "Alpha (Z-A)":
            self.list_container.contents.sort(reverse=True, key=lambda dream: dream.title)

        elif option == "Date Modified":
            self.list_container.contents.sort(key=lambda dream: datetime.datetime.strptime(dream.date_modified, "%m/%d/%Y"))

        elif option == "Date Dreamt":
            self.list_container.contents.sort(key=lambda dream: datetime.datetime.strptime(dream.date_dreamt, "%m/%d/%Y"))


    def click(self, position: list):
        """Simulates a click in the dream log view component"""
        position[0] = position[0] - self.x
        position[1] = position[1] - self.y

        self.dream_input.active = False
        self.dream_title.active = False
        self.date_input.active = False

        # Filter dropdown
        option = self.sort_dropdown.click(position)
        if option:
            if not isinstance(option, bool):
                self.sort_dreams(option)
            return
        else:
            self.sort_dropdown.active = False

        # Dream log inputs
        if self.dream_input.check_mcollision(position):
            self.dream_input.active = True
            Globals.cursor_position = len(self.dream_input.text)
            return
        elif self.dream_title.check_mcollision(position):
            self.dream_title.active = True
            Globals.cursor_position = len(self.dream_title.text)
            return
        elif self.date_input.check_mcollision(position):
            self.date_input.active = True
            Globals.cursor_position = len(self.date_input.text)
            return
            
        # Dream log save button
        elif self.save_button.check_mcollision(position):
                result = self.save_dream()
                if result:
                    self.dream_input.text = ""
                    self.dream_title.text = ""
                    self.date_input.text = ""
                return

        # Dream log remove button
        elif self.delete_button.check_mcollision(position) and self.dream_title.text != "":
            if self.confirm_delete:
                self.popup_displayed = True
                return
            else:
                # Remove the log from the list
                for log in self.list_container.contents:
                    if log.title == self.dream_title.text:
                        self.list_container.contents.remove(log)

                # Reset fields
                self.dream_input.text = ""
                self.dream_title.text = ""
                self.date_input.text = ""
                return

        # List container
        item = self.list_container.check_click(position)
        if item:
            self.dream_input.text = item.data
            self.dream_title.text = item.title
            self.date_input.text = "".join(item.date_dreamt.split("/"))
            self.date_input.cursor_position = 8
            return