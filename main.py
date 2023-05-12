import pygame as pg 
from modules import Board,Piece
import random
pg.init()                                      #initiates a pygame instance
board = Board((512,512))
board.board_state["e5"] = Piece("pawn","white")
board.board_state["d6"] = Piece("pawn","black")
board.board_state["d5"] = Piece("pawn","black")


running = True                                  #variable checks if loop should go on
while running:                                  #game loop
    for event in pg.event.get():
        if event.type == pg.QUIT:               #Once exited the instance gets killed
            running = False

    #gamelogic
    board.build()
    board.manage_click()
    #board.display_turn()

    pg.display.flip()
pg.quit()



