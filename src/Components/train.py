import pygame

from typing import List, Tuple
from uuid import uuid1, UUID

from line import Line
from rider import Rider

# Design constants
TRAIN_CAPACITY: int = 6
TRAIN_SPEED: float = 2.0

# Visual constants
TRAIN_SIZE: int = 12
TRAIN_COLOR: Tuple[int, int, int] = (255, 200, 50)


class Train:
    """Represents a train traveling along a line between stations."""
    
    def __init__(self, line: Line):
        self.line: Line = line
        self.capacity: int = TRAIN_CAPACITY
        self.riders: List[Rider] = []
        self.progress: float = 0.0
        self.id: UUID = uuid1()
        self.forward: bool = True
    
    def update(self) -> None:
        """Update train position along the line."""
        if self.forward:
            self.progress += TRAIN_SPEED
            if self.progress >= 100.0:
                self.progress = 100.0
                self.forward = False
                self._arrive_at_station(self.line.destination)
        else:
            self.progress -= TRAIN_SPEED
            if self.progress <= 0.0:
                self.progress = 0.0
                self.forward = True
                self._arrive_at_station(self.line.origin)
    
    def _arrive_at_station(self, station) -> None:
        """Handle train arriving at a station (unload/load passengers)."""
        print(f"Train arrived at {station.describe()}")
    
    def get_position(self) -> Tuple[int, int]:
        """Calculate current position based on progress along the line."""
        t = self.progress / 100.0
        x = int(self.line.origin.x + t * (self.line.destination.x - self.line.origin.x))
        y = int(self.line.origin.y + t * (self.line.destination.y - self.line.origin.y))
        return (x, y)
    
    def render(self, screen: pygame.Surface) -> None:
        """Render the train at its current position."""
        x, y = self.get_position()
        rect = pygame.Rect(x - TRAIN_SIZE, y - TRAIN_SIZE, TRAIN_SIZE * 2, TRAIN_SIZE * 2)
        pygame.draw.rect(screen, TRAIN_COLOR, rect)