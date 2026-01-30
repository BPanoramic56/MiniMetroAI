import pygame
import time

from random import randint
from uuid import uuid1, UUID
from typing import List, Tuple
from random import choice

import shapes
from resourceManager import resources

from typeEnums import StationType
from rider import Rider
from tracker import Tracker

# Design constants
STATION_LIMIT: int = 20
RIDER_SPAWN_INTERVAL: float = 5.0

# Visual constants
STATION_SIZE: int = 20
UNSERVICED_COLOR: Tuple[int, int, int] = (175, 100, 100)
SERVICED_COLOR: Tuple[int, int, int] = (80, 80, 255)
SELECTED_COLOR: Tuple[int, int, int] = (255, 255, 255)


class Station:
    """Represents a metro station with a shape and position."""
    
    def __init__(self, x: int, y: int, type: StationType, tracker: Tracker = None):
        self.x: int = x
        self.y: int = y
        self.station_type: StationType = type
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
        # Try to render sprite first
        color = SELECTED_COLOR if selected else (UNSERVICED_COLOR if self.tracker.serviced_stations[self.id] == 0 else SERVICED_COLOR)
        sprite = resources.get_station_sprite(self.station_type, STATION_SIZE)
        if sprite and resources.use_sprites:
            # Tint the sprite with the color
            tinted_sprite = sprite.copy()
            tinted_sprite.fill(color, special_flags=pygame.BLEND_RGBA_MULT)
            rect = tinted_sprite.get_rect(center=(self.x, self.y))
            screen.blit(tinted_sprite, rect)
        else:
            # Fallback to geometric shapes
            shapes.CustomShape.render_shape(
                screen=screen,
                x=self.x,
                y=self.y,
                size=STATION_SIZE,
                type=self.station_type,
                width=5,
                color=color
            )
    
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
            self.create_passenger()
        for rider in self.riders:
            rider.update()
        
        self.riders = [rider for rider in self.riders if not rider.abandon]
        
    def create_passenger(self) -> None:
        destination_type: StationType = choice(list(self.tracker.station_types))
            
        # Does not add the rider to the station if it's destination is already this station. This adds a little variability and randomness to the time in which drivers are created
        if destination_type == self.station_type:
            return
        
        new_rider = Rider(self.id, destination_type, tracker=self.tracker)
        self.riders.append(new_rider)
        print(f"New rider at {self.describe()}: wants {destination_type.name} ({len(self.riders)} waiting)")
        if self.tracker:
            self.tracker.total_passengers += 1