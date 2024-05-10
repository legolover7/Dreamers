# Import statements
from tkinter import Tk
from tkinter.filedialog import askopenfilename
import contextlib
with contextlib.redirect_stdout(None):
    import pygame as pyg
try:
    import pyperclip
    paste_enabled = True
except ModuleNotFoundError:
    paste_enabled = False
    
import json
import sys
import os

# Custom modules
from common.classes.buttons import Button, Checkbox
from common.classes.display import Colors, Fonts
from common.classes.globals import Globals, FilePaths
from common.classes.input_field import *

import common.modules.typing_handler as typing_handler
import common.modules.chunk_text as chunk_text
import editor.modules.draw as draw

def Main():
    # Initialize window
    pyg.init()
    info_object = pyg.display.Info()
    Globals.WIDTH, Globals.HEIGHT = (1920, 1080)
    Globals.WINDOW_WIDTH, Globals.WINDOW_HEIGHT = info_object.current_w, info_object.current_h
    Globals.WINDOW = pyg.display.set_mode((Globals.WINDOW_WIDTH, Globals.WINDOW_HEIGHT))
    pyg.display.set_caption("Texting App")
    os.system("cls")

    # Various buttons and fields
    keyword_input     = IFBlock((600, 150, 400, 30),                 "Enter Keyword",          Fonts.font_20)
    page_input        = IFBlock((1100, 150, 220, 30),                "Enter Page Number",      Fonts.font_20)
    description_input = IFBlock((600, 200, Globals.WIDTH-1200, 230), "Enter Description",      Fonts.font_20)
    related_input     = IFBlock((600, 450, Globals.WIDTH-1200, 30),  "Enter Related Terms",    Fonts.font_20)
    category_input    = IFBlock((600, 500, Globals.WIDTH-1200, 30),  "Enter Categories",       Fonts.font_20)
    links_input       = IFBlock((600, 550, Globals.WIDTH-1200, 30),  "Enter Definition Links", Fonts.font_20)
    ref_input         = IFBlock((600, 600, Globals.WIDTH-1200, 30),  "Enter References",       Fonts.font_20)

    verb_box = Checkbox((650, 650, 20, 20), "Verb", Fonts.font_20)
    noun_box = Checkbox((750, 650, 20, 20), "Noun", Fonts.font_20)
    adjective_box = Checkbox((900, 650, 20, 20), "Adjective", Fonts.font_20)
    name_box = Checkbox((1050, 650, 20, 20), "Name/Place", Fonts.font_20)

    save_button = Button((Globals.WIDTH/2-100, Globals.HEIGHT-100, 200, 40), Colors.blue, "Save", Fonts.font_24, Colors.white)
    merge_button = Button((20, 20, 150, 30), Colors.aqua, "Merge Files", Fonts.font_24, Colors.black)

    fields = [keyword_input, page_input, description_input, related_input, category_input, links_input, ref_input]
    boxes = [verb_box, noun_box, adjective_box, name_box]
    buttons = [save_button, merge_button]
    active_field = None
    error_message = ""
    error_timeout = 0
    index = 0

    # Make sure term file exists
    if not os.path.isfile(FilePaths.terms):
        with open(FilePaths.terms, "w") as file:
            file.write(json.dumps({"terms": []}, indent=4))

    while True:
        for event in pyg.event.get():
            Globals.mouse_position[0] = pyg.mouse.get_pos()[0] * (Globals.WIDTH / Globals.WINDOW_WIDTH)
            Globals.mouse_position[1] = pyg.mouse.get_pos()[1] * (Globals.HEIGHT / Globals.WINDOW_HEIGHT)
            if event.type == pyg.QUIT:
                pyg.quit()
                sys.exit()

            elif event.type == pyg.KEYDOWN:
                key = event.key
                mods = pyg.key.get_mods()
                shift, caps, ctrl = mods & pyg.KMOD_SHIFT, mods & pyg.KMOD_CAPS, mods & pyg.KMOD_CTRL

                if key == pyg.K_F1:
                    pyg.quit()
                    sys.exit()

                elif key == pyg.K_ESCAPE:
                    active_field = None

                # Save fields to file
                elif key == pyg.K_RETURN:
                    response = SaveWord(fields, boxes)
                    if response == "Saved":
                        for field in fields:
                            field.text = ""
                        for box in boxes:
                            box.active = False
                        active_field = None
                        error_message = ""
                    else:
                        error_message = response
                        error_timeout = Globals.FPS * 3

                elif key == pyg.K_TAB:
                    Globals.cursor_frame = 0
                    fields[index].active = False
                    if shift: index = max(0, index - 1)
                    else: index = min(index + 1, len(fields) - 1)

                    fields[index].active = True

                elif key == pyg.K_v and ctrl and active_field != None and paste_enabled:
                    active_field.text = pyperclip.paste()
                    Globals.cursor_position = len(active_field.text)
                else:
                    if active_field != None:
                        active_field.text, Globals.cursor_position = typing_handler.handler(active_field.text, key, (shift, caps, ctrl), Globals.cursor_position)
                        Globals.cursor_frame = 0
                        

            elif event.type == pyg.MOUSEBUTTONDOWN and event.button == 1:
                active_field = None
                
                # Select a field
                for i in range(len(fields)):
                    fields[i].active = False
                    if fields[i].check_mcollision():
                        fields[i].active = True
                        Globals.cursor_position = len(fields[i].text)
                        Globals.cursor_frame = 0
                        index = i
                        break

                for box in boxes:
                    if box.check_mcollision():
                        box.active = not box.active

                for field in fields:
                    if field.active:
                        active_field = field

                # Save fields to file
                if save_button.check_mcollision():
                    response = SaveWord(fields, boxes)
                    if response == "Saved":
                        for field in fields:
                            field.text = ""
                        for box in boxes:
                            box.active = False
                        active_field = None
                        error_message = ""
                    else:
                        error_message = response
                        error_timeout = Globals.FPS * 3

                # Merge data files
                if merge_button.check_mcollision():
                    filename = askopenfilename()
                    if filename:
                        outdata = {}
                        write = True
                        with open(FilePaths.terms, "r") as outfile, open(filename, "r") as infile:
                            outdata = json.load(outfile)
                            try:
                                indata = json.load(infile)
                                for item in indata["terms"]:
                                    if item not in outdata["terms"]:
                                        outdata["terms"] += [item]
                            except (UnicodeDecodeError, json.decoder.JSONDecodeError):
                                write = False

                        # Don't write if the read operation failed
                        if write:
                            with open(FilePaths.terms, "w") as file:
                                file.write(json.dumps(outdata, indent=4))
                        
        Globals.cursor_frame = min(Globals.cursor_timeout * Globals.FPS + 1, Globals.cursor_frame + 1)
        error_timeout = max(0, error_timeout - 1)

        draw.draw(fields, boxes, buttons, error_message, error_timeout)
        Globals.clock.tick(Globals.FPS)

def SaveWord(fields, boxes):
    keyword_input, page_input, description_input, related_input, category_input, links_input, ref_input = fields
    verb_box, noun_box, adjective_box, name_box = boxes

    if keyword_input.text == "":
        return "No keyword"

    # Split certain fields into a list
    related = related_input.text.split(",") if related_input.text != "" else []
    categories = category_input.text.split(",") if category_input.text != "" else []
    links = links_input.text.split(",") if links_input.text != "" else []
    references = ref_input.text.split(",") if ref_input.text != "" else []

    for i in range(len(related)):
        related[i] = related[i].strip()

    for i in range(len(categories)):
        categories[i] = categories[i].strip()

    for i in range(len(links)):
        links[i] = links[i].strip()

    for i in range(len(references)):
        references[i] = references[i].strip()

    object = {
        "keyword": keyword_input.text,
        "page_number": page_input.text,
        "description": description_input.text,
        "related_terms": related,
        "categories": categories,
        "links": links,
        "references": references,
        "is_verb": verb_box.active,
        "is_noun": noun_box.active,
        "is_adjective": adjective_box.active,
        "is_name": name_box.active,
    }

    data = ""
    with open("data/search_terms.json", "r") as file:
        data = json.load(file)
        data["terms"] += [object]

    with open("data/search_terms.json", "w") as file:
        file.write(json.dumps(data, indent=4))

    return "Saved"

if __name__ == "__main__":
    Main()