import pygame
import time

from random import randint
from enum import Enum
from typing import Tuple

from station import Station
from line import Line

# Fixed constants
WIDTH: int      = 800
HEIGHT: int     = 800
FPS: int        = 60
UI_HEIGHT: int  = 60

# Design constants
STATION_SPACING: int            = 80
STATION_SPAWN_INTERVAL: float   = 10.0
CLICK_SPACING: int              = 10 # Half of STATION_SIZE seems to be enough

# Visual constants
COLORS = {
    "BG_COLOR":         (14, 14, 41),
    "UI_COLOR":         (186, 167, 176),
    "UI_LINE_COLOR":    (11, 110, 79),
    "UI_TEXT_COLOR":    (27, 82, 153)
}

class MiniMetro:
    """Main game class for MiniMetro simulation."""
    
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("MiniMetro")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 28)
        self.large_font = pygame.font.Font(None, 36)
        
        self.stations: list[Station] = []
        self.start_time: float = time.time()
        self.last_spawn_time: float = time.time()
        self.selected_station: Station = None
        
        self.lines: list[Line] = []
    
    def get_elapsed_time(self) -> float:
        """Get time elapsed since game start in seconds."""
        return time.time() - self.start_time
    
    def should_auto_spawn(self) -> bool:
        """Check if enough time has passed for automatic station spawn."""
        return time.time() - self.last_spawn_time >= STATION_SPAWN_INTERVAL
    
    def render(self) -> None:
        """Render all game elements to screen."""
        self.screen.fill(COLORS["BG_COLOR"])
        
        for line in self.lines:
            line.render(self.screen)
        for station in self.stations:
            station.render(self.screen, station == self.selected_station)
        
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
        station = Station(x, y)
        self.stations.append(station)
        self.last_spawn_time = time.time()
        print(f"Created ({len(self.stations)}): {station.describe()}")
    
    def update(self) -> None:
        """Update game state (auto-spawn stations)."""
        if self.should_auto_spawn():
            self.create_station()
    
    def check_line(self, origin: Station, destination: Station):
        for line in self.lines:
            if (origin.id == line.origin.id and destination.id == line.destination.id) or (origin.id == line.destination.id and destination.id == line.origin.id):
                return False
        return True
            
    def check_location(self, location):
        x, y = location
        spacing = CLICK_SPACING
        for station in self.stations:
            if x + spacing >= station.x and x - spacing <= station.x and y + spacing >= station.y and y - spacing <= station.y:
                
                if self.selected_station and station.id != self.selected_station.id:
                    if self.check_line(self.selected_station, station):
                        self.lines.append(Line(self.selected_station, station))
                        self.selected_station = None
                        break
                else:
                    print(f"Station cliked: {station.describe()}")
                    self.selected_station = station
                    break