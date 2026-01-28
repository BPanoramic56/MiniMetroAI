import pygame
import time
import math

from typing import List, Tuple, Dict
from uuid import uuid1, UUID
from random import randint

from line import Line
from rider import Rider
from station import Station
from typeEnums import TrainType
from tracker import Tracker

# Design constants
TRAIN_DWELL_TIME: float = 2.0

# Visual constants
TRAIN_SIZE: int = 12
TRAIN_COLOR: Dict[TrainType, Tuple[int, int, int]] = {
	TrainType.Regular: (112, 238, 156),
	TrainType.Express: (67, 67, 113),
	TrainType.HighCapacity: (90, 24, 7)
}


class Train:
    """Represents a train traveling along a line between stations."""
    
    def __init__(self, line: Line, type: TrainType = TrainType.Regular, tracker: Tracker = None):
        self.line: Line = line
        self.riders: List[Rider] = []
        self.type: TrainType = type
        self.capacity = type.capacity
        self.speed = type.speed

        self.distance_traveled: float = 0.0
        self.total_distance: float = self._calculate_line_distance()
        self.id: UUID = uuid1()
        self.forward: bool = True
        self.at_station: bool = False
        self.station_arrival_time: float = 0.0
        self.station_parked: Station = None
        
        self.tracker = tracker
    
    def _calculate_line_distance(self) -> float:
        """Calculate the total distance between origin and destination."""
        dx = self.line.destination.x - self.line.origin.x
        dy = self.line.destination.y - self.line.origin.y
        return math.sqrt(dx * dx + dy * dy)
    
    def update(self) -> None:
        """Update train position along the line."""
        if self.at_station:
            if time.time() - self.station_arrival_time >= TRAIN_DWELL_TIME:
                self.at_station = False
            else:
                new_rider_list: List[Rider] = self.riders
                for rider in self.riders:
                    if rider.destination_type == self.station_parked.station_type:
                        new_rider_list.remove(rider)
                        if self.tracker:
                            self.tracker.passengers_arrived += 1
                self.riders = new_rider_list
                while len(self.riders) < self.capacity and len(self.station_parked.riders) != 0:
                    self.riders.append(self.station_parked.riders.pop(0))
                    print(f"{len(self.riders)} aboard {self.id}")
                return
        
        if self.forward:
            self.distance_traveled += self.speed
            if self.distance_traveled >= self.total_distance:
                self.distance_traveled = self.total_distance
                self.forward = False
                self._arrive_at_station(self.line.destination)
        else:
            self.distance_traveled -= self.speed
            if self.distance_traveled <= 0.0:
                self.distance_traveled = 0.0
                self.forward = True
                self._arrive_at_station(self.line.origin)
    
    def _arrive_at_station(self, station) -> None:
        """Handle train arriving at a station (unload/load passengers)."""
        self.at_station = True
        self.station_parked = station
        self.station_arrival_time = time.time()
        print(f"Train arrived at {station.describe()}")
    
    def get_position(self) -> Tuple[int, int]:
        """Calculate current position based on distance traveled along the line."""
        if self.total_distance == 0:
            return (self.line.origin.x, self.line.origin.y)
        
        t = self.distance_traveled / self.total_distance
        x = int(self.line.origin.x + t * (self.line.destination.x - self.line.origin.x))
        y = int(self.line.origin.y + t * (self.line.destination.y - self.line.origin.y))
        return (x, y)
    
    def render(self, screen: pygame.Surface) -> None:
        """Render the train at its current position."""
        x, y = self.get_position()
        rect = pygame.Rect(x - TRAIN_SIZE, y - TRAIN_SIZE, TRAIN_SIZE * 2, TRAIN_SIZE * 2)
        pygame.draw.rect(screen, TRAIN_COLOR[self.type], rect)
         
        rider_x = x + 20
        
        for rider in self.riders:
            rider.render(screen, rider_x, y - 18)
            rider_x += 15