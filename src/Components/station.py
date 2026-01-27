import pygame

from enum import Enum
from random import randint
from uuid import uuid1

# Design Constants
STATION_LIMIT: int = 20 # Total amount of riders a station can hold at once

# Visual constants
STATION_SIZE: int = 20
STATION_COLOR = (100, 100, 100)
SELECTED_COLOR = (100, 100, 150)


class StationType(Enum):
    """Types of stations with different shapes."""
    Circle = 0
    Triangle = 1
    Square = 2

class Station:
    """Represents a metro station with a shape and position."""
    
    def __init__(self, x: int, y: int):
        self.station: StationType = StationType(randint(0, len(StationType) - 1))
        self.x: int = x
        self.y: int = y
        self.id: int = uuid1()
        self.limit: int = STATION_LIMIT
    
    def type(self) -> str:
        """Get the station type name."""
        return self.station.name
    
    def describe(self) -> str:
        """Get a text description of the station."""
        return f"{self.station.name} at ({self.x}, {self.y})"
    
    def render(self, screen: pygame.Surface, selected: bool = False) -> None:
        """Render the station shape on the given surface."""
        color = SELECTED_COLOR if selected else STATION_COLOR
        
        if self.station == StationType.Circle:
            pygame.draw.circle(screen, color, (self.x, self.y), STATION_SIZE)
        elif self.station == StationType.Triangle:
            points = [
                (self.x, self.y - STATION_SIZE),
                (self.x - STATION_SIZE, self.y + STATION_SIZE),
                (self.x + STATION_SIZE, self.y + STATION_SIZE)
            ]
            pygame.draw.polygon(screen, color, points)
        elif self.station == StationType.Square:
            rect = pygame.Rect(self.x - STATION_SIZE, self.y - STATION_SIZE, STATION_SIZE * 2, STATION_SIZE * 2)
            pygame.draw.rect(screen, color, rect)