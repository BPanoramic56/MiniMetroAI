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
            TrainType.HighCapacity: 8,
        }[self]
    
    @property
    def speed(self) -> int:
        return {
            TrainType.Regular: 4.0,
            TrainType.Express: 6.4,
            TrainType.HighCapacity: 3.2,
        }[self]
    
# TODO: Possible later implementations
# class LineType(Enum):
#     Regular = 1
#     Express = 2
#     HighCapacity = 3

class GameSpeed(Enum):
    Regular = 1
    TwoStep = 2
    FourStep = 4