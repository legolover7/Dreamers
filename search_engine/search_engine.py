import pygame as pyg
import sys
import os

from common.classes.display import Colors, Fonts
from common.classes.globals import Globals
from common.modules.profiler import Profiler

import search_engine.modules.draw as draw
from search_engine.modules.search_view import SearchView
from components.tab_control.tab_container import TabContainer
from components.tab_control.tab_components import Tab

def Main():
    # Initialize window
    pyg.init()
    info_object = pyg.display.Info()
    Globals.WIDTH, Globals.HEIGHT = (1920, 1080)
    Globals.WINDOW_WIDTH, Globals.WINDOW_HEIGHT = info_object.current_w, info_object.current_h
    Globals.WINDOW = pyg.display.set_mode((Globals.WINDOW_WIDTH, Globals.WINDOW_HEIGHT))
    pyg.display.set_caption("Texting App")
    os.system("cls")

    search_view = SearchView()
    search_view.update_search()

    profiler = Profiler(Globals.FPS, (Globals.WIDTH - 30, 4), Fonts.font_20, Colors.white)
    
    tab_view = TabContainer([Tab((Globals.WIDTH/2+52, 0, 75, 30), "Search"), Tab((Globals.WIDTH/2+125, 0, 120, 30), "Definition")])

    while True:
        profiler.calc_frame()

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

                if key == pyg.K_F9:
                    profiler.display = not profiler.display

            elif event.type == pyg.MOUSEBUTTONDOWN and event.button == 1:
                for tab in tab_view.tabs:
                    if tab.check_mcollision():
                        tab_view.update_view(tab.text)

                # Check for a result that was clicked on
                result = search_view.check_result_clicked()
                if result is not None:
                    tab_view.current_search = result
                    tab_view.update_view("Definition")

                # Check for the "Clear result" button in the description tab
                if tab_view.view == "Definition" and tab_view.definition_view.clear_search_button.check_mcollision():
                    tab_view.current_search = None

        draw.draw(search_view, tab_view, profiler)
        Globals.clock.tick(Globals.FPS)


if __name__ == "__main__":
    Main()