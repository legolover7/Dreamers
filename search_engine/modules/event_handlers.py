import pygame as pyg

from common.classes.globals import Globals
import common.modules.typing_handler as typing_handler
import common.modules.collider as collider
from components.tab_control.tab_container import TabContainer
from search_engine.modules.result_view import ResultsView
from components.tab_control.tab_container import TabContainer
from components.tab_control.tab_components import Tab, TabBar

def handle_input(key, mods, tab_view: TabContainer):
    shift, caps, ctrl = mods
    # Search bar
    if tab_view.search_view.searchbar.active and not (key == pyg.K_SPACE and tab_view.search_view.searchbar.text == ""):
        tab_view.search_view.searchbar.text, Globals.cursor_position = typing_handler.handler(tab_view.search_view.searchbar.text, key, mods, Globals.cursor_position)

    # Dream log input
    elif tab_view.dream_log_view.dream_input.active:
        if key == pyg.K_TAB:
            tab_view.dream_log_view.dream_input.active = False
            tab_view.dream_log_view.dream_title.active = True
            Globals.cursor_position = len(tab_view.dream_log_view.dream_title.text)
        else:
            tab_view.dream_log_view.dream_input.text, Globals.cursor_position = typing_handler.handler(tab_view.dream_log_view.dream_input.text, key, mods, Globals.cursor_position)

    # Dream log title
    elif tab_view.dream_log_view.dream_title.active:
        if key == pyg.K_TAB and shift:
            tab_view.dream_log_view.dream_input.active = True
            tab_view.dream_log_view.dream_title.active = False
            Globals.cursor_position = len(tab_view.dream_log_view.dream_input.text)
        elif key == pyg.K_TAB:
            tab_view.dream_log_view.dream_title.active = False
            tab_view.dream_log_view.date_input.active = True
            Globals.cursor_position = len(tab_view.dream_log_view.date_input.text)
        else:
            tab_view.dream_log_view.dream_title.text, Globals.cursor_position = typing_handler.handler(tab_view.dream_log_view.dream_title.text, key, mods, Globals.cursor_position)

    elif tab_view.dream_log_view.date_input.active:
        if key == pyg.K_TAB and shift:
            tab_view.dream_log_view.dream_title.active = True
            tab_view.dream_log_view.date_input.active = False
            Globals.cursor_position = len(tab_view.dream_log_view.dream_title.text)
        else:
            tab_view.dream_log_view.date_input.text, Globals.cursor_position = typing_handler.handler(tab_view.dream_log_view.date_input.text, key, mods, Globals.cursor_position)

def handle_mouse_click(tab_view: TabContainer, results_view: ResultsView, tab_bar: TabBar):
    # Check for close button
    if collider.collides_point_circle(Globals.mouse_position, (Globals.WIDTH - 19, 15), 12):
        return "QUIT"

    # Check for the different tabs for the tab view (right half)
    for tab in tab_view.tabs:
        if tab.check_mcollision():
            tab_view.update_view(tab.text)

    # Check for a result that was clicked on
    result = results_view.check_result_clicked()
    if result is not None:
        # A related keyword was clicked
        if isinstance(result, str):
            results_view.update_search({"keyword": result, "type": "strict"})
            tab_view.update_view("Search")
            tab_view.search_view.searchbar.text = result
        else:
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
    if tab_view.view == "Definition":
        if tab_view.definition_view.clear_search_button.check_mcollision():
            tab_view.current_search = None

    # Check for search's searchbar
    elif tab_view.view == "Search":
        tab_view.search_view.searchbar.active = False
        if tab_view.search_view.searchbar.check_mcollision():
            tab_view.search_view.searchbar.active = True
            Globals.cursor_position = len(tab_view.search_view.searchbar.text)

    # Check for dream log's input fields and list container
    elif tab_view.view == "Dream Log":
        tab_view.dream_log_view.dream_input.active = False
        tab_view.dream_log_view.dream_title.active = False
        tab_view.dream_log_view.date_input.active = False

        if tab_view.dream_log_view.dream_input.check_mcollision():
            tab_view.dream_log_view.dream_input.active = True
            Globals.cursor_position = len(tab_view.dream_log_view.dream_input.text)
        elif tab_view.dream_log_view.dream_title.check_mcollision():
            tab_view.dream_log_view.dream_title.active = True
            Globals.cursor_position = len(tab_view.dream_log_view.dream_title.text)
        elif tab_view.dream_log_view.date_input.check_mcollision():
            tab_view.dream_log_view.date_input.active = True
            Globals.cursor_position = len(tab_view.dream_log_view.date_input.text)
            
        # Dream log save button
        if tab_view.dream_log_view.save_button.check_mcollision():
            tab_view.dream_log_view.save_dream()
            tab_view.dream_log_view.dream_input.text = ""
            tab_view.dream_log_view.dream_title.text = ""

        # List container
        item = tab_view.dream_log_view.list_container.check_click()
        if item:
            tab_view.dream_log_view.dream_input.text = item.data
            tab_view.dream_log_view.dream_title.text = item.title
            tab_view.dream_log_view.date_input.text = item.date_dreamed

    # Check for settings' checkboxes
    elif tab_view.view == "Settings":
        for box_key in tab_view.settings_view.boxes.keys():
            box = tab_view.settings_view.boxes[box_key]
            if box.check_mcollision():
                box.active = not box.active
                tab_view.settings_view.data[box.value] = box.active

def handle_mouse_scroll(tab_view: TabContainer, event):
    if tab_view.view == "Dream Log":

        if tab_view.dream_log_view.dream_input.check_mcollision():
            tab_view.dream_log_view.dream_input.scroll_text_content(-event.y)