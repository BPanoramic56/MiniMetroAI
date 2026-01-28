import pygame
import time

from random import randint
from uuid import uuid1, UUID
from typing import List, Tuple

from typeEnums import StationType
from rider import Rider
from tracker import Tracker

# Design constants
STATION_LIMIT: int = 20
RIDER_SPAWN_INTERVAL: float = 5.0

# Visual constants
STATION_SIZE: int = 20
STATION_COLOR: Tuple[int, int, int] = (150, 150, 150)
SELECTED_COLOR: Tuple[int, int, int] = (150, 150, 250)


class Station:
    """Represents a metro station with a shape and position."""
    
    def __init__(self, x: int, y: int, tracker: Tracker = None):
        self.station_type: StationType = StationType(randint(0, len(StationType) - 1))
        self.x: int = x
        self.y: int = y
        self.id: UUID = uuid1()
        self.limit: int = STATION_LIMIT
        self.last_spawn_time: float = time.time()
        self.riders: List[Rider] = []
        
        self.tracker = tracker
    
    def type(self) -> str:
        """Get the station type name."""
        return self.station_type.name
    
    def describe(self) -> str:
        """Get a text description of the station."""
        return f"{self.station_type.name} at ({self.x}, {self.y})"
    
    def render(self, screen: pygame.Surface, selected: bool = False) -> None:
        """Render the station shape on the given surface."""
        color = SELECTED_COLOR if selected else STATION_COLOR
        
        if self.station_type == StationType.Circle:
            pygame.draw.circle(screen, color, (self.x, self.y), STATION_SIZE)
        elif self.station_type == StationType.Triangle:
            points = [
                (self.x, self.y - STATION_SIZE),
                (self.x - STATION_SIZE, self.y + STATION_SIZE),
                (self.x + STATION_SIZE, self.y + STATION_SIZE)
            ]
            pygame.draw.polygon(screen, color, points)
        elif self.station_type == StationType.Square:
            rect = pygame.Rect(self.x - STATION_SIZE, self.y - STATION_SIZE, STATION_SIZE * 2, STATION_SIZE * 2)
            pygame.draw.rect(screen, color, rect)
    
        rider_y: int = self.y - 20
        rider_x: int = self.x + 30
        for rider in self.riders:
            rider.render(screen, rider_x, rider_y)
            rider_x += 15

    def should_create_rider(self) -> bool:
        """Check if enough time has passed to spawn a new rider."""
        if time.time() - self.last_spawn_time >= RIDER_SPAWN_INTERVAL:
            self.last_spawn_time = time.time()
            return True
        return False

    def update(self) -> None:
        """Update station state (spawn riders)."""
        if self.should_create_rider() and len(self.riders) < self.limit:
            destination_type = StationType(randint(0, len(StationType) - 1))
             
            # Does not add the rider to the station if it's destination is already this station. This adds a little variability and randomness to the time in which drivers are created
            if destination_type == self.station_type:
                return
            
            new_rider = Rider(self.id, destination_type, tracker=self.tracker)
            self.riders.append(new_rider)
            print(f"New rider at {self.describe()}: wants {destination_type.name} ({len(self.riders)} waiting)")
            if self.tracker:
                self.tracker.total_passengers += 1
        
        for rider in self.riders:
            rider.update()
        
        self.riders = [rider for rider in self.riders if not rider.abandon]