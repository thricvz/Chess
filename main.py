from modules import Board
board = Board()

"""
for piece in board.pieces_in_play:
    print("-"*15)
    print(f"{piece.color} {piece.type} at {piece.position}")
    possible_states = {"attacking":piece.attacking,"protecting":piece.protecting,"attacked by":piece.attacked_by,"protected by ":piece.protected_by}
    for state in possible_states.items():
        print(f"{state[0]} {len(state[1])} pieces:")
        for concerned_piece in state[1]:
            print(f"    {concerned_piece.color} {concerned_piece.type} at {concerned_piece.position}")

    print("-"*15)
"""