import pygame as pyg
pyg.init()
pyg.font.init()

from common.classes.display import Colors, Fonts
from common.classes.globals import Globals

def draw(fields, boxes, buttons, active_field, desc_offset, related_input, category_input, error_message, error_timeout):
    VID_BUFFER = Globals.VID_BUFFER
    WIDTH, HEIGHT = Globals.WIDTH, Globals.HEIGHT

    VID_BUFFER.fill(Colors.black)

    for field in fields:
        if field == related_input or field == category_input:
            field.draw(active_field, desc_offset)
        else:
            field.draw(active_field)

    for box in boxes:
        box.draw()

    for button in buttons:
        button.draw()

    if error_timeout > 0:
        text_width = Fonts.font_20.size(error_message)[0]
        Globals.VID_BUFFER.blit(Fonts.font_20.render(error_message, True, Colors.error_red), ((Globals.WIDTH-text_width)/2, Globals.HEIGHT-130))

    # Draw window
    Globals.WINDOW.blit(pyg.transform.scale(VID_BUFFER, (Globals.WINDOW_WIDTH, Globals.WINDOW_HEIGHT)), (0, 0))
    pyg.display.update() 