import pygame as pyg
pyg.init()
pyg.font.init()

from common.classes.display import Colors, Fonts
from common.classes.globals import Globals
from common.classes.input_field import InputField

from components.tab_control.tab_components import TabBar
from components.tab_control.tab_container import TabContainer
from search_engine.modules.result_view import ResultsView

def draw(search_view: ResultsView, tab_view: TabContainer, tab_bar: TabBar, profiler):
    VID_BUFFER = Globals.VID_BUFFER
    WIDTH, HEIGHT = Globals.WIDTH, Globals.HEIGHT

    VID_BUFFER.fill(Colors.black)

    tab_bar.draw(VID_BUFFER, (0, 0))
    search_view.draw(VID_BUFFER, (50, 0))
    tab_view.draw(VID_BUFFER, (Globals.WIDTH/2+50, 0))

    for tab in tab_view.tabs:
        tab.draw(VID_BUFFER)

    profiler.draw(VID_BUFFER)

    # Draw window
    Globals.WINDOW.blit(pyg.transform.scale(VID_BUFFER, (Globals.WINDOW_WIDTH, Globals.WINDOW_HEIGHT)), (0, 0))
    pyg.display.update() 
