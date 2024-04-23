import pygame as pyg
import sys
import os

from common.classes.globals import Globals

import search_engine.modules.draw as draw
import search_engine.modules.search_view as search_view

def Main():
    # Initialize window
    pyg.init()
    info_object = pyg.display.Info()
    Globals.WIDTH, Globals.HEIGHT = (1920, 1080)
    Globals.WINDOW_WIDTH, Globals.WINDOW_HEIGHT = info_object.current_w, info_object.current_h
    Globals.WINDOW = pyg.display.set_mode((Globals.WINDOW_WIDTH, Globals.WINDOW_HEIGHT))
    pyg.display.set_caption("Texting App")
    os.system("cls")

    search_view.update_search()

    while True:
        # Get events
        for event in pyg.event.get():
            Globals.mouse_position = pyg.mouse.get_pos()
            if event.type == pyg.QUIT:
                pyg.quit()
                sys.exit()

            elif event.type == pyg.KEYDOWN:
                key = event.key
                mods = pyg.key.get_mods()
                shift, caps, ctrl = mods & pyg.KMOD_SHIFT, mods & pyg.KMOD_CAPS, mods & pyg.KMOD_CTRL

                # Kill key
                if key == pyg.K_F1:
                    pyg.quit()
                    sys.exit()

        draw.draw()
        Globals.clock.tick(Globals.FPS)


if __name__ == "__main__":
    Main()