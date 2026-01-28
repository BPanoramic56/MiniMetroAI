from dataclasses import dataclass


@dataclass
class Tracker:
    """Tracks game-wide statistics for passengers."""
    total_passengers: int = 0
    passengers_arrived: int = 0
    passengers_lost: int = 0