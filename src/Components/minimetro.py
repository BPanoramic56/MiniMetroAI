import pygame
import time
import math

from pygame.math import Vector2
from random import randint
from typing import List, Optional, Tuple, Dict, Set
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
SIDEBAR_WIDTH: int = 100

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
    "UI_TEXT_COLOR":    (27, 82, 153),
    "SIDEBAR_BG":       (30, 30, 30)
}

# Line color display constants
LINE_COLOR_SIZE: int = 40
LINE_COLOR_SELECTED_SIZE: int = 50
LINE_COLOR_PADDING: int = 10


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
        
        self.station_spawn_interval: float = STATION_SPAWN_INTERVAL
        
        self.lines: List[Line] = []
        self.trains: List[Train] = []

        self.lines_available: Set[Tuple[int, int, int]]= set([
            (255, 0, 0),
            (0, 255, 0),
            (0, 0, 255)
        ])
        
        self.tracker = Tracker()
    
    def get_elapsed_time(self) -> float:
        """Get time elapsed since game start in seconds."""
        return time.time() - self.start_time
    
    def should_auto_spawn(self) -> bool:
        """Check if enough time has passed for automatic station spawn."""
        return time.time() - self.last_spawn_time >= self.station_spawn_interval
    
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
        
        # Render sidebar
        self._render_sidebar()
        
        # Render UI bar
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
    
    def _render_sidebar(self) -> None:
        """Render the sidebar with line colors."""
        # Draw sidebar background
        sidebar_rect = pygame.Rect(WIDTH - SIDEBAR_WIDTH, 0, SIDEBAR_WIDTH, HEIGHT - UI_HEIGHT)
        pygame.draw.rect(self.screen, COLORS["SIDEBAR_BG"], sidebar_rect)
        pygame.draw.line(self.screen, COLORS["UI_LINE_COLOR"], (WIDTH - SIDEBAR_WIDTH, 0), (WIDTH - SIDEBAR_WIDTH, HEIGHT - UI_HEIGHT), 2)
        
        # Draw line color indicators
        y_offset = LINE_COLOR_PADDING
        for line in self.lines:
            size = LINE_COLOR_SELECTED_SIZE if line.selected else LINE_COLOR_SIZE
            x_center = WIDTH - SIDEBAR_WIDTH // 2
            y_center = y_offset + size // 2
            
            # Draw circle for line color
            pygame.draw.circle(self.screen, line.color, (x_center, y_center), size // 2)
            
            # Draw border if selected
            if line.selected:
                pygame.draw.circle(self.screen, (255, 255, 255), (x_center, y_center), size // 2, 3)
            
            y_offset += size + LINE_COLOR_PADDING
    
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
            x = randint(STATION_SPACING, WIDTH - SIDEBAR_WIDTH - STATION_SPACING)
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
        self.tracker.station_types.add(type)
        self.tracker.serviced_stations[station.id] = 0
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
            if (origin.id == line.origin.id and destination.id == line.destination.id) or (origin.id == line.destination.id and destination.id == line.origin.id):
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
            for station in line_to_remove.stations:
                self.tracker.serviced_stations[station.id] -= 1
            
            if line_to_remove.circular:
                self.tracker.serviced_stations[line_to_remove.stations[0].id] -= 1
                
            self.lines.remove(line_to_remove)
            self.trains = [train for train in self.trains if train.line.id != line_id]
                
            self.lines_available.add(line.color)
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
        """Check if a location has been clicked and handle station/line/sidebar interactions."""
        x, y = location
        
        # Check sidebar first (highest priority)
        if x >= WIDTH - SIDEBAR_WIDTH:
            self._check_sidebar_click(location)
            return
        
        # Check if a station was clicked
        clicked_station = self._get_station_at_position(location)
        if clicked_station:
            self._handle_station_click(clicked_station)
            return
        
        # Check if a line was clicked
        clicked_line = self._get_line_at_position(location)
        if clicked_line:
            self._handle_line_click(clicked_line)
            return
        
        # Nothing was clicked - deselect everything
        self.selected_station = None
        if self.selected_line:
            self.selected_line.selected = False
            self.selected_line = None
    
    def _get_station_at_position(self, location: Tuple[int, int]) -> Optional[Station]:
        """Get station at the given position, or None if no station there."""
        x, y = location
        for station in self.stations:
            if (x + CLICK_SPACING >= station.x and x - CLICK_SPACING <= station.x and
                y + CLICK_SPACING >= station.y and y - CLICK_SPACING <= station.y):
                return station
        return None
    
    def _get_line_at_position(self, location: Tuple[int, int]) -> Optional[Line]:
        """Get line at the given position using line segment distance check."""
        for line in self.lines:
            for i in range(len(line.stations) - 1):
                origin = (line.stations[i].x, line.stations[i].y)
                destination = (line.stations[i + 1].x, line.stations[i + 1].y)
                
                if self._point_near_line_segment(location, origin, destination, tolerance=10):
                    return line
            
            # Check circular closing segment
            if line.circular and len(line.stations) > 2:
                origin = (line.stations[-1].x, line.stations[-1].y)
                destination = (line.stations[0].x, line.stations[0].y)
                
                if self._point_near_line_segment(location, origin, destination, tolerance=10):
                    return line
        
        return None
    
    def _point_near_line_segment(self, point: Tuple[int, int], p1: Tuple[int, int], p2: Tuple[int, int], tolerance: int = 10) -> bool:
        """Check if a point is within tolerance distance of a line segment."""
        px, py = point
        x1, y1 = p1
        x2, y2 = p2
        
        # Vector from p1 to p2
        dx = x2 - x1
        dy = y2 - y1
        
        # Handle zero-length segment
        length_squared = dx * dx + dy * dy
        if length_squared == 0:
            dist = math.sqrt((px - x1) ** 2 + (py - y1) ** 2)
            return dist <= tolerance
        
        # Project point onto line, clamped to segment
        t = max(0, min(1, ((px - x1) * dx + (py - y1) * dy) / length_squared))
        
        # Find closest point on segment
        closest_x = x1 + t * dx
        closest_y = y1 + t * dy
        
        # Check distance
        dist = math.sqrt((px - closest_x) ** 2 + (py - closest_y) ** 2)
        return dist <= tolerance
    
    def _handle_station_click(self, station: Station) -> None:
        """Handle clicking on a station."""
        if self.selected_station:
            if station.id == self.selected_station.id:
                # Clicking same station - deselect
                self.selected_station = None
            else:
                # Connecting to another station
                self._connect_stations(self.selected_station, station)
        else:
            # Select this station
            print(f"Station clicked: {station.describe()}")
            self.selected_station = station
    
    def _connect_stations(self, origin: Station, destination: Station) -> None:
        """Connect two stations with a line or extend existing line."""
        # Check if we should extend an existing line
        line_to_extend = None
        for line in self.lines:
            if line.destination.id == origin.id and not line.circular:
                line_to_extend = line
                break
        
        if line_to_extend:
            # Extend the existing line
            if line_to_extend.add_station(destination):
                # Recalculate distances for trains on this line
                for train in self.trains:
                    if train.line.id == line_to_extend.id:
                        train.segment_distances = train._calculate_all_segment_distances()
                        train.total_line_distance = sum(train.segment_distances)
                print(f"Extended line to {destination.type()}")
                self.selected_station = destination
                self.tracker.serviced_stations[destination.id] += 1
            else:
                print("Cannot extend line here")
                self.selected_station = None
        elif self.check_line(origin, destination):
            # Create new line
            if len(self.lines_available) == 0:
                return
            new_line_color = self.lines_available.pop()
            new_line = Line([origin, destination], new_line_color)
            self.tracker.serviced_stations[origin.id] += 1
            self.tracker.serviced_stations[destination.id] += 1
            self.lines.append(new_line)
            self.trains.append(Train(line=new_line, tracker=self.tracker))
            print(f"Created line and train between {origin.type()} and {destination.type()}")
            self.selected_station = destination
        else:
            self.selected_station = None
    
    def _handle_line_click(self, line: Line) -> None:
        """Handle clicking on a line."""
        # Deselect previous line
        if self.selected_line:
            self.selected_line.selected = False
        
        # Toggle selection
        if self.selected_line == line:
            self.selected_line = None
        else:
            line.selected = True
            self.selected_line = line
            print(f"Line selected: {line.id}")
    
    def _check_sidebar_click(self, location: Tuple[int, int]) -> None:
        """Check if a line color in the sidebar was clicked."""
        x, y = location
        
        y_offset = LINE_COLOR_PADDING
        for line in self.lines:
            size = LINE_COLOR_SELECTED_SIZE if line.selected else LINE_COLOR_SIZE
            x_center = WIDTH - SIDEBAR_WIDTH // 2
            y_center = y_offset + size // 2
            
            # Check if click is within circle
            dist = math.sqrt((x - x_center) ** 2 + (y - y_center) ** 2)
            if dist <= size // 2:
                if line.selected:
                    # Line was selected - delete it
                    self.delete_line(line.id)
                    print(f"Deleted line {line.id}")
                else:
                    # Deselect previous line
                    if self.selected_line:
                        self.selected_line.selected = False
                    
                    # Select this line
                    line.selected = True
                    self.selected_line = line
                    print(f"Line selected from sidebar: {line.id}")
                return
            
            y_offset += size + LINE_COLOR_PADDING