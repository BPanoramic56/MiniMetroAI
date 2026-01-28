import math
import pygame

from typeEnums import StationType

class CustomShape:
    @staticmethod
    def regular_polygon(sides, size):
        radius = size / 2
        points = []

        for i in range(sides):
            angle = 2 * math.pi * i / sides - math.pi / 2
            x = math.cos(angle) * radius
            y = math.sin(angle) * radius
            points.append((x, y))

        return points

    @staticmethod
    def pentagon(size):
        return CustomShape.regular_polygon(5, size)

    @staticmethod
    def hexagon(size):
        return CustomShape.regular_polygon(6, size)

    @staticmethod
    def star(size):
        outer = size / 2
        inner = outer * 0.381966

        points = []
        step = math.pi / 5

        for i in range(10):
            radius = outer if i % 2 == 0 else inner
            angle = i * step - math.pi / 2
            x = math.cos(angle) * radius
            y = math.sin(angle) * radius
            points.append((x, y))

        return points

    @staticmethod
    def cross(size, width):
        s = size / 2
        w = width / 2

        return [
            (-w, -s), (w, -s),
            (w, -w), (s, -w),
            (s, w), (w, w),
            (w, s), (-w, s),
            (-w, w), (-s, w),
            (-s, -w), (-w, -w)
        ]

    @staticmethod
    def draw(surface, color, shape_points, position):
        px, py = position
        translated = [(x + px, y + py) for x, y in shape_points]
        pygame.draw.polygon(surface, color, translated)

    @staticmethod
    def render_shape(screen: pygame.Surface, x, y, type, size = 10, width = 5, color = (255, 0, 0)):
        if type == StationType.Circle:
            pygame.draw.circle(screen, color, (x, y), size)
            
        elif type == StationType.Triangle:
            points = [
                (x, y - size),
                (x - size, y + size),
                (x + size, y + size)
            ]
            pygame.draw.polygon(screen, color, points)
            
        elif type == StationType.Square:
            rect = pygame.Rect(x - size, y - size, size * 2, size * 2)
            pygame.draw.rect(screen, color, rect)
        
        elif type == StationType.Cross:
            cross = CustomShape.cross(size * 2, 5)
            CustomShape.draw(screen, color, cross, (x, y))
        
        elif type == StationType.Hexagon:
            hexagon = CustomShape.hexagon(size * 2)
            CustomShape.draw(screen, color, hexagon, (x, y))
            
        elif type == StationType.Pentagon:
            pentagon = CustomShape.pentagon(size * 2)
            CustomShape.draw(screen, color, pentagon, (x, y))
            
        elif type == StationType.Star:
            star = CustomShape.star(size * 2)
            CustomShape.draw(screen, color, star, (x, y))