import contextlib
with contextlib.redirect_stdout(None):
    import pygame as pyg

from common.classes.display import Colors, Fonts
from common.classes.globals import Globals

def draw(fields, boxes, buttons, error_message, error_timeout):
    VID_BUFFER = Globals.VID_BUFFER
    WIDTH, HEIGHT = Globals.WIDTH, Globals.HEIGHT

    VID_BUFFER.fill(Colors.black)

    text_width = Fonts.font_35.size("Dreamers Editor")[0]
    VID_BUFFER.blit(Fonts.font_35.render("Dreamers Editor", True, Colors.white), (Globals.WIDTH/2 - text_width/2, 20))

    for i in range(len(fields)):
        field = fields[i]
        if i > 2:
            field.draw(VID_BUFFER)
        else:
            field.draw(VID_BUFFER)

    for box in boxes:
        box.draw(VID_BUFFER)

    for button in buttons:
        button.draw(VID_BUFFER)

    if error_timeout > 0:
        text_width = Fonts.font_20.size(error_message)[0]
        Globals.VID_BUFFER.blit(Fonts.font_20.render(error_message, True, Colors.error_red), ((Globals.WIDTH-text_width)/2, Globals.HEIGHT-130))

    # Draw window
    Globals.WINDOW.blit(pyg.transform.scale(VID_BUFFER, (Globals.WINDOW_WIDTH, Globals.WINDOW_HEIGHT)), (0, 0))
    pyg.display.update() 