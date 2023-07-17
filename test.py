from src.modules import Board

raw= """
. . k . . . . .
. . . . . . . .
. . . . . . . .
. P p . . . . .
. . . . . . . .
. . . . . . . .
. . . . P . . .
K . . . . . . .
"""

board = Board()
board.build_from_text(raw)

board.update_pieces_statuses()
w_p = board.pieces_in_play[1]
b_p = board.pieces_in_play[2]
b_p.times_moved = 1
w_p2 = board.pieces_in_play[3]
enp =  board.en_passant("white")
board.display(w_p.position)
board.move_piece(w_p2,"e3")
board.switch_turn()
board.update_en_passant_possiblity()
board.update_pieces_statuses()

board.display(w_p.position)