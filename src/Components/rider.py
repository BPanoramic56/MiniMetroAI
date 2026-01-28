import pygame

from time import time
from uuid import uuid1, UUID
from typing import Tuple

import shapes

from typeEnums import StationType
from tracker import Tracker

# Design constants
RIDER_PATIENCE: float = 30.0
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
        shapes.CustomShape.render_shape(
            screen=screen,
            x=x,
            y=y,
            type=self.destination_type,
            size=RIDER_SIZE,
            width=2,
            color=RIDER_COLOR
        )
    
    def update(self):
        if time() > self.spawn_time + self.patience and not self.abandon:
            self.abandon = True
            if self.tracker:
                self.tracker.passengers_lost += 1