import contextlib
with contextlib.redirect_stdout(None):
    import pygame as pyg

from common.classes.display import Colors, ColorTheme, Fonts
from common.classes.globals import Globals
import common.modules.collider as collider
import common.modules.chunk_text as chunk_text

class Result:
    def __init__(self, data, selected=False):
        self.data = data
        self.height = 0
        self.related_links = []
        self.generated_links = False
        self.selected = selected

    def draw(self, window: pyg.Surface, offset: tuple[int, int]):
        """Draws this result, including keyword, description, and related links"""
        keyword, description, related = self.get_data()
        start_offset = offset[1]
        self.ox, self.oy = offset

        # Hover indicator
        if self.check_mcollision():
            pyg.draw.rect(window, ColorTheme.current_theme.field_border_color, (offset[0]-8, offset[1], Globals.WIDTH/2-6, self.height), border_radius=8)

        # Searched for indicator
        if self.selected:
            pyg.draw.rect(window, ColorTheme.current_theme.selected_tab_color, (offset[0]-8, offset[1], Globals.WIDTH/2-6, self.height), border_radius=8)

        # Display the keyword
        char_height = Fonts.font_30.size("A")[1]
        window.blit(Fonts.font_30.render(keyword, True, ColorTheme.current_theme.text_color), offset)
        offset[1] += char_height

        # Display the description
        char_width, char_height = Fonts.font_20.size("A")
        description_text = chunk_text.chunk(description, content_width=Globals.WIDTH/2 - 70, char_width=char_width)
        if len(description_text) > 0:
            window.blit(Fonts.font_20.render(description_text[0].strip() + ("..." if len(description_text) > 1 else ""), True, ColorTheme.current_theme.dim_text_color), offset)
        offset[1] += char_height

        # Display related links
        if len(related) > 0:
            hori_offset, text_height = Fonts.font_18.size("Related terms: ")
            window.blit(Fonts.font_18.render("Related terms:", True, ColorTheme.current_theme.dim_text_color), offset)
            
            for rel in related:
                # Separating terms by commas
                comma = ", " if related.index(rel) < len(related) - 1 else ""
                text_width, text_height = Fonts.font_18.size(rel)
                # Creating link buttons
                if not self.generated_links:
                    self.related_links += [{
                        "rect": (offset[0] + hori_offset, offset[1], text_width, text_height),
                        "term": rel
                    }]

                color = Colors.light_blue if collider.collides_point(Globals.mouse_position, (offset[0] + hori_offset, offset[1], text_width, text_height)) else ColorTheme.current_theme.dim_text_color
                # Draw text
                window.blit(Fonts.font_18.render(rel, True, color), (offset[0] + hori_offset, offset[1]))
                window.blit(Fonts.font_18.render(comma, True, ColorTheme.current_theme.dim_text_color), (offset[0] + hori_offset + Fonts.font_18.size(rel)[0], offset[1]))
                hori_offset += text_width + Fonts.font_18.size(", ")[0]
            
            offset[1] += text_height

        self.height = offset[1] - start_offset
        return offset[1] + 5
    
    def check_mcollision(self) -> bool:
        """Returns true if mouse cursor is within this result's bound"""
        return collider.collides_point(Globals.mouse_position, (self.ox-8, self.oy, Globals.WIDTH/2-6, self.height))

    def check_related_click(self) -> str:
        """Returns the search term of the related link clicked"""
        for link in self.related_links:
            if collider.collides_point(Globals.mouse_position, (link["rect"])):
                return link["term"]

    def get_data(self):
        """Gets data from self, returns the result's keyword, description, and related links"""
        keyword = self.data["keyword"]
        description = self.data["description"]
        related = self.data["related_terms"]

        return keyword, description, related