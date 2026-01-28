import pygame
import time

from random import randint
from typing import List, Optional, Tuple, Dict
from uuid import UUID

from station import Station
from line import Line
from train import Train
from tracker import Tracker
from typeEnums import StationType

# Fixed constants
WIDTH: int      = 800
HEIGHT: int     = 800
FPS: int        = 60
UI_HEIGHT: int  = 60

# Design constants
STATION_SPACING: int            = 80
STATION_SPAWN_INTERVAL: float   = 10.0
CLICK_SPACING: int              = 20
STATION_MAX: int                = 100

# Visual constants
COLORS: Dict[str, Tuple[int, int, int]] = {
    "BG_COLOR":         (14, 14, 14),
    "UI_COLOR":         (186, 167, 176),
    "UI_LINE_COLOR":    (11, 110, 79),
    "UI_TEXT_COLOR":    (27, 82, 153)
}


class MiniMetro:
    """Main game class for MiniMetro simulation."""
    
    def __init__(self):
        pygame.init()
        self.screen: pygame.Surface = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("MiniMetro")
        self.clock: pygame.time.Clock = pygame.time.Clock()
        self.font: pygame.font.Font = pygame.font.Font(None, 28)
        self.large_font: pygame.font.Font = pygame.font.Font(None, 36)
        
        self.stations: List[Station] = []
        self.start_time: float = time.time()
        self.last_spawn_time: float = time.time()
        self.selected_station: Optional[Station] = None
        self.selected_line: Optional[Line] = None
        
        self.lines: List[Line] = []
        self.trains: List[Train] = []

        self.tracker = Tracker()
    
    def get_elapsed_time(self) -> float:
        """Get time elapsed since game start in seconds."""
        return time.time() - self.start_time
    
    def should_auto_spawn(self) -> bool:
        """Check if enough time has passed for automatic station spawn."""
        return time.time() - self.last_spawn_time >= STATION_SPAWN_INTERVAL
    
    def render(self) -> None:
        """Render all game elements to screen."""
        self.screen.fill(COLORS["BG_COLOR"])
        
        # In order of background-to-foreground
        for line in self.lines:
            line.render(self.screen)
        for station in self.stations:
            station.render(self.screen, station == self.selected_station)
        for train in self.trains:
            train.render(self.screen)
        
        ui_rect = pygame.Rect(0, HEIGHT - UI_HEIGHT, WIDTH, UI_HEIGHT)
        pygame.draw.rect(self.screen, COLORS["UI_COLOR"], ui_rect)
        pygame.draw.line(self.screen, COLORS["UI_LINE_COLOR"], (0, HEIGHT - UI_HEIGHT), (WIDTH, HEIGHT - UI_HEIGHT), 2)
        
        elapsed = int(self.get_elapsed_time())
        info_text = self.font.render(
            f"Time: {elapsed}s  |  Stations: {len(self.stations)}",
            True,
            COLORS["UI_TEXT_COLOR"]
        )
        self.screen.blit(info_text, (20, HEIGHT - UI_HEIGHT + 18))
        
        info_text = self.font.render(
            f"Passengers: {self.tracker.total_passengers}  |  Arrived: {self.tracker.passengers_arrived} | Lost: {self.tracker.passengers_lost}",
            True,
            COLORS["UI_TEXT_COLOR"]
        )
        self.screen.blit(info_text, (300, HEIGHT - UI_HEIGHT + 18))
        
        pygame.display.flip()
    
    def is_valid_location(self, x: int, y: int) -> bool:
        """Check if location is valid (not too close to existing stations)."""
        for station in self.stations:
            distance = ((station.x - x) ** 2 + (station.y - y) ** 2) ** 0.5
            if distance < STATION_SPACING:
                return False
        return True
    
    def create_location(self) -> Tuple[int, int]:
        """Generate a valid random location for a new station."""
        max_attempts = 100
        attempt = 0
        
        while attempt < max_attempts:
            x = randint(STATION_SPACING, WIDTH - STATION_SPACING)
            y = randint(STATION_SPACING, HEIGHT - UI_HEIGHT - STATION_SPACING)
            
            if self.is_valid_location(x, y):
                return (x, y)
            
            attempt += 1
        
        return (WIDTH // 2, HEIGHT // 2)
    
    def create_station(self) -> None:
        """Create a new station at a valid location."""
        x, y = self.create_location()
        type: StationType = StationType(randint(0, len(StationType) - 1))
        station = Station(x, y, type, self.tracker)
        print(type)
        self.tracker.station_types.add(type)
        self.stations.append(station)
        
        self.last_spawn_time = time.time()
        print(f"Created ({len(self.stations)}): {station.describe()}")
    
    def update(self) -> None:
        """Update game state (auto-spawn stations)."""
        if self.should_auto_spawn() and len(self.stations) < STATION_MAX:
            self.create_station()
        for station in self.stations:
            station.update()
        for train in self.trains:
            train.update()
    
    def check_line(self, origin: Station, destination: Station) -> bool:
        """Check if a line between origin and destination already exists."""
        for line in self.lines:
            if (origin.id == line.origin.id and destination.id == line.destination.id) or \
               (origin.id == line.destination.id and destination.id == line.origin.id):
                return False
        return True
    
    def delete_line(self, line_id: UUID) -> bool:
        """Delete a line and all trains on that line."""
        line_to_remove = None
        for line in self.lines:
            if line.id == line_id:
                line_to_remove = line
                break
        
        if line_to_remove:
            self.lines.remove(line_to_remove)
            self.trains = [train for train in self.trains if train.line.id != line_id]
            print(f"Deleted line {line_id}")
            return True
        return False
    
    def delete_train(self, train_id: UUID) -> bool:
        """Delete a specific train."""
        train_to_remove = None
        for train in self.trains:
            if train.id == train_id:
                train_to_remove = train
                break
        
        if train_to_remove:
            self.trains.remove(train_to_remove)
            print(f"Deleted train {train_id}")
            return True
        return False
            
    def check_location(self, location: Tuple[int, int]) -> None:
        """Check if a location has been clicked and handle station/line interactions."""
        x, y = location
        spacing = CLICK_SPACING
        for station in self.stations:
            if x + spacing >= station.x and x - spacing <= station.x and \
               y + spacing >= station.y and y - spacing <= station.y:
                
                if self.selected_station:
                    if station.id != self.selected_station.id:
                        # Check if we should extend an existing line
                        line_to_extend = None
                        for line in self.lines:
                            if line.destination.id == self.selected_station.id and not line.circular:
                                line_to_extend = line
                                break
                        
                        if line_to_extend:
                            # Extend the existing line
                            if line_to_extend.add_station(station):
                                # Recalculate distances for trains on this line
                                for train in self.trains:
                                    if train.line.id == line_to_extend.id:
                                        train.segment_distances = train._calculate_all_segment_distances()
                                        train.total_line_distance = sum(train.segment_distances)
                                print(f"Extended line to {station.type()}")
                                self.selected_station = station
                            else:
                                print("Cannot extend line here")
                                self.selected_station = None
                        elif self.check_line(self.selected_station, station):
                            # Create new line
                            new_line = Line([self.selected_station, station])
                            self.lines.append(new_line)
                            self.trains.append(Train(line=new_line, tracker=self.tracker))
                            print(f"Created line and train between {self.selected_station.type()} and {station.type()}")
                            self.selected_station = station
                        else:
                            self.selected_station = None
                    else:
                        self.selected_station = None
                else:
                    print(f"Station clicked: {station.describe()}")
                    self.selected_station = station
                    break