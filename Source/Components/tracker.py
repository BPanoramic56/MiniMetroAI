from dataclasses import dataclass, field
from typing import Set, Dict
from uuid import UUID

from typeEnums import StationType

@dataclass
class Tracker:
    """Tracks game-wide statistics for passengers."""
    total_passengers: int   = 0
    passengers_arrived: int = 0
    passengers_lost: int    = 0
    station_types: Set[StationType]     = field(default_factory=set)
    serviced_stations: Dict[UUID, int]  = field(default_factory=dict)