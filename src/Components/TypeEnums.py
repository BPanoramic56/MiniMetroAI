from enum import Enum

class StationType(Enum):
    """Types of stations with different shapes."""
    Circle = 0
    Triangle = 1
    Square = 2
    
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
    def speed(self) -> int:
        return {
            TrainType.Regular: 4.0,
            TrainType.Express: 6.4,
            TrainType.HighCapacity: 2.0,
        }[self]
    
# TODO: Possible later implementations
# class LineType(Enum):
#     Regular = 1
#     Express = 2
#     HighCapacity = 3