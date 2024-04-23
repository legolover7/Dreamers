import pygame as pyg
import json
pyg.init()

from common.classes.display import Colors, Fonts
from common.classes.globals import Globals
from common.modules.collider import collides_point
from search_engine.classes.results import Result

search_results = []

with open("data/search_terms.json", "r") as file:
    data = json.load(file)["terms"]

def draw(window, offset):
    global search_results
    x, y = offset
    width, height = Globals.WIDTH/2, Globals.HEIGHT

    pyg.draw.rect(window, Colors.dark_black, (x, y, width, height), border_radius=8)
    pyg.draw.rect(window, Colors.black, (x+2, y+2, width-4, height-4), border_radius=8)

    vertical_offset = 0
    for result in search_results:
        vertical_offset = result.draw(window, [x + 10, y + 10 + vertical_offset])


def update_search(criteria={}):
    global data
    global search_results

    search_results = []
    if criteria != {}:
        searched_term = criteria["search"].lower()
        index = -1

        for i in range(len(data)):
            if data[i]["keyword"].lower() == searched_term:
                index = i
                break
        if index != -1:
            # Add before
            for i in range(max(0, index - Globals.MAX_RETURN_NUMBER//2), index):
                search_results += [Result(data[i])]

            # Add after
            for i in range(index, min(len(data), index + Globals.MAX_RETURN_NUMBER//2 + 1)):
                search_results += [Result(data[i])]
                
    else:
        for i in range(Globals.MAX_RETURN_NUMBER):
            if i == len(data):
                break
            search_results += [Result(data[i])]
