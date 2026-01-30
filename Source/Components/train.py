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
from resourceManager import resources

# Design constants
TRAIN_DWELL_TIME: float = 0.5

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

        self.current_station_index: int = 0
        self.distance_traveled: float = 0.0
        self.segment_distances: List[float] = self._calculate_all_segment_distances()
        self.total_line_distance: float = sum(self.segment_distances)
        
        self.id: UUID = uuid1()
        self.forward: bool = True
        self.at_station: bool = True
        self.station_arrival_time: float = time.time()
        self.station_parked: Station = self.line.stations[0]
        
        self.tracker = tracker
    
    def _calculate_all_segment_distances(self) -> List[float]:
        """Calculate distances for all segments in the line."""
        distances = []
        for i in range(len(self.line.stations) - 1):
            origin = self.line.stations[i]
            destination = self.line.stations[i + 1]
            dx = destination.x - origin.x
            dy = destination.y - origin.y
            distances.append(math.sqrt(dx * dx + dy * dy))
        
        # Add closing segment for circular lines
        if self.line.circular and len(self.line.stations) > 2:
            origin = self.line.stations[-1]
            destination = self.line.stations[0]
            dx = destination.x - origin.x
            dy = destination.y - origin.y
            distances.append(math.sqrt(dx * dx + dy * dy))
        
        return distances
    
    def _get_current_segment_index(self) -> int:
        """Get which segment the train is currently on based on distance traveled."""
        cumulative = 0.0
        for i, segment_dist in enumerate(self.segment_distances):
            cumulative += segment_dist
            if self.distance_traveled < cumulative:
                return i
        return len(self.segment_distances) - 1
    
    def _get_station_at_distance(self, distance: float) -> Tuple[int, bool]:
        """Check if train is at a station at the given distance. Returns (station_index, at_station)."""
        cumulative = 0.0
        tolerance = self.speed * 0.5
        
        for i, segment_dist in enumerate(self.segment_distances):
            # Check if at station i (start of segment)
            if abs(distance - cumulative) < tolerance:
                return (i, True)
            cumulative += segment_dist
        
        # Check if at final station
        if abs(distance - cumulative) < tolerance:
            if self.line.circular:
                return (0, True)
            else:
                return (len(self.line.stations) - 1, True)
        
        return (-1, False)
    
    def update(self) -> None:
        """Update train position along the line."""
        if self.at_station:
            if time.time() - self.station_arrival_time - (min(len(self.station_parked.riders), self.capacity) * 0.5) >= TRAIN_DWELL_TIME:
                self.at_station = False
            else:
                # Unload passengers at their destination
                remaining_riders = [rider for rider in self.riders if rider.destination_type != self.station_parked.station_type]
                unloaded_count = len(self.riders) - len(remaining_riders)
                self.riders = remaining_riders
                
                if self.tracker and unloaded_count > 0:
                    self.tracker.passengers_arrived += unloaded_count
                
                # Load new passengers up to capacity (only those we can deliver)
                riders_checked = 0
                while len(self.riders) < self.capacity and riders_checked < len(self.station_parked.riders):
                    rider: Rider = self.station_parked.riders[riders_checked]
                    
                    if rider.destination_type in self.line.get_station_types():
                        # Take this rider
                        self.riders.append(self.station_parked.riders.pop(riders_checked))
                        print(f"{len(self.riders)} aboard train")
                    else:
                        # Skip this rider, check next one
                        riders_checked += 1
                return
        
        # Move the train
        if self.forward:
            self.distance_traveled += self.speed
            
            # Check for arrival at station
            station_index, arrived = self._get_station_at_distance(self.distance_traveled)
            if arrived and station_index != self.current_station_index:
                self.current_station_index = station_index
                self._arrive_at_station(self.line.stations[station_index])
            
            # Check if reached end of line
            if self.distance_traveled >= self.total_line_distance:
                if self.line.circular:
                    # Loop back to start for circular lines
                    self.distance_traveled = 0.0
                    self.current_station_index = 0
                    self._arrive_at_station(self.line.stations[0])
                else:
                    # Reverse direction for non-circular lines
                    self.distance_traveled = self.total_line_distance
                    self.forward = False
                    self.current_station_index = len(self.line.stations) - 1
                    if not self.at_station:
                        self._arrive_at_station(self.line.stations[-1])
        else:
            self.distance_traveled -= self.speed
            
            # Check for arrival at station
            station_index, arrived = self._get_station_at_distance(self.distance_traveled)
            if arrived and station_index != self.current_station_index:
                self.current_station_index = station_index
                self._arrive_at_station(self.line.stations[station_index])
            
            # Check if reached start of line
            if self.distance_traveled <= 0.0:
                self.distance_traveled = 0.0
                self.forward = True
                self.current_station_index = 0
                if not self.at_station:
                    self._arrive_at_station(self.line.stations[0])
    
    def _arrive_at_station(self, station) -> None:
        """Handle train arriving at a station (unload/load passengers)."""
        self.at_station = True
        self.station_parked = station
        self.station_arrival_time = time.time()
        print(f"Train arrived at {station.describe()}")
    
    def get_position(self) -> Tuple[int, int]:
        """Calculate current position based on distance traveled along the entire line."""
        if self.total_line_distance == 0:
            return (self.line.stations[0].x, self.line.stations[0].y)
        
        # Find which segment we're on
        current_segment = self._get_current_segment_index()
        
        # Calculate distance from start of current segment
        distance_before_segment = sum(self.segment_distances[:current_segment])
        distance_in_segment = self.distance_traveled - distance_before_segment
        
        # Get origin and destination of current segment
        if current_segment >= len(self.line.stations) - 1 and self.line.circular:
            origin = self.line.stations[-1]
            destination = self.line.stations[0]
        else:
            origin = self.line.stations[current_segment]
            if current_segment + 1 < len(self.line.stations):
                destination = self.line.stations[current_segment + 1]
            else:
                return (origin.x, origin.y)
        
        # Interpolate position within segment
        segment_length = self.segment_distances[current_segment]
        if segment_length == 0:
            return (origin.x, origin.y)
        
        t = distance_in_segment / segment_length
        x = int(origin.x + t * (destination.x - origin.x))
        y = int(origin.y + t * (destination.y - origin.y))
        return (x, y)
    
    def get_direction_angle(self) -> float:
        """Calculate the angle the train is pointing (in degrees)."""
        if self.total_line_distance == 0:
            return 0.0
        
        # Find which segment we're on
        current_segment = self._get_current_segment_index()
        
        # Get origin and destination of current segment
        if current_segment >= len(self.line.stations) - 1 and self.line.circular:
            origin = self.line.stations[-1]
            destination = self.line.stations[0]
        else:
            origin = self.line.stations[current_segment]
            if current_segment + 1 < len(self.line.stations):
                destination = self.line.stations[current_segment + 1]
            else:
                # At the end, use previous segment direction
                if current_segment > 0:
                    origin = self.line.stations[current_segment - 1]
                    destination = self.line.stations[current_segment]
                else:
                    return 0.0
        
        # Calculate angle from origin to destination
        dx = destination.x - origin.x
        dy = destination.y - origin.y
        
        # atan2 returns angle in radians, convert to degrees
        # Note: pygame uses (0, 0) at top-left, so y increases downward
        angle = math.degrees(math.atan2(dy, dx))
        
        # If going backward, flip the angle 180 degrees
        if not self.forward:
            angle += 180
            
        angle += 90
        
        return angle
    
    def render(self, screen: pygame.Surface) -> None:
        """Render the train at its current position."""
        x, y = self.get_position()
        
        # Try to render sprite first
        sprite = resources.get_train_sprite(self.type, TRAIN_SIZE)
        if sprite and resources.use_sprites:
            # Get direction angle and rotate sprite
            angle = self.get_direction_angle()
            # Negative angle because pygame rotates counter-clockwise but our angle is clockwise
            rotated_sprite = pygame.transform.rotate(sprite, -angle)
            rect = rotated_sprite.get_rect(center=(x, y))
            screen.blit(rotated_sprite, rect)
        else:
            # Fallback to colored rectangle (doesn't rotate)
            rect = pygame.Rect(x - TRAIN_SIZE, y - TRAIN_SIZE, TRAIN_SIZE * 2, TRAIN_SIZE * 2)
            pygame.draw.rect(screen, TRAIN_COLOR[self.type], rect)
         
        rider_x = x + 20
        for rider in self.riders:
            rider.render(screen, rider_x, y - 18)
            rider_x += 15