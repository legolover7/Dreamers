import contextlib
with contextlib.redirect_stdout(None):
    import pygame as pyg

class Globals:
    # Default size of the application
    WIDTH, HEIGHT = (1920, 1080)
    # User's monitor size
    WINDOW_WIDTH, WINDOW_HEIGHT = (1920, 1080)
    # Actual window object that gets displayed to the user
    WINDOW = None
    # Image buffer that gets scaled to the user's monitor size, from the default size
    VID_BUFFER = pyg.surface.Surface((WIDTH, HEIGHT))

    # Max FPS of application
    FPS = 60
    # Pygame clock object for controlling the framerate
    clock = pyg.time.Clock()

    # Current position of mouse cursor
    mouse_position = [0, 0]

    cursor_position = 0
    cursor_period = 1.2 * FPS
    cursor_timeout = 5 * cursor_period
    cursor_frame = 0 

    MAX_RETURN_NUMBER = 15


class FilePaths:
    settings = "./data/settings.json"
    logs = "./data/dreams.json"
    terms = "./data/search_terms.json"