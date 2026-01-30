from enum import Enum

class StationType(Enum):
    """Types of stations with different shapes."""
    Circle      = 0
    Triangle    = 1
    Square      = 2
    Cross       = 3
    Pentagon    = 4
    Hexagon     = 5
    
class TrainType(Enum):
    Regular = 0
    Express = 1
    HighCapacity = 2
    
    @property
    def capacity(self) -> int: 
        return {
            TrainType.Regular: 5,
            TrainType.Express: 5,
            TrainType.HighCapacity: 10,
        }[self]
    
    @property
    def speed(self) -> float:
        return {
            TrainType.Regular: 4.0,
            TrainType.Express: 8.0, 
            TrainType.HighCapacity: 3.0,
        }[self]
        
    @property
    def acceleration(self) -> float:
        return {
            TrainType.Regular: 0.025,
            TrainType.Express: 0.05, # Very high, but the acceleration makes it fair
            TrainType.HighCapacity: 0.025,
        }[self]

class GameSpeed(Enum):
    Regular = 1
    TwoStep = 2
    FourStep = 4