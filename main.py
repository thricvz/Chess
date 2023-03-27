import pygame as pg 
from modules import Board 
import random
pg.init()                                      #initiates a pygame instance
board = Board((512,512))
board.generate_pieces()

running = True                                  #variable checks if loop should go on
while running:                                  #game loop
    for event in pg.event.get():
        if event.type == pg.QUIT:               #Once exited the instance gets killed
            running = False 
            
    #gamelogic        
    board.get_clicked_case(event)
    board.build()

    pg.display.update()
pg.quit()


