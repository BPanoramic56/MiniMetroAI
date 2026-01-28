from dataclasses import dataclass
from typing import Set

from typeEnums import StationType

# @dataclass
class Tracker:
    """Tracks game-wide statistics for passengers."""
    total_passengers: int = 0
    passengers_arrived: int = 0
    passengers_lost: int = 0
    station_types: Set[StationType] = set()