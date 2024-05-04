import pygame as pyg
import json
pyg.init()

from common.classes.display import Colors, Fonts
from common.classes.globals import Globals
from common.modules.collider import collides_point
from search_engine.classes.results import Result

class SearchView:
    def __init__(self):
        self.search_results = []
        with open("data/search_terms.json", "r") as file:
            self.data = json.load(file)["terms"]

    def draw(self, window, offset):
        x, y = offset
        width, height = Globals.WIDTH/2, Globals.HEIGHT

        pyg.draw.rect(window, Colors.dark_black, (x, y, width, height), border_radius=8)
        pyg.draw.rect(window, Colors.black, (x+2, y+2, width-4, height-4), border_radius=8)

        vertical_offset = 0
        for result in self.search_results:
            vertical_offset = result.draw(window, [x + 10, y + 10 + vertical_offset])

    def update_search(self, criteria={}):
        """Updates the search contents based on the criteria provided"""
        self.search_results = []
        if criteria != {}:
            searched_term = criteria["search"].lower()
            index = -1

            for i in range(len(self.data)):
                if self.data[i]["keyword"].lower() == searched_term:
                    index = i
                    break
            if index != -1:
                # Add before
                for i in range(max(0, index - Globals.MAX_RETURN_NUMBER//2), index):
                    self.search_results += [Result(self.data[i])]

                # Add after
                for i in range(index, min(len(self.data), index + Globals.MAX_RETURN_NUMBER//2 + 1)):
                    self.search_results += [Result(self.data[i])]
                    
        else:
            for i in range(Globals.MAX_RETURN_NUMBER):
                if i == len(self.data):
                    break
                self.search_results += [Result(self.data[i])]

    def check_result_clicked(self):
        """Checks if any of its the view's results were clicked"""
        for result in self.search_results:
            if result.check_mcollision():
                return result