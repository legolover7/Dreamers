# Import statements
from tkinter import Tk
from tkinter.filedialog import askopenfilename
import pygame as pyg
import pyperclip
import json
import sys
import os

# Custom modules
from common.classes.buttons import Button, Checkbox
from common.classes.display import Colors, Fonts
from common.classes.globals import Globals
from common.classes.input_field import InputField

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
    keyword_input = InputField((600, 150, 400, 30), Fonts.font_20, "Enter Keyword", title="Keyword(s)", title_font=Fonts.font_24)
    page_input = InputField((1100, 150, 220, 30), Fonts.font_20, "Enter Page Number", title="Page Number", title_font=Fonts.font_24)
    description_input = InputField((600, 250, Globals.WIDTH-1200, 30), Fonts.font_20, "Enter Description", title="Description", title_font=Fonts.font_24)
    related_input = InputField((600, 350, Globals.WIDTH-1200, 30), Fonts.font_20, "Enter Terms", title="Related Search Terms", title_font=Fonts.font_24)
    category_input = InputField((600, 450, Globals.WIDTH-1200, 30), Fonts.font_20, "Enter Categories", title="Categories", title_font=Fonts.font_24)
    links_input = InputField((600, 550, Globals.WIDTH-1200, 30), Fonts.font_20, "Enter Links", title="Links to Definition of", title_font=Fonts.font_24)
    ref_input = InputField((600, 650, Globals.WIDTH-1200, 30), Fonts.font_20, "Enter References", title="References", title_font=Fonts.font_24)

    verb_box = Checkbox((650, 710, 20, 20), "Verb", Fonts.font_20)
    noun_box = Checkbox((750, 710, 20, 20), "Noun", Fonts.font_20)
    adjective_box = Checkbox((900, 710, 20, 20), "Adjective", Fonts.font_20)

    save_button = Button((Globals.WIDTH/2-100, Globals.HEIGHT-100, 200, 40), Colors.blue, "Save", Fonts.font_24, Colors.white)
    merge_button = Button((20, 20, 150, 30), Colors.aqua, "Merge Files", Fonts.font_24, Colors.black)

    fields = [keyword_input, page_input, description_input, related_input, category_input, links_input, ref_input]
    boxes = [verb_box, noun_box, adjective_box]
    buttons = [save_button, merge_button]
    active_field = None
    error_message = ""
    error_timeout = 0
    index = -1

    while True:
        text_lines = chunk_text.chunk(description_input.text, content_width=description_input.width-5, char_width=description_input.font.size("A")[0])
        desc_offset = max(10, (len(text_lines)-1) * description_input.font.size("A")[1] + 10)

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

                elif key == pyg.K_RETURN:
                    # Save fields to file
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
                    if shift:
                        index = max(0, index - 1)

                    else:
                        index = min(index + 1, len(fields) - 1)

                    active_field = fields[index]

                elif key == pyg.K_v and ctrl and active_field != None:
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
                    if i > 2:
                        if fields[i].check_mcollision(desc_offset):
                            active_field = fields[i]
                            Globals.cursor_position = len(fields[i].text)
                            Globals.cursor_frame = 0
                            index = i
                            break
                    else:
                        if fields[i].check_mcollision():
                            active_field = fields[i]
                            Globals.cursor_position = len(fields[i].text)
                            Globals.cursor_frame = 0
                            index = i
                            break

                for box in boxes:
                    if box.check_mcollision(desc_offset):
                        box.active = not box.active

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
                    outdata = {}
                    with open("data/search_terms.json", "r") as outfile, open(filename, "r") as infile:
                        outdata = json.load(outfile)
                        indata = json.load(infile)
                        for item in indata["terms"]:
                            if item not in outdata["terms"]:
                                outdata["terms"] += [item]

                    with open("data/search_terms.json", "w") as file:
                        file.write(json.dumps(outdata, indent=4))              
                        
        Globals.cursor_frame = min(Globals.cursor_timeout * Globals.FPS + 1, Globals.cursor_frame + 1)
        error_timeout = max(0, error_timeout - 1)

        draw.draw(fields, boxes, buttons, active_field, desc_offset, error_message, error_timeout)
        Globals.clock.tick(Globals.FPS)

def SaveWord(fields, boxes):
    keyword_input, page_input, description_input, related_input, category_input, links_input, ref_input = fields
    verb_box, noun_box, adjective_box = boxes

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