import pygame as pyg
import sys
import os

from common.classes.display import Colors, Fonts
from common.classes.globals import Globals
from common.modules.profiler import Profiler
from common.modules.typing_handler import handler

import search_engine.modules.draw as draw
from search_engine.modules.result_view import ResultsView
from components.tab_control.tab_container import TabContainer
from components.tab_control.tab_components import Tab, TabBar

def Main():
    # Initialize window
    pyg.init()
    info_object = pyg.display.Info()
    Globals.WIDTH, Globals.HEIGHT = (1920, 1080)
    Globals.WINDOW_WIDTH, Globals.WINDOW_HEIGHT = info_object.current_w, info_object.current_h
    Globals.WINDOW = pyg.display.set_mode((Globals.WINDOW_WIDTH, Globals.WINDOW_HEIGHT))
    pyg.display.set_caption("Texting App")
    os.system("cls")

    results_view = ResultsView()
    results_view.update_search()

    profiler = Profiler(Globals.FPS, (Globals.WIDTH - 30, 4), Fonts.font_20, Colors.white)
    
    tab_view = TabContainer([Tab((Globals.WIDTH/2+52, 0, 75, 30), "Search"), Tab((Globals.WIDTH/2+125, 0, 120, 30), "Definition")])
    tab_bar = TabBar()

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

                elif key == pyg.K_RETURN and tab_view.view == "Search":
                    search = tab_view.search_view.searchbar.text
                    if search != "":
                        tab_view.search_view.searchbar.text = ""
                        tab_view.search_view.history.append(search)
                        Globals.cursor_position = 0
                        results_view.update_search({"keyword": search, "type": "contains"})

                else:
                    if tab_view.search_view.searchbar.active and not (key == pyg.K_SPACE and tab_view.search_view.searchbar.text == ""):
                        tab_view.search_view.searchbar.text, Globals.cursor_position = handler(tab_view.search_view.searchbar.text, key, (shift, caps, ctrl), Globals.cursor_position)

            elif event.type == pyg.MOUSEBUTTONDOWN and event.button == 1:
                tab_view.search_view.searchbar.active = False
                # Check for the different tabs for the tab view (right half)
                for tab in tab_view.tabs:
                    if tab.check_mcollision():
                        tab_view.update_view(tab.text)

                # Check for a result that was clicked on
                result = results_view.check_result_clicked()
                if result is not None:
                    tab_view.current_search = result
                    tab_view.update_view("Definition")
                    
                # Check for the different tabs for the tabbar (leftmost size)
                index = tab_bar.check_mcollision()
                if index != None:
                    results_view.update_search({"keyword": "ABCDEFGHIJKLMNOPQRSTUVWXYZ"[index], "type": "strict"})

                index = tab_view.search_view.check_history_clicked()
                if index != None:
                    results_view.update_search({"keyword": tab_view.search_view.history[index], "type": "strict"})

                # Check for the "Clear result" button in the description tab
                if tab_view.view == "Definition" and tab_view.definition_view.clear_search_button.check_mcollision():
                    tab_view.current_search = None

                # Check for search's searchbar
                elif tab_view.view == "Search" and tab_view.search_view.searchbar.check_mcollision():
                    tab_view.search_view.searchbar.active = True
                    Globals.cursor_position = len(tab_view.search_view.searchbar.text)

        draw.draw(results_view, tab_view, tab_bar, profiler)
        Globals.clock.tick(Globals.FPS)


if __name__ == "__main__":
    Main()