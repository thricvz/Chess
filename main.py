import pygame as pg 
from modules import Board,Piece
import random
pg.init()                                      #initiates a pygame instance
board = Board((512,512))
#board.generate_pieces()
board.board_state["e7"] = Piece("pawn","white")
board.board_state["e3"] = Piece("bishop","white")
board.board_state["h3"] = Piece("rook","black")
board.board_state["d7"] = Piece("knight","white")
board.board_state["g1"] = Piece("queen","white")
board.board_state["h2"] = Piece("king","white")

running = True                                  #variable checks if loop should go on
while running:                                  #game loop
    for event in pg.event.get():
        if event.type == pg.QUIT:               #Once exited the instance gets killed
            running = False

    #gamelogic
    board.build()
    board.manage_click()

    pg.display.flip()
pg.quit()



