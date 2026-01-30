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
    station_service_dict: Dict[UUID, Set[StationType]] = field(default_factory=dict)
    line_service_dict: Dict[UUID, Set[StationType]] = field(default_factory=dict)
    
def generate_mermaid_graph(tracker: Tracker) -> str:
    """
    Generate a mermaid graph showing lines and stations connected by serviced types.
    """
    mermaid_lines = ["graph TD"]

    # Connect lines to service types
    for line_id, service_types in tracker.line_service_dict.items():
        line_node = f"Line_{str(line_id).replace('-', '')}"
        for stype in service_types:
            service_node = f"Type_{stype}"
            mermaid_lines.append(f"{line_node} --> {service_node}")

    # Connect stations to service types
    for station_id, service_types in tracker.station_service_dict.items():
        station_node = f"Station_{str(station_id).replace('-', '')}"
        for stype in service_types:
            service_node = f"Type_{stype}"
            mermaid_lines.append(f"{station_node} --> {service_node}")

    return "\n".join(mermaid_lines)