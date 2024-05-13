import contextlib
with contextlib.redirect_stdout(None):
    import pygame as pyg
import requests
import sys
import os

# Common classes
from common.classes.display import Colors, Fonts, ColorTheme
from common.classes.globals import Globals
from components.utilities.profiler import Profiler
# Specific classes
from search_engine.classes.results import Result
from search_engine.modules.result_view import ResultsView
# Components
from components.tab_control.tab_container import TabContainer
from components.tab_control.tab_components import Tab, TabBar
from components.tab_control.search_view import SearchView
from components.tab_control.definition_view import DefinitionView
from components.tab_control.dream_log_view import DreamLogView
from components.tab_control.settings_view import SettingsView
# Modules
import search_engine.modules.event_handlers as ev_handlers
import search_engine.modules.draw as draw
import search_engine.modules.save_handler as s_handler

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

    profiler = Profiler(Globals.FPS, (Globals.WIDTH - 30, Globals.HEIGHT - 22), Fonts.font_20, Colors.white)
    
    tab_view = TabContainer(
        (Globals.WIDTH/2 + 50, 0), (Globals.WIDTH/2 - 50, Globals.HEIGHT),
        [Tab((2, 0, 75, 30), "Search"), Tab((75, 0, 120, 30), "Definition"), 
         Tab((193, 0, 110, 30), "Dream Log"), Tab((301, 0, 100, 30), "Settings")
    ])
    tab_bar = TabBar()

    # Unpack tab view objects
    search_view:     SearchView     = tab_view.views["Search"]
    definition_view: DefinitionView = tab_view.views["Definition"]
    dream_log_view:  DreamLogView   = tab_view.views["Dream Log"]
    settings_view:   SettingsView   = tab_view.views["Settings"]

    while True:
        profiler.calc_frame()
        profiler.display = settings_view.boxes["show_fps"].active
        dream_log_view.confirm_delete = settings_view.boxes["confirm_log_delete"].active

        # Get events
        for event in pyg.event.get():
            Globals.mouse_position[0] = pyg.mouse.get_pos()[0] * (Globals.WIDTH / Globals.WINDOW_WIDTH)
            Globals.mouse_position[1] = pyg.mouse.get_pos()[1] * (Globals.HEIGHT / Globals.WINDOW_HEIGHT)
            if event.type == pyg.QUIT:
                Quit(tab_view)

            elif event.type == pyg.KEYDOWN:
                key = event.key
                mods = pyg.key.get_mods()
                shift, caps, ctrl = mods & pyg.KMOD_SHIFT, mods & pyg.KMOD_CAPS, mods & pyg.KMOD_CTRL

                if key == pyg.K_F1:
                    Quit(tab_view)

                if key == pyg.K_F9:
                    settings_view.boxes["show_fps"].active = not tab_view.settings_view.boxes["show_fps"].active

                elif key == pyg.K_RETURN and tab_view.view == "Search":
                    search = search_view.searchbar.text
                    # Search for item and save it to history (if active)
                    if search != "":
                        definition_view.split_semis = True
                        search_view.searchbar.text = ""
                        if settings_view.boxes["save_history"].active:
                            search_view.history.append(search)
                        Globals.cursor_position = 0
                        results_view.update_search({"keyword": search, "type": "contains"})
                        search_view.search_index = 0

                        # Search for bible verses
                        if len(results_view.search_results) == 0 and settings_view.boxes["bible_search"].active:
                            response = requests.get("https://labs.bible.org/api/?passage=" + search + "&formatting=plain")
                            if response.status_code == 200:
                                tab_view.update_view("Definition")
                                definition_view.split_semis = False
                                definition_view.current_search = Result({"keyword": search, "description": response.text, "related_terms": False, "references": ["From: https://labs.bible.org/api/"], "page_number": "", "is_verb": False, "is_noun": False, "is_adjective": False})

                elif key == pyg.K_PAGEDOWN and dream_log_view.dream_input.active:
                    dream_log_view.dream_input.scroll_content(0, "max")
                elif key == pyg.K_PAGEUP and dream_log_view.dream_input.active:
                    dream_log_view.dream_input.scroll_content(0, "min")

                else:
                    ev_handlers.handle_input(key, (shift, caps, ctrl), tab_view)

            elif event.type == pyg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    result = ev_handlers.handle_mouse_click(tab_view, results_view, tab_bar)
                    if result == "QUIT":
                        Quit(tab_view)

                # Middleclick on history item brings it to the description view
                elif event.button == 2:
                    index = search_view.check_history_clicked()
                    if index != None:
                        definition_view.split_semis = True
                        tab_view.update_view("Definition")
                        definition_view.current_search = results_view.get_search(search_view.history[index])

                        if definition_view.current_search == None and settings_view.boxes["bible_search"].active:
                            response = requests.get("https://labs.bible.org/api/?passage=" + search + "&formatting=plain")
                            if response.status_code == 200:
                                tab_view.update_view("Definition")
                                definition_view.split_semis = False
                                definition_view.current_search = Result({"keyword": search, "description": response.text, "related_terms": False, "references": ["From: https://labs.bible.org/api/"], "page_number": "", "is_verb": False, "is_noun": False, "is_adjective": False})

                elif event.button == 6 and search_view.search_index < len(search_view.history) - 1:
                    ev_handlers.navigate_result(tab_view, results_view, "back")

                elif event.button == 7 and search_view.search_index > 0:
                    ev_handlers.navigate_result(tab_view, results_view, "forward")
            
            elif event.type == pyg.MOUSEWHEEL:
                ev_handlers.handle_mouse_scroll(tab_view, event)

        Globals.cursor_frame = min(Globals.cursor_timeout * Globals.FPS + 1, Globals.cursor_frame + 1)
        draw.draw(results_view, tab_view, tab_bar, profiler)
        Globals.clock.tick(Globals.FPS)

def Quit(tab_view: TabContainer):
    # Save data
    s_handler.save_settings(tab_view.views["Settings"].data)

    dream_data = {"dreams": []}
    for dream in tab_view.views["Dream Log"].list_container.contents:
        dream_data["dreams"].append({"title": dream.title, "date_dreamed": dream.date_dreamt, "date_modified": dream.date_modified, "data": dream.data})
        
    s_handler.save_dreams(dream_data)

    # Exit pygame as program
    pyg.quit()
    sys.exit()

if __name__ == "__main__":
    Main()
