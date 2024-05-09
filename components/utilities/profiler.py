import contextlib
with contextlib.redirect_stdout(None):
    import pygame as pyg
import time

class Profiler:
    def __init__(self, desired_framerate, position, font, color, precision=0, display=False):
        self.past_frames = []
        self.framerate = desired_framerate
        self.previous_frame = 0
        self.x, self.y = position
        self.font = font
        self.text_color = color
        self.precision = precision
        self.display = display

    def calc_frame(self):
        """Calculates the delta time between this frame and the previous, and adds it to its list of frames"""
        current_frame = time.time()
        if self.previous_frame != 0:
            self.past_frames.append(current_frame - self.previous_frame)
            if len(self.past_frames) > self.framerate * 5:
                self.past_frames.pop(0)
        self.previous_frame = current_frame

    def calc_framerate(self):
        """Calculates the actual framerate of a program based on the profiler's saved frames"""
        # Calculate the average delta between frames
        try:
            frame_total = sum(self.past_frames) / len(self.past_frames)
            return 1 / frame_total
        except ZeroDivisionError:
            return self.framerate
    
    def draw(self, window):
        if not self.display:
            return
        
        fps = (int(self.calc_framerate()) if self.precision == 0 else round(self.calc_framerate(), self.precision))
        window.blit(self.font.render(str(fps), True, self.text_color), (self.x, self.y))