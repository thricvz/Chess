import pygame as pg 
from modules import Board,Piece
import random
pg.init()                                      #initiates a pygame instance
board = Board((512,512))
#board.generate_pieces()
board.board_state["g1"] = Piece("knight","white")
board.board_state["e7"] = Piece("queen","white")
running = True                                  #variable checks if loop should go on
while running:                                  #game loop
    for event in pg.event.get():
        if event.type == pg.QUIT:               #Once exited the instance gets killed
            running = False 
            
    #gamelogic   
    board.build()
    if board.clicked():
        board.predict()

    pg.display.flip()
pg.quit()


