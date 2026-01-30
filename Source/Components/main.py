import pygame
import random

from random import choice, randint

import minimetro

from typeEnums import TrainType, GameSpeed

# Design constants
START_STATIONS: int = 3

metro: minimetro.MiniMetro = minimetro.MiniMetro()
# speed: GameSpeed = GameSpeed.Regular

if __name__ == "__main__":
    for _ in range(START_STATIONS):
        metro.create_station()
    
    running: bool = True
    paused: bool = False
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    metro.create_station()
                elif event.key == pygame.K_ESCAPE:
                    paused = not paused
                elif event.key == pygame.K_t:
                    if metro.lines:
                        if metro.train_quantity < metro.max_trains:
                            line = random.choice(metro.lines)
                            metro.trains.append(minimetro.Train(line, TrainType(randint(0, len(TrainType) - 1))))
                            metro.train_quantity += 1
                            print(f"Created train on line (Total: {len(metro.trains)})")
                        else:
                            print("No trains available")
                elif event.key == pygame.K_p:
                    if metro.stations:
                        choice(metro.stations).create_passenger()
                elif event.key == pygame.K_r:
                    metro = minimetro.MiniMetro()
                    for _ in range(START_STATIONS):
                        metro.create_station()
                # elif event.key == pygame.K_SPACE:
                #     if speed == GameSpeed.Regular:
                #         metro.station_spawn_interval *= 0.5
                #         speed = GameSpeed.TwoStep
                #     elif speed == GameSpeed.TwoStep:
                #         metro.station_spawn_interval *= 0.5
                #         speed = GameSpeed.FourStep
                #     elif speed == GameSpeed.FourStep:
                #         metro.station_spawn_interval *= 4
                #         speed = GameSpeed.Regular
                        
            elif event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                metro.check_location(pos)
        
        if not paused:
            metro.update()
            metro.render()
            metro.clock.tick(minimetro.FPS)
    
    pygame.quit()