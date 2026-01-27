import pygame

from station import Station
from random import randint

line_colors: list[tuple] = [
	(255, 150, 150),
	(150, 255, 150),
	(150, 150, 255)
]

class Line:
	def __init__(self, origin: Station, destination: Station):
		self.origin: Station = origin
		self.destination: Station = destination
		self.color = line_colors[randint(0, len(line_colors)- 1)]
		self.width = 10
        
	def render(self, screen: pygame.Surface):
		pygame.draw.line(screen, self.color, (self.origin.x, self.origin.y), (self.destination.x, self.destination.y), self.width)