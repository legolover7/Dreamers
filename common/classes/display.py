import contextlib
with contextlib.redirect_stdout(None):
    import pygame as pyg
pyg.font.init()

class Colors:
    dark_black = (0, 0, 0)
    black = (25, 25, 25)
    dark_gray = (50, 50, 50)
    gray = (70, 70, 70)
    light_gray = (90, 90, 90)
    lightish_gray = (105, 105, 105)
    lighter_gray = (120, 120, 120)
    dark_white = (200, 200, 200)
    white = (255, 255, 255)

    green = (0, 200, 0)
    aqua = (0, 255, 255)
    dark_aqua = (0, 128, 128)
    blue = (0, 0, 200)
    light_blue = (0, 0, 238)
    red = (200, 0, 0)
    error_red = (255, 0, 0)

class Fonts:
    font_18 = pyg.font.SysFont("consolas", 18)
    font_20 = pyg.font.SysFont("consolas", 20)
    font_24 = pyg.font.SysFont("consolas", 24)
    font_30 = pyg.font.SysFont("consolas", 30)
    font_35 = pyg.font.SysFont("consolas", 35)

class ColorScheme:
    def __init__(self, bg, bgbdr, fbdr, fbg, stc, tc, dtc, cc):
        self.background_color = bg
        self.background_border_color = bgbdr
        self.field_border_color = fbdr
        self.field_background_color = fbg
        self.selected_tab_color = stc
        self.text_color = tc
        self.dim_text_color = dtc
        self.cursor_color = cc

class ColorTheme:
    #                        Background         Background Border  Field background     Field border       Selected Tab color    Text          Dimmed text          Cursor
    dark_mode  = ColorScheme(Colors.black,      Colors.dark_black, Colors.gray,         Colors.dark_gray,  Colors.light_gray,    Colors.white, Colors.lighter_gray, Colors.white)
    light_mode = ColorScheme(Colors.dark_white, Colors.dark_white, Colors.dark_white,   Colors.gray,       Colors.lighter_gray,    Colors.black, Colors.gray,         Colors.black)
    current_theme = dark_mode

    def change_theme(theme):
        if theme == "Dark":
            ColorTheme.current_theme = ColorTheme.dark_mode

        elif theme == "Light":
            ColorTheme.current_theme = ColorTheme.light_mode