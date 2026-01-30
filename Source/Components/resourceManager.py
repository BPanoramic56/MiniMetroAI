import pygame
import os

from typing import Dict, Tuple, Optional
from pathlib import Path

from typeEnums import StationType, TrainType

# Resource paths
ASSETS_DIR: Path = Path("Source/Assets/Images")
SPRITES_DIR: Path = ASSETS_DIR / "Sprites"
BACKGROUNDS_DIR: Path = ASSETS_DIR / "Backgrounds"

# Station sprite paths
STATION_SPRITES: Dict[StationType, str] = {
    StationType.Circle: "circle.png",
    StationType.Triangle: "triangle.png",
    StationType.Square: "square.png",
    StationType.Cross: "cross.png",
    StationType.Pentagon: "pentagon.png",
    StationType.Hexagon: "hexagon.png",
}

# Train sprite paths
TRAIN_SPRITES: Dict[TrainType, str] = {
    TrainType.Regular: "train_regular.png",
    TrainType.Express: "train_express.png",
    TrainType.HighCapacity: "train_highcap.png",
}

# Rider sprite paths
RIDER_SPRITES: Dict[StationType, str] = {
    StationType.Circle: "circle.png",
    StationType.Triangle: "triangle.png",
    StationType.Square: "square.png",
    StationType.Cross: "cross.png",
    StationType.Pentagon: "pentagon.png",
    StationType.Hexagon: "hexagon.png",
}


class ResourceManager:
    """Manages loading and caching of game sprites and images."""
    
    def __init__(self):
        self.station_sprites: Dict[StationType, pygame.Surface] = {}
        self.train_sprites: Dict[TrainType, pygame.Surface] = {}
        self.rider_sprites: Dict[StationType, pygame.Surface] = {}
        self.background: Optional[pygame.Surface] = self.load_background()
        self.use_sprites: bool = False
        self._sprites_loaded: bool = False
        
        self._ensure_directories()
    
    def _ensure_directories(self) -> None:
        """Create asset directories if they don't exist."""
        SPRITES_DIR.mkdir(parents=True, exist_ok=True)
        BACKGROUNDS_DIR.mkdir(parents=True, exist_ok=True)
    
    def _load_sprites(self) -> None:
        """Load all sprite images from the assets directory. Called lazily after pygame init."""
        if self._sprites_loaded:
            return
        
        try:
            # Load station sprites
            for station_type, filename in STATION_SPRITES.items():
                path = SPRITES_DIR / filename
                if path.exists():
                    self.station_sprites[station_type] = pygame.image.load(str(path)).convert_alpha()
            
            # Load train sprites
            for train_type, filename in TRAIN_SPRITES.items():
                path = SPRITES_DIR / filename
                if path.exists():
                    self.train_sprites[train_type] = pygame.image.load(str(path)).convert_alpha()
            
            # Load rider sprites
            for rider_type, filename in RIDER_SPRITES.items():
                path = SPRITES_DIR / filename
                if path.exists():
                    self.rider_sprites[rider_type] = pygame.image.load(str(path)).convert_alpha()
            
            # Check if we have enough sprites to use sprite mode
            self.use_sprites = (len(self.station_sprites) > 0 or 
                               len(self.train_sprites) > 0 or 
                               len(self.rider_sprites) > 0)
            
            self._sprites_loaded = True
            
            if self.use_sprites:
                print(f"Loaded {len(self.station_sprites)} station sprites, {len(self.train_sprites)} train sprites, {len(self.rider_sprites)} rider sprites")
        except Exception as e:
            print(f"Error loading sprites: {e}")
            self.use_sprites = False
    
    def load_background(self) -> bool:
        """Load a background image."""
        filename = "back.png"
        path = BACKGROUNDS_DIR / filename
        if path.exists():
            try:
                self.background = pygame.image.load(str(path)).convert()
                print(f"Loaded background: {filename}")
                return True
            except Exception as e:
                print(f"Error loading background: {e}")
        return False
    
    def get_station_sprite(self, station_type: StationType, size: int) -> Optional[pygame.Surface]:
        """Get scaled station sprite for given type."""
        if not self._sprites_loaded:
            self._load_sprites()
        
        if station_type in self.station_sprites:
            sprite = self.station_sprites[station_type]
            return pygame.transform.scale(sprite, (size * 2, size * 2))
        return None
    
    def get_train_sprite(self, train_type: TrainType, size: int) -> Optional[pygame.Surface]:
        """Get scaled train sprite for given type."""
        if not self._sprites_loaded:
            self._load_sprites()
        
        if train_type in self.train_sprites:
            sprite = self.train_sprites[train_type]
            return pygame.transform.scale(sprite, (size * 2, size * 2))
        return None
    
    def get_rider_sprite(self, destination_type: StationType, size: int) -> Optional[pygame.Surface]:
        """Get scaled rider sprite for given destination type."""
        if not self._sprites_loaded:
            self._load_sprites()
        
        if destination_type in self.rider_sprites:
            sprite = self.rider_sprites[destination_type]
            return pygame.transform.scale(sprite, (size * 2, size * 2))
        return None
    
    def get_background(self, screen_size: Tuple[int, int]) -> Optional[pygame.Surface]:
        """Get background scaled to screen size."""
        if self.background:
            return pygame.transform.scale(self.background, screen_size)
        return None


# Global resource manager instance
resources = ResourceManager()