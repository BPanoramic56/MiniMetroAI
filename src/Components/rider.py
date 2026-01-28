import pygame

from time import time
from uuid import uuid1, UUID
from typing import Tuple

from typeEnums import StationType
from tracker import Tracker

# Design constants
RIDER_PATIENCE: float = 2.0
RIDER_SIZE: int = 5
RIDER_COLOR: Tuple[int, int, int] = (200, 100, 100)

class Rider:
    """Represents a passenger waiting at a station."""
    
    def __init__(self, origin: UUID, destination: StationType, tracker: Tracker = None):
        self.origin_id: UUID = origin
        self.destination_type: StationType = destination
        self.patience: float = RIDER_PATIENCE
        self.spawn_time = time()
        self.id: UUID = uuid1()
        
        self.abandon: bool = False    
    
        self.tracker = tracker
    
    def render(self, screen: pygame.Surface, x, y):        
        if self.destination_type == StationType.Circle:
            pygame.draw.circle(screen, RIDER_COLOR, (x, y), RIDER_SIZE)
        elif self.destination_type == StationType.Triangle:
            points = [
                (x, y - RIDER_SIZE),
                (x - RIDER_SIZE, y + RIDER_SIZE),
                (x + RIDER_SIZE, y + RIDER_SIZE)
            ]
            pygame.draw.polygon(screen, RIDER_COLOR, points)
        elif self.destination_type == StationType.Square:
            rect = pygame.Rect(x - RIDER_SIZE, y - RIDER_SIZE, RIDER_SIZE * 2, RIDER_SIZE * 2)
            pygame.draw.rect(screen, RIDER_COLOR, rect)
    
    def update(self):
        if time() > self.spawn_time + self.patience and not self.abandon:
            self.abandon = True
            if self.tracker:
                self.tracker.passengers_lost += 1