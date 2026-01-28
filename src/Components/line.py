import pygame

from random import randint
from typing import List, Tuple, Set
from uuid import uuid1, UUID

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
    """Represents a metro line connecting multiple stations."""
    
    def __init__(self, stations: List[Station]):
        if len(stations) < 2:
            raise ValueError("Line must connect at least 2 stations")
        
        self.stations: List[Station] = stations
        self.color: Tuple[int, int, int] = LINE_COLORS[randint(0, len(LINE_COLORS) - 1)]
        self.width: int = LINE_WIDTH
        self.id: UUID = uuid1()
        self.circular: bool = False
    
    @property
    def origin(self) -> Station:
        """Get the first station on the line."""
        return self.stations[0]
    
    @property
    def destination(self) -> Station:
        """Get the last station on the line."""
        return self.stations[-1]
    
    def get_station_types(self) -> Set[StationType]:
        """Get all unique station types on this line."""
        return {station.station_type for station in self.stations}
    
    def add_station(self, station: Station) -> bool:
        """Add a station to the end of the line. Returns True if added, False if it creates invalid cycle."""
        # Check if connecting to first station (circular line)
        if len(self.stations) > 2 and station.id == self.stations[0].id:
            self.circular = True
            print(f"Line {self.id} is now circular")
            return True
        
        # Prevent adding station that's already in the middle of the line
        for i, existing_station in enumerate(self.stations[:-1]):
            if station.id == existing_station.id:
                print(f"Cannot add station - would create cycle in middle of line")
                return False
        
        # Allow re-adding the last station (extending from endpoint)
        if station.id == self.stations[-1].id:
            return False
        
        self.stations.append(station)
        return True
    
    def make_circular(self) -> None:
        """Make the line circular (trains loop back to start). Only works if 3+ stations."""
        if len(self.stations) >= 3:
            self.circular = True
        
    def render(self, screen: pygame.Surface) -> None:
        """Render the line segments connecting all stations."""
        for i in range(len(self.stations) - 1):
            pygame.draw.line(
                screen,
                self.color,
                (self.stations[i].x, self.stations[i].y),
                (self.stations[i + 1].x, self.stations[i + 1].y),
                self.width
            )
        
        if self.circular and len(self.stations) > 2:
            pygame.draw.line(
                screen,
                self.color,
                (self.stations[-1].x, self.stations[-1].y),
                (self.stations[0].x, self.stations[0].y),
                self.width
            )