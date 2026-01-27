import pygame

from enum import Enum
from random import randint
from uuid import uuid1

# Visual constants
STATION_SIZE: int = 20
STATION_COLOR: tuple[int, int, int] = (136, 183, 181)


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
    
    def type(self) -> str:
        """Get the station type name."""
        return self.station.name
    
    def describe(self) -> str:
        """Get a text description of the station."""
        return f"{self.station.name} at ({self.x}, {self.y})"
    
    def render(self, screen: pygame.Surface, selected: bool = False) -> None:
        """Render the station shape on the given surface."""
        modifier: int = 0
        if selected:
            modifier = 5
        if self.station == StationType.Circle:
            pygame.draw.circle(screen, STATION_COLOR, (self.x, self.y), STATION_SIZE + modifier)
        elif self.station == StationType.Triangle:
            points = [
                (self.x, self.y - STATION_SIZE - modifier),
                (self.x - STATION_SIZE, self.y + STATION_SIZE + modifier),
                (self.x + STATION_SIZE, self.y + STATION_SIZE + modifier)
            ]
            pygame.draw.polygon(screen, STATION_COLOR, points)
        elif self.station == StationType.Square:
            rect = pygame.Rect(self.x - STATION_SIZE, self.y - STATION_SIZE, STATION_SIZE * 2, STATION_SIZE * 2 + modifier)
            pygame.draw.rect(screen, STATION_COLOR, rect)