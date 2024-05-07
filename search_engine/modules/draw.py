import pygame as pyg
pyg.init()
pyg.font.init()

from common.classes.display import Colors
from common.classes.globals import Globals

from components.tab_control.tab_components import TabBar
from components.tab_control.tab_container import TabContainer
from search_engine.modules.result_view import ResultsView
import common.modules.collider as collider

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

    if collider.collides_point_circle(Globals.mouse_position, (Globals.WIDTH - 19, 15), 12):
        pyg.draw.circle(VID_BUFFER, Colors.gray, (Globals.WIDTH - 19, 15), 12)

    pyg.draw.line(VID_BUFFER, Colors.white, (Globals.WIDTH - 24, 10), (Globals.WIDTH - 14, 20))
    pyg.draw.line(VID_BUFFER, Colors.white, (Globals.WIDTH - 14, 10), (Globals.WIDTH - 24, 20))

    # Draw window
    Globals.WINDOW.blit(pyg.transform.scale(VID_BUFFER, (Globals.WINDOW_WIDTH, Globals.WINDOW_HEIGHT)), (0, 0))
    pyg.display.update() 
