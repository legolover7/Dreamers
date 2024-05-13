import pygame as pyg
import copy

from common.classes.display import Colors, ColorTheme
from common.classes.globals import Globals

from components.tab_control.tab_components import TabBar
from components.tab_control.tab_container import TabContainer
from search_engine.modules.result_view import ResultsView
import common.modules.collider as collider

def draw(search_view: ResultsView, tab_view: TabContainer, tab_bar: TabBar, profiler):
    VID_BUFFER = Globals.VID_BUFFER

    VID_BUFFER.fill(ColorTheme.current_theme.background_color)

    tab_bar.draw(VID_BUFFER, (0, 0))
    search_view.draw(VID_BUFFER, (50, 0))
    
    tab_view.draw(VID_BUFFER, Globals.mouse_position)

    profiler.draw(VID_BUFFER, ColorTheme.current_theme.text_color)

    # Close button
    if collider.collides_point_circle(Globals.mouse_position, (Globals.WIDTH - 19, 15), 12):
        pyg.draw.circle(VID_BUFFER, ColorTheme.current_theme.field_background_color, (Globals.WIDTH - 19, 15), 12)
    pyg.draw.line(VID_BUFFER, ColorTheme.current_theme.cursor_color, (Globals.WIDTH - 24, 10), (Globals.WIDTH - 14, 20))
    pyg.draw.line(VID_BUFFER, ColorTheme.current_theme.cursor_color, (Globals.WIDTH - 14, 10), (Globals.WIDTH - 24, 20))

    # Draw window
    Globals.WINDOW.blit(pyg.transform.scale(VID_BUFFER, (Globals.WINDOW_WIDTH, Globals.WINDOW_HEIGHT)), (0, 0))
    pyg.display.update() 
