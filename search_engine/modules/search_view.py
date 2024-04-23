import pygame as pyg
import json
pyg.init()

from common.classes.display import Colors, Fonts
from common.classes.globals import Globals
from common.modules.collider import collides_point

class Result:
    def __init__(self, data):
        self.data = data
        self.height = 0
        self.related_links = []
        self.generated_links = False

    def draw(self, window, offset):
        keyword, description, related = get_data(self.data)
        start_offset = offset[1]

        if collides_point(Globals.mouse_position, (offset[0]-8, offset[1], Globals.WIDTH/2-6, self.height)):
            pyg.draw.rect(window, Colors.light_gray, (offset[0]-8, offset[1], Globals.WIDTH/2-6, self.height), border_radius=8)

        text_height = Fonts.font_30.size(keyword)[1]
        window.blit(Fonts.font_30.render(keyword, True, Colors.white), offset)
        offset[1] += text_height

        text_height = Fonts.font_20.size(keyword)[1]
        window.blit(Fonts.font_20.render(description, True, Colors.dark_white), offset)
        offset[1] += text_height

        if len(related) > 0:
            hori_offset, text_height = Fonts.font_18.size("Related terms: ")
            window.blit(Fonts.font_18.render("Related terms:", True, Colors.dark_white), offset)
            
            for rel in related:
                # Separating terms by commas
                comma = ", " if related.index(rel) < len(related) - 1 else ""
                text_width, text_height = Fonts.font_18.size(rel)
                # Creating link buttons
                if not self.generated_links:
                    self.related_links += [{
                        "rect": (offset[0] + hori_offset, offset[1], text_width, text_height),
                        "term": rel
                    }]

                color = Colors.light_blue if collides_point(Globals.mouse_position, (offset[0] + hori_offset, offset[1], text_width, text_height)) else Colors.dark_white
                # Draw text
                window.blit(Fonts.font_18.render(rel, True, color), (offset[0] + hori_offset, offset[1]))
                window.blit(Fonts.font_18.render(comma, True, Colors.dark_white), (offset[0] + hori_offset + Fonts.font_18.size(rel)[0], offset[1]))
                hori_offset += text_width + Fonts.font_18.size(", ")[0]
                
            
            offset[1] += text_height

        self.height = offset[1] - start_offset
        return offset[1] + 5

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


def get_data(result):
    keyword = result["keyword"]
    description = result["description"]
    related = result["related_terms"]

    return keyword, description, related

def update_search(criteria={}):
    global data
    global search_results

    search_results = []
    if criteria != {}:
        searched_term = criteria["search"]
        index = -1

        for i in range(len(data)):
            if data[i]["keyword"] == searched_term:
                index = i
                break
        if index != -1:
            # Add before
            for i in range()
    
    else:
        for i in range(Globals.MAX_RETURN_NUMBER):
            if i == len(data):
                break
            search_results += [Result(data[i])]
