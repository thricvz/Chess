from modules import Board

raw= """
. . . K . . . .
. . . . . . . .
. . . . . . . .
. . . . . . . .
. B . . . . . .
. . . . . . . .
. . . b . . . .
. . . . k . . .
"""

board = Board()
board.build_from_text(raw)

board.update_pieces_statuses()
w_b = board.pieces_in_play[2]
board.restrict_piece_movement(w_b)
board.display(w_b.position)