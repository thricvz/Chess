import pygame as pg 
from modules import Board , Pawn
import random
pg.init()                                      #initiates a pygame instance
board = Board()
board.generate_pieces()

sel = board.board_state["a2"]
print(sel)

running = True                                  #variable checks if loop should go on
while running:                                  #game loop
    for event in pg.event.get():
        if event.type == pg.QUIT:               #Once exited the instance gets killed
            running = False
    #game logic
    board.build()

    pg.display.update()
pg.quit()


