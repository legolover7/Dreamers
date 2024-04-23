import pygame as pyg
pyg.init()
pyg.font.init()

from common.classes.display import Colors, Fonts
from common.classes.globals import Globals

import search_engine.modules.search_view as search_view
import search_engine.modules.tabbar as tabbar

def draw():
    VID_BUFFER = Globals.VID_BUFFER
    WIDTH, HEIGHT = Globals.WIDTH, Globals.HEIGHT

    VID_BUFFER.fill(Colors.black)

    search_view.draw(VID_BUFFER, (50, 0))
    tabbar.draw(VID_BUFFER, (0, 0))

    # Draw window
    Globals.WINDOW.blit(pyg.transform.scale(VID_BUFFER, (Globals.WINDOW_WIDTH, Globals.WINDOW_HEIGHT)), (0, 0))
    pyg.display.update() 