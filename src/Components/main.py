import pygame
import random

import minimetro

# Design constants
START_STATIONS: int = 3

metro: minimetro.MiniMetro = minimetro.MiniMetro()

if __name__ == "__main__":
    for _ in range(START_STATIONS):
        metro.create_station()
    
    running: bool = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    metro.create_station()
                elif event.key == pygame.K_t:
                    if metro.lines:
                        line = random.choice(metro.lines)
                        metro.trains.append(minimetro.Train(line))
                        print(f"Created train on line (Total: {len(metro.trains)})")
            elif event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                metro.check_location(pos)
        
        metro.update()
        metro.render()
        metro.clock.tick(minimetro.FPS)
    
    pygame.quit()