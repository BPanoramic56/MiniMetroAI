from enum import Enum

class StationType(Enum):
    """Types of stations with different shapes."""
    Circle = 0
    Triangle = 1
    Square = 2
    
# TODO: Possible later implementations
# class LineType(Enum):
#     Regular = 1
#     Express = 2
#     HighCapacity = 3