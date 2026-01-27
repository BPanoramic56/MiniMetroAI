from line import Line
from station import Station, StationType

RIDER_PATIENCE: float = 30.0 # Amount of time a rider will wait for a train. In the game, getting this to zero results in a loss, let's implement that later

class Rider:
    def __init__(self, origin: Station, destination: StationType):
        self.origin: Station = origin,
        self.destination: StationType = destination
        self.patience: float = RIDER_PATIENCE