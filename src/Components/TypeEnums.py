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
            TrainType.Regular: 100,
            TrainType.Express: 200,
            TrainType.HighCapacity: 400,
        }[self]
    
    @property
    def speed(self) -> int:
        return {
            TrainType.Regular: 2.0,
            TrainType.Express: 3.2,
            TrainType.HighCapacity: 1.5,
        }[self]
    
# TODO: Possible later implementations
# class LineType(Enum):
#     Regular = 1
#     Express = 2
#     HighCapacity = 3