from uuid import uuid1, UUID

from TypeEnums import StationType

# Design constants
RIDER_PATIENCE: float = 30.0

class Rider:
    """Represents a passenger waiting at a station."""
    
    def __init__(self, origin: UUID, destination: StationType):
        self.origin_id: UUID = origin
        self.destination_type: StationType = destination
        self.patience: float = RIDER_PATIENCE
        self.id: UUID = uuid1()