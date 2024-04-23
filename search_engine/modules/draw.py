import pygame as pyg
pyg.init()
pyg.font.init()

from common.classes.display import Colors, Fonts
from common.classes.globals import Globals
from common.classes.input_field import InputField

import search_engine.modules.search_view as search_view
import search_engine.modules.tabbar as tabbar
import search_engine.modules.tabpanel as tabpanel

def draw(tabs):
    VID_BUFFER = Globals.VID_BUFFER
    WIDTH, HEIGHT = Globals.WIDTH, Globals.HEIGHT

    VID_BUFFER.fill(Colors.black)

    tabbar.draw(VID_BUFFER, (0, 0))
    search_view.draw(VID_BUFFER, (50, 0))
    tabpanel.draw(VID_BUFFER, (Globals.WIDTH/2+50, 0))

    for tab in tabs:
        tab.draw(VID_BUFFER)

    if tab[0].active:
        pass
        #draw_search_tab(VID_BUFFER, (Globals.WIDTH/2+50, 0))

    # Draw window
    Globals.WINDOW.blit(pyg.transform.scale(VID_BUFFER, (Globals.WINDOW_WIDTH, Globals.WINDOW_HEIGHT)), (0, 0))
    pyg.display.update() 

    