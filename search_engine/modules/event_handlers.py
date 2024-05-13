import pygame as pyg
import copy

# Common classes/modules
from common.classes.display import ColorTheme
from common.classes.globals import Globals
import common.modules.typing_handler as typing_handler
import common.modules.collider as collider
from components.tab_control.tab_container import TabContainer
# Components
from components.tab_control.tab_container import TabContainer
from components.tab_control.tab_components import Tab, TabBar
from components.tab_control.search_view import SearchView
from components.tab_control.definition_view import DefinitionView
from components.tab_control.dream_log_view import DreamLogView
from components.tab_control.settings_view import SettingsView
# Other
from search_engine.modules.result_view import ResultsView

def handle_input(key, mods, tab_view: TabContainer):
    shift, caps, ctrl = mods
    Globals.cursor_frame = 0
    # Search bar
    if tab_view.views["Search"].searchbar.active and not (key == pyg.K_SPACE and tab_view.views["Search"].searchbar.text == ""):
        tab_view.views["Search"].searchbar.text, Globals.cursor_position = typing_handler.handler(tab_view.views["Search"].searchbar.text, key, mods, Globals.cursor_position)

    # Dream log input
    elif tab_view.views["Dream Log"].dream_input.active:
        if key == pyg.K_TAB:
            tab_view.views["Dream Log"].dream_input.active = False
            tab_view.views["Dream Log"].dream_title.active = True
            Globals.cursor_position = len(tab_view.views["Dream Log"].dream_title.text)
        else:
            tab_view.views["Dream Log"].dream_input.text, Globals.cursor_position = typing_handler.handler(tab_view.views["Dream Log"].dream_input.text, key, mods, Globals.cursor_position, allow_enter=True)

    # Dream log title
    elif tab_view.views["Dream Log"].dream_title.active :
        if key == pyg.K_TAB and shift:
            tab_view.views["Dream Log"].dream_input.active = True
            tab_view.views["Dream Log"].dream_title.active = False
            Globals.cursor_position = len(tab_view.views["Dream Log"].dream_input.text)
        elif key == pyg.K_TAB:
            tab_view.views["Dream Log"].dream_title.active = False
            tab_view.views["Dream Log"].date_input.active = True
            Globals.cursor_position = len(tab_view.views["Dream Log"].date_input.text)
        else:
            tab_view.views["Dream Log"].dream_title.text, Globals.cursor_position = typing_handler.handler(tab_view.views["Dream Log"].dream_title.text, key, mods, Globals.cursor_position)

    # Dream log date
    elif tab_view.views["Dream Log"].date_input.active:
        if key == pyg.K_TAB and shift:
            tab_view.views["Dream Log"].dream_title.active = True
            tab_view.views["Dream Log"].date_input.active = False
            Globals.cursor_position = len(tab_view.views["Dream Log"].dream_title.text)
        else:
            tab_view.views["Dream Log"].date_input.text, Globals.cursor_position = typing_handler.handle_ints(tab_view.views["Dream Log"].date_input.text, key, mods, Globals.cursor_position)

def handle_mouse_click(tab_view: TabContainer, results_view: ResultsView, tab_bar: TabBar):
    tab_mouse_position = copy.deepcopy(Globals.mouse_position)
    tab_mouse_position[0] = tab_mouse_position[0] - tab_view.x
    tab_mouse_position[1] = tab_mouse_position[1] - tab_view.y

    # Unpack tab view objects
    search_view:     SearchView     = tab_view.views["Search"]
    definition_view: DefinitionView = tab_view.views["Definition"]
    dream_log_view:  DreamLogView   = tab_view.views["Dream Log"]
    settings_view:   SettingsView   = tab_view.views["Settings"]
    
    Globals.cursor_frame = 0
    # Confirmation popups
    if dream_log_view.popup_displayed and not tab_view.popup.check_mcollision(tab_mouse_position):
        dream_log_view.popup_displayed = False
        return
    elif dream_log_view.popup_displayed:
        # Dream log button
        response = tab_view.popup.click(tab_mouse_position)
        if response == "Cancel":
            dream_log_view.popup_displayed = False
            return
        elif response == "Confirm":
            # Remove the log from the list
            for log in dream_log_view.list_container.contents:
                if log.title == dream_log_view.dream_title.text:
                    dream_log_view.list_container.contents.remove(log)

            # Reset fields
            dream_log_view.dream_input.text = ""
            dream_log_view.dream_title.text = ""
            dream_log_view.date_input.text = ""
            dream_log_view.popup_displayed = False
            return
    
    tab_mouse_position = copy.deepcopy(Globals.mouse_position)
    tab_mouse_position[0] = tab_mouse_position[0] - tab_view.x
    tab_mouse_position[1] = tab_mouse_position[1] - tab_view.y
    # Check for close button
    if collider.collides_point_circle(Globals.mouse_position, (Globals.WIDTH - 19, 15), 12):
        return "QUIT"

    # Check for the different tabs for the tab view (right half)
    for tab in tab_view.tabs:
        if tab.check_mcollision(tab_mouse_position):
            tab_view.update_view(tab.text)
            return

    # Check for a result that was clicked on
    result = results_view.check_result_clicked()
    if result is not None:
        # A related keyword was clicked
        if isinstance(result, str):
            results_view.update_search({"keyword": result, "type": "strict"})
            tab_view.update_view("Search")
            search_view.history.append(result)
        else:
            definition_view.current_search = result
            tab_view.update_view("Definition")
        return
        
    # Check for the different tabs for the tabbar (leftmost size)
    index = tab_bar.check_mcollision()
    if index != None:
        results_view.update_search({"keyword": "ABCDEFGHIJKLMNOPQRSTUVWXYZ"[index], "type": "strict"})
        return

    if tab_view.view == "Search":
        index = search_view.check_history_clicked(tab_mouse_position)
        if index != None:
            results_view.update_search({"keyword": search_view.history[index], "type": "strict"})
            return

    # Send a click to the currently active tab
    if tab_view.check_mcollision(Globals.mouse_position):
        tab_view.views[tab_view.view].click(tab_mouse_position)



def handle_mouse_scroll(tab_view: TabContainer, event: pyg.event.Event):
    """Handles when a mouse scroll event happens"""
    if tab_view.view == "Dream Log":
        if tab_view.views["Dream Log"].dream_input.check_mcollision():
            tab_view.views["Dream Log"].dream_input.scroll_content(-event.y)


def navigate_result(tab_view: TabContainer, results_view: ResultsView, direction):
    if direction == "back":
        tab_view.views["Search"].search_index += 1
        previous_search = tab_view.views["Search"].history[len(tab_view.views["Search"].history) - tab_view.views["Search"].search_index - 1]
        results_view.update_search({"keyword": previous_search, "type": "contains"})
        tab_view.views["Search"].searchbar.text = previous_search
        Globals.cursor_position = len(previous_search)

    else:
        tab_view.views["Search"].search_index -= 1
        previous_search = tab_view.views["Search"].history[len(tab_view.views["Search"].history) - tab_view.views["Search"].search_index - 1]
        results_view.update_search({"keyword": previous_search, "type": "contains"})
        tab_view.views["Search"].searchbar.text = previous_search
        Globals.cursor_position = len(previous_search)