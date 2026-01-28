import pygame

from random import randint
from typing import List, Tuple

from typeEnums import StationType
from station import Station

# Visual constants
LINE_COLORS: List[Tuple[int, int, int]] = [
    (255, 150, 150),
    (150, 255, 150),
    (150, 150, 255)
]
LINE_WIDTH: int = 10


class Line:
    """Represents a metro line connecting two stations."""
    
    def __init__(self, origin: Station, destination: Station):
        self.origin: Station = origin
        self.destination: Station = destination
        self.color: Tuple[int, int, int] = LINE_COLORS[randint(0, len(LINE_COLORS) - 1)]
        self.width: int = LINE_WIDTH
        
    def render(self, screen: pygame.Surface) -> None:
        """Render the line connecting two stations."""
        pygame.draw.line(
            screen, 
            self.color, 
            (self.origin.x, self.origin.y), 
            (self.destination.x, self.destination.y), 
            self.width
        )