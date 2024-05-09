import contextlib
with contextlib.redirect_stdout(None):
    import pygame as pyg
import json
import os

from common.classes.display import Colors, Fonts
from common.classes.globals import Globals
from search_engine.classes.results import Result
from search_engine.modules.save_handler import FilePaths

class ResultsView:
    def __init__(self):
        self.search_results = []
        
        # Read data from search_terms.json
        if os.path.isfile(FilePaths.terms):
            with open(FilePaths.terms, "r") as file:
                self.data = json.load(file)["terms"]
        else:
            with open(FilePaths.terms, "w") as file:
                file.write(json.dumps({"terms": []}, indent=4))
                self.data = []

    def draw(self, window, offset):
        x, y = offset
        width, height = Globals.WIDTH/2, Globals.HEIGHT

        pyg.draw.rect(window, Colors.dark_black, (x, y, width, height), border_radius=8)
        pyg.draw.rect(window, Colors.black, (x+2, y+2, width-4, height-4), border_radius=8)

        vertical_offset = 0
        for result in self.search_results:
            vertical_offset = result.draw(window, [x + 10, y + 10 + vertical_offset])

        if len(self.search_results) == 0:
            text_width = Fonts.font_30.size("No search results found")[0]
            window.blit(Fonts.font_30.render("No search results found", True, Colors.light_gray), (x + (width - text_width)/2, y + 10))

    def update_search(self, criteria={}):
        """Updates the search contents based on the criteria provided"""
        self.search_results = []
        if criteria != {}:
            searched_term = criteria["keyword"].lower()
            type = criteria["type"]
            length = len(searched_term)
            index = -1
            
            # "Contains" will give the index of the first item that contains the searched term
            # "Strict" will give the index of the first item where the start of the word exactly matches the searched term

            # Find the index of the first item that matches the criteria
            for i in range(len(self.data)):
                if searched_term in self.data[i]["keyword"].lower() and type == "contains":
                    index = i
                    break
                elif searched_term == self.data[i]["keyword"].lower()[:length] and type == "strict":
                    index = i
                    break

            if index != -1:
                # Add before
                for i in range(max(0, index - Globals.MAX_RETURN_NUMBER//2), index):
                    self.search_results += [Result(self.data[i])]

                # Add item
                self.search_results += [Result(self.data[index], True)]

                # Add after
                for i in range(index+1, min(len(self.data), index + Globals.MAX_RETURN_NUMBER//2 + 1)):
                    self.search_results += [Result(self.data[i])] 
        else:
            # Get the first MAX_RETURN_NUMBER items
            for i in range(Globals.MAX_RETURN_NUMBER):
                if i == len(self.data):
                    break
                self.search_results += [Result(self.data[i])]

    def check_result_clicked(self):
        """Checks if any of its the view's results were clicked"""
        for result in self.search_results:
            # Check if a related link was clicked, first
            link = result.check_related_click()
            if link:
                return link
            if result.check_mcollision():
                return result